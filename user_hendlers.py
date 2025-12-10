from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, ChatMemberUpdated
from aiogram.filters import Command, ChatMemberUpdatedFilter, KICKED, MEMBER, ADMINISTRATOR
from aiogram.fsm.context import FSMContext
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from database import User, Movie, Channel, Rating, Subscription
from user_keyboard import *


router = Router()


# Check subscription to mandatory channels
async def check_user_subscriptions(bot: Bot, user_id: int, db: AsyncSession) -> tuple[bool, list]:
    result = await db.execute(
        select(Channel).where(
            and_(Channel.channel_type == "mandatory", Channel.is_active == True)
        )
    )
    channels = result.scalars().all()
    
    not_subscribed = []
    
    for channel in channels:
        try:
            member = await bot.get_chat_member(channel.channel_id, user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                not_subscribed.append({
                    'id': channel.channel_id,
                    'title': channel.title,
                    'username': channel.username,
                    'invite_link': channel.invite_link
                })
        except Exception:
            not_subscribed.append({
                'id': channel.channel_id,
                'title': channel.title,
                'username': channel.username,
                'invite_link': channel.invite_link
            })
    
    return len(not_subscribed) == 0, not_subscribed


# Get or create user
async def get_or_create_user(message: Message, db: AsyncSession) -> User:
    result = await db.execute(select(User).where(User.tg_id == message.from_user.id))
    user = result.scalar_one_or_none()
    
    if not user:
        user = User(
            tg_id=message.from_user.id,
            first_name=message.from_user.first_name,
            username=message.from_user.username
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
    else:
        user.last_active = datetime.utcnow()
        user.first_name = message.from_user.first_name
        user.username = message.from_user.username
        await db.commit()
    
    return user


# Start command
@router.message(Command("start"))
async def start_handler(message: Message, db: AsyncSession):
    user = await get_or_create_user(message, db)
    
    if user.is_blocked:
        await message.answer("❌ Siz bloklangansiz! Admin bilan bog'laning.  📞 @rizo3313")
        return
    
    # Check subscriptions
    is_subscribed, channels = await check_user_subscriptions(message.bot, message.from_user.id, db)
    
    if not is_subscribed:
        text = """
🎬 <b>KinaMax'ga xush kelibsiz!</b>

Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling:
        """
        await message.answer(
            text,
            reply_markup=subscription_check_keyboard(channels),
            parse_mode="HTML"
        )
        return
    
    text = f"""
👋 Assalomu aleykum, <b>{message.from_user.first_name}</b>!

🎬 <b>KinaMax</b> botiga xush kelibsiz!


🔍 Kino qidirish uchun 4-xonali kodni yuboring.
Masalan: <code>1234</code>

📱 Yoki menyudan foydalaning ⬇️

admin bilan bog'laning: @rizo3313
    """

    await message.answer(text, reply_markup=user_main_menu(), parse_mode="HTML")


# Check subscription callback
@router.callback_query(F.data == "check_subscription")
async def check_subscription_callback(callback: CallbackQuery, db: AsyncSession):
    is_subscribed, channels = await check_user_subscriptions(
        callback.bot, 
        callback.from_user.id, 
        db
    )
    
    if not is_subscribed:
        await callback.answer("❌ Siz hali barcha kanallarga obuna bo'lmagansiz!", show_alert=True)
        return
    
    text = f"""
✅ Obuna tasdiqlandi!

👋 Assalomu aleykum, <b>{callback.from_user.first_name}</b>!

🎬 <b>KinaMax</b> botiga xush kelibsiz!

🔍 Kino qidirish uchun 4-xonali kodni yuboring.
Masalan: <code>1234</code>

📱 Yoki menyudan foydalaning ⬇️
admin bilan bog'laning: @rizo3313
    """
    
    await callback.message.edit_text(text, parse_mode="HTML")
    await callback.message.answer("Tanlang:", reply_markup=user_main_menu())
    await callback.answer()


# Movie search by code
@router.message(F.text.regexp(r'^\d{4}$'))
async def search_movie_by_code(message: Message, db: AsyncSession):
    user = await get_or_create_user(message, db)
    
    if user.is_blocked:
        await message.answer("❌ Siz bloklangansiz!")
        return
    
    # Check subscriptions
    is_subscribed, channels = await check_user_subscriptions(message.bot, message.from_user.id, db)
    
    if not is_subscribed:
        text = "❌ Kino ko'rish uchun kanallarga obuna bo'ling:"
        await message.answer(
            text,
            reply_markup=subscription_check_keyboard(channels)
        )
        return
    
    code = message.text.strip()
    
    # Search movie
    result = await db.execute(
        select(Movie).where(and_(Movie.code == code, Movie.is_active == True))
    )
    movie = result.scalar_one_or_none()
    
    if not movie:
        await message.answer(
            "❌ Bunday kodli kino topilmadi!\n\n"
            "Iltimos, to'g'ri kodni kiriting yoki admin bilan bog'laning."
        )
        return
    
    # Send loading animation
    loading_msg = await message.answer("🎬 Kino yuklanmoqda...")
    
    # Send movie
    caption = f"""
🎬 <b>{movie.title}</b>

{movie.description or ""}

🔢 Kod: <code>{movie.code}</code>
👁 Ko'rilgan: {movie.views} marta
⭐️ Rating: {movie.likes} 👍 / {movie.dislikes} 👎

@Kinamax_bot orqali
    """
    
    try:
        await message.bot.send_video(
            chat_id=message.chat.id,
            video=movie.file_id,
            caption=caption,
            parse_mode="HTML",
            reply_markup=movie_rating_keyboard(movie.id)
        )
        
        # Update stats
        movie.views += 1
        user.watched_movies += 1
        await db.commit()
        
        await loading_msg.delete()
        
    except Exception as e:
        await loading_msg.edit_text("❌ Kino yuborishda xatolik yuz berdi!")


# Movie rating - Like
@router.callback_query(F.data.startswith("rate_like_"))
async def rate_movie_like(callback: CallbackQuery, db: AsyncSession):
    movie_id = int(callback.data.split("_")[-1])
    
    # Check if already rated
    result = await db.execute(
        select(Rating).where(
            and_(Rating.movie_id == movie_id, Rating.user_id == callback.from_user.id)
        )
    )
    existing_rating = result.scalar_one_or_none()
    
    if existing_rating:
        await callback.answer("✅ Siz bu kinoni allaqachon baholagansiz!", show_alert=True)
        return
    
    # Get movie
    movie_result = await db.execute(select(Movie).where(Movie.id == movie_id))
    movie = movie_result.scalar_one_or_none()
    
    if not movie:
        await callback.answer("❌ Kino topilmadi!", show_alert=True)
        return
    
    # Get user
    user_result = await db.execute(select(User).where(User.tg_id == callback.from_user.id))
    user = user_result.scalar_one_or_none()
    
    # Add rating
    rating = Rating(
        user_id=user.id,
        movie_id=movie_id,
        rating_type="like"
    )
    db.add(rating)
    
    movie.likes += 1
    user.total_ratings += 1
    
    await db.commit()
    
    await callback.message.edit_reply_markup(reply_markup=rating_thanks_keyboard())
    await callback.answer("✅ Rahmat! Sizga yoqqanidan xursandmiz! 👍", show_alert=True)


# Movie rating - Dislike
@router.callback_query(F.data.startswith("rate_dislike_"))
async def rate_movie_dislike(callback: CallbackQuery, db: AsyncSession):
    movie_id = int(callback.data.split("_")[-1])
    
    # Check if already rated
    result = await db.execute(
        select(Rating).where(
            and_(Rating.movie_id == movie_id, Rating.user_id == callback.from_user.id)
        )
    )
    existing_rating = result.scalar_one_or_none()
    
    if existing_rating:
        await callback.answer("✅ Siz bu kinoni allaqachon baholagansiz!", show_alert=True)
        return
    
    # Get movie
    movie_result = await db.execute(select(Movie).where(Movie.id == movie_id))
    movie = movie_result.scalar_one_or_none()
    
    # Get user
    user_result = await db.execute(select(User).where(User.tg_id == callback.from_user.id))
    user = user_result.scalar_one_or_none()
    
    # Add rating
    rating = Rating(
        user_id=user.id,
        movie_id=movie_id,
        rating_type="dislike"
    )
    db.add(rating)
    
    movie.dislikes += 1
    user.total_ratings += 1
    
    await db.commit()
    
    await callback.message.edit_reply_markup(reply_markup=rating_thanks_keyboard())
    await callback.answer("Fikringiz uchun rahmat! 👎", show_alert=True)


# Star rating
@router.callback_query(F.data.startswith("star_"))
async def rate_movie_stars(callback: CallbackQuery, db: AsyncSession):
    parts = callback.data.split("_")
    stars = int(parts[1])
    movie_id = int(parts[2])
    
    # Check if already rated
    result = await db.execute(
        select(Rating).where(
            and_(Rating.movie_id == movie_id, Rating.user_id == callback.from_user.id)
        )
    )
    existing_rating = result.scalar_one_or_none()
    
    if existing_rating:
        await callback.answer("✅ Siz bu kinoni allaqachon baholagansiz!", show_alert=True)
        return
    
    # Get user
    user_result = await db.execute(select(User).where(User.tg_id == callback.from_user.id))
    user = user_result.scalar_one_or_none()
    
    # Add rating
    rating = Rating(
        user_id=user.id,
        movie_id=movie_id,
        rating_type="stars",
        stars=stars
    )
    db.add(rating)
    
    user.total_ratings += 1
    await db.commit()
    
    await callback.message.edit_reply_markup(reply_markup=rating_thanks_keyboard())
    await callback.answer(f"✅ {stars} ⭐️ baho berildi! Rahmat!", show_alert=True)


# User profile
@router.message(F.text == "👤 Profil")
async def user_profile(message: Message, db: AsyncSession):
    result = await db.execute(select(User).where(User.tg_id == message.from_user.id))
    user = result.scalar_one_or_none()
    
    if not user:
        await message.answer("❌ Xatolik yuz berdi!")
        return
    
    text = f"""
👤 <b>PROFIL</b>

👤 Ism: {user.first_name}
🆔 ID: <code>{user.tg_id}</code>
📅 Qo'shilgan: {user.joined_at.strftime('%d.%m.%Y')}

📊 STATISTIKA:
🎬 Ko'rilgan kinolar: {user.watched_movies} ta
⭐️ Baholangan kinolar: {user.total_ratings} ta
    """
    
    await message.answer(text, reply_markup=user_profile_menu(), parse_mode="HTML")


# Help
@router.message(F.text == "ℹ️ Yordam")
async def help_command(message: Message):
    text = """
ℹ️ <b>YORDAM</b>

🔍 <b>Kino qidirish:</b>
Bot yoki kanallarda e'lon qilingan 4-xonali kodni yuboring.
Misol: <code>1234</code>

⭐️ <b>Baholash:</b>
Kino ko'rgandan so'ng "👍 Yoqdi" yoki "👎 Yoqmadi" tugmasini bosing.

👤 <b>Profil:</b>
O'z statistikangizni ko'ring.

❓ <b>Savollar?</b>
Admin: @rizo3313
    """
    
    await message.answer(text, parse_mode="HTML")


# Search again callback
@router.callback_query(F.data == "search_again")
async def search_again(callback: CallbackQuery):
    text = """
🔍 Yangi kino qidirish uchun 4-xonali kodni yuboring:

Misol: <code>1234</code>
    """
    
    await callback.message.answer(text, parse_mode="HTML")
    await callback.answer()


# Close message
@router.callback_query(F.data == "close")
async def close_message(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer()