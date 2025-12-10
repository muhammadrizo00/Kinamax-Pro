from aiogram import Router, F , Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
import random
import string

from database import User, Movie, Channel, Rating, Stats, Broadcast, get_db
from admin_keyboard import *
from config import Config

router = Router()


# FSM States
class AdminStates(StatesGroup):
    waiting_movie = State()
    waiting_movie_title = State()
    waiting_movie_desc = State()
    waiting_movie_delete = State()
    waiting_channel_add = State()
    waiting_add_channel = State()
    waiting_delete_channel = State()
    waiting_channel_delete = State()
    waiting_broadcast = State()


class ChannelStates(StatesGroup):
    waiting_channel_username = State()
    waiting_delete_channel = State()


# Code generator
def generate_code() -> str:
    return ''.join(random.choices(string.digits, k=4))

# Check if user is admin
async def is_admin(user_id: int, db: AsyncSession) -> bool:
    # 1) .env dagi adminlar
    if user_id in Config.ADMIN_IDS:
        return True

    # 2) Bazadagi adminlar
    result = await db.execute(select(User).where(User.tg_id == user_id))
    user = result.scalar_one_or_none()
    return user and user.is_admin


# Admin main menu
@router.message(Command("admin"))
async def admin_panel(message: Message, db: AsyncSession):
    if not await is_admin(message.from_user.id, db):
        await message.answer("❌ Sizda admin huquqi yo'q!")
        return
    
    text = """
🎛 <b>ADMIN PANEL</b>

Botni boshqarish uchun quyidagi bo'limlardan birini tanlang:
    """
    
    await message.answer(text, reply_markup=admin_main_menu(), parse_mode="HTML")


# Movie management
@router.message(F.text == "🎬 Kino boshqaruvi")
async def movie_management(message: Message, db: AsyncSession):
    if not await is_admin(message.from_user.id, db):
        return
    
    result = await db.execute(select(func.count(Movie.id)))
    total_movies = result.scalar()
    
    text = f"""
🎬 <b>KINO BOSHQARUVI</b>

📊 Jami kinolar: {total_movies} ta

Quyidagi amallardan birini tanlang:
    """
    
    await message.answer(text, reply_markup=movie_management_menu(), parse_mode="HTML")


@router.callback_query(F.data == "movie_management")
async def movie_management_callback(callback: CallbackQuery, db: AsyncSession):
    await movie_management(callback.message, db)
    await callback.answer()


# Add movie
@router.callback_query(F.data == "add_movie")
async def add_movie_start(callback: CallbackQuery, state: FSMContext):
    text = """
➕ <b>KINO QO'SHISH</b>

Iltimos, kino faylini yuboring (video yoki file sifatida).

Format: MP4, MKV, AVI va boshqalar qo'llab-quvvatlanadi.

❌ Bekor qilish uchun /cancel
    """
    
    await callback.message.answer(text, reply_markup=cancel_button(), parse_mode="HTML")
    await state.set_state(AdminStates.waiting_movie)
    await callback.answer()


# Add movie – file qabul qilish va kanalga yuborish
@router.message(AdminStates.waiting_movie, F.video | F.document)
async def add_movie_file(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    # Get file_id va file_name
    if message.video:
        file_obj = message.video
    else:
        file_obj = message.document

    file_id = file_obj.file_id
    file_name = file_obj.file_name or "Video"

    # Faylni kanalga yuborish
    try:
        sent_msg = await bot.send_video(
            chat_id=Config.MOVIE_CHANNEL_ID,
            video=file_id,
            caption=file_name
        )
        # Kanaldagi file_id saqlash uchun
        channel_file_id = sent_msg.video.file_id
    except Exception as e:
        await message.answer(f"❌ Kanalga yuborishda xato: {e}")
        return

    # State ga saqlash
    await state.update_data(file_id=channel_file_id, default_title=file_name)

    text = f"""
✅ Fayl qabul qilindi va kanalga yuborildi!

📝 Endi kino nomini kiriting:

Misol: Spiderman 2023 UzbekTili

❌ Bekor qilish: /cancel
    """
    await message.answer(text, parse_mode="HTML")
    await state.set_state(AdminStates.waiting_movie_title)


@router.message(AdminStates.waiting_movie_title, F.text)
async def add_movie_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    
    text = """
📄 Kino haqida qisqacha tavsif yozing:

Misol:
Janr: Fantastika, Jangovor
Yil: 2023
Til: O'zbek (Dublyaj)
Sifat: Full HD

Yoki "yuq" yozing tavsif bermaslik uchun.

❌ Bekor qilish: /cancel
    """
    
    await message.answer(text, parse_mode="HTML")
    await state.set_state(AdminStates.waiting_movie_desc)


@router.message(AdminStates.waiting_movie_desc, F.text)
async def add_movie_desc(message: Message, state: FSMContext, db: AsyncSession):
    description = None if message.text.lower() in ['yuq', 'yo\'q', 'no'] else message.text
    
    data = await state.get_data()
    
    # Generate unique code
    while True:
        code = generate_code()
        result = await db.execute(select(Movie).where(Movie.code == code))
        if not result.scalar_one_or_none():
            break
    
    # Create movie
    movie = Movie(
        code=code,
        title=data['title'],
        description=description,
        file_id=data['file_id'],
        created_by=message.from_user.id
    )
    
    db.add(movie)
    await db.commit()
    await db.refresh(movie)
    
    text = f"""
✅ <b>KINO MUVAFFAQIYATLI QO'SHILDI!</b>

🎬 Nomi: {movie.title}
🔢 Kod: <code>{movie.code}</code>
📅 Qo'shilgan: {movie.created_at.strftime('%d.%m.%Y %H:%M')}

Foydalanuvchilar bu kinoni <code>{movie.code}</code> kodi orqali ko'rishlari mumkin!
    """
    
    await message.answer(text, reply_markup=back_button(), parse_mode="HTML")
    await state.clear()


# 1️⃣ — Delete movie start
@router.callback_query(F.data == "delete_movie")
async def delete_movie_start(callback: CallbackQuery, state: FSMContext):
    text = """
🗑 <b>KINO O'CHIRISH</b>

O'chirmoqchi bo'lgan kino kodini kiriting:

Misol: 1234

❌ Bekor qilish: /cancel
    """

    await callback.message.answer(text, reply_markup=cancel_button(), parse_mode="HTML")
    await state.set_state(AdminStates.waiting_movie_delete)
    await callback.answer()


# 2️⃣ — Code entered → show confirm
@router.message(AdminStates.waiting_movie_delete)
async def delete_movie_confirm(message: Message, state: FSMContext, db: AsyncSession):
    code = message.text.strip()

    result = await db.execute(select(Movie).where(Movie.code == code))
    movie = result.scalar_one_or_none()

    if not movie:
        await message.answer("❌ Bunday kodli kino topilmadi!")
        return

    text = f"""
❓ <b>Ushbu kinoni o'chirmoqchimisiz?</b>

🎬 Nomi: {movie.title}
🔢 Kod: {movie.code}
👁 Ko'rilgan: {movie.views} marta
⭐️ Rating: {movie.likes} 👍 / {movie.dislikes} 👎
    """

    await state.update_data(movie_id=movie.id)

    await message.answer(
        text,
        reply_markup=delete_movie_confirm_btn(movie.id),
        parse_mode="HTML"
    )


# 3️⃣ — Final delete
@router.callback_query(F.data.startswith("confirm_delete_movie_"))
async def delete_movie_final(callback: CallbackQuery, state: FSMContext, db: AsyncSession):
    movie_id = int(callback.data.split("_")[-1])

    result = await db.execute(select(Movie).where(Movie.id == movie_id))
    movie = result.scalar_one_or_none()

    if movie:
        await db.delete(movie)
        await db.commit()

        await callback.message.edit_text(
            f"✅ Kino '{movie.title}' muvaffaqiyatli o'chirildi!",
            reply_markup=back_button()
        )
    else:
        await callback.message.edit_text("❌ Kino topilmadi!")

    await state.clear()
    await callback.answer()


# List movies
@router.callback_query(F.data.startswith("list_movies"))
async def list_movies(callback: CallbackQuery, db: AsyncSession):
    page = 1
    if "_page_" in callback.data:
        page = int(callback.data.split("_")[-1])
    
    per_page = 10
    offset = (page - 1) * per_page
    
    result = await db.execute(
        select(Movie)
        .where(Movie.is_active == True)
        .order_by(desc(Movie.created_at))
        .limit(per_page)
        .offset(offset)
    )
    movies = result.scalars().all()
    
    count_result = await db.execute(select(func.count(Movie.id)).where(Movie.is_active == True))
    total = count_result.scalar()
    total_pages = (total + per_page - 1) // per_page
    
    if not movies:
        await callback.message.edit_text("📭 Kinolar topilmadi!", reply_markup=back_button())
        return
    
    text = f"🎬 <b>BARCHA KINOLAR</b> (Sahifa {page}/{total_pages})\n\n"
    
    for movie in movies:
        text += f"🔢 <code>{movie.code}</code> - {movie.title}\n"
        text += f"   👁 {movie.views} | ⭐️ {movie.likes}👍 {movie.dislikes}👎\n\n"
    
    await callback.message.edit_text(
        text,
        reply_markup=movie_list_pagination(page, total_pages),
        parse_mode="HTML"
    )
    await callback.answer()

# CONTINUATION OF admin_handlers.py

# Channel management
@router.message(F.text == "📢 Kanal boshqaruvi")
async def channel_management(message: Message, db: AsyncSession):
    text = """
📢 <b>KANAL BOSHQARUVI</b>

Quyidagi amallardan birini tanlang:
    """
    await message.answer(text, reply_markup=channel_management_menu(), parse_mode="HTML")


@router.callback_query(F.data == "add_channel")
async def add_channel_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "➕ Qo‘shmoqchi bo‘lgan kanal username yoki ID sini kiriting.\n\nMisol: @mychannel yoki -1001234567890",
        reply_markup=cancel_button()
    )
    await state.set_state(ChannelStates.waiting_channel_username)
    await callback.answer()

@router.message(ChannelStates.waiting_channel_username)
async def add_channel_finish(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
    username = message.text.strip()

    try:
        chat = await bot.get_chat(username)
        bot_member = await bot.get_chat_member(chat.id, bot.id)
    except:
        await message.answer("❌ Kanal topilmadi yoki bot kanalga kirmagan!")
        return

    if bot_member.status != "administrator":
        await message.answer("❌ Bot kanalga ADMIN bo‘lishi shart!")
        return

    new_channel = Channel(
        channel_id=chat.id,
        title=chat.title,
        username=chat.username,
        channel_type="mandatory",
        invite_link=chat.invite_link
    )
    db.add(new_channel)
    await db.commit()

    await message.answer(
        f"✅ Kanal qo‘shildi!\n\n<b>{chat.title}</b>\nID: <code>{chat.id}</code>",
        parse_mode="HTML"
    )

    await state.clear()



@router.callback_query(F.data == "delete_channel")
async def delete_channel_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "🗑 O‘chirmoqchi bo‘lgan kanal ID yoki username kiriting:",
        reply_markup=cancel_button()
    )
    await state.set_state(ChannelStates.waiting_delete_channel)
    await callback.answer()


@router.message(ChannelStates.waiting_delete_channel)
async def delete_channel_confirm_step(message: Message, state: FSMContext, db: AsyncSession):
    inp = message.text.strip()

    result = await db.execute(
        select(Channel).where((Channel.username == inp) | (Channel.channel_id == int(inp)))
    )
    channel = result.scalar_one_or_none()

    if not channel:
        await message.answer("❌ Bunday kanal topilmadi!")
        return

    await state.update_data(channel_id=channel.id)

    await message.answer(
        f"❓ <b>{channel.title}</b> kanalini o‘chirmoqchimisiz?",
        reply_markup=channel_delete_confirm(channel.id),
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("confirm_delete_channel_"))
async def delete_channel_final(callback: CallbackQuery, db: AsyncSession, state: FSMContext):
    channel_id = int(callback.data.split("_")[-1])

    # Avval kanalni bazadan olish
    result = await db.execute(select(Channel).where(Channel.id == channel_id))
    channel = result.scalar_one_or_none()

    if not channel:
        await callback.message.edit_text("❌ Kanal topilmadi!")
        await callback.answer()
        return

    # ORM orqali o‘chirish – eng to‘g‘ri yo‘l
    await db.delete(channel)
    await db.commit()

    await callback.message.edit_text(f"✅ Kanal '{channel.title}' muvaffaqiyatli o‘chirildi!")
    await callback.answer()
    await state.clear()



@router.callback_query(F.data.startswith("confirm_delete_channel_"))
async def delete_channel_final(callback: CallbackQuery, state: FSMContext, db: AsyncSession):
    channel_id = int(callback.data.split("_")[-1])

    result = await db.execute(select(Channel).where(Channel.id == channel_id))
    channel = result.scalar_one_or_none()

    if channel:
        await db.delete(channel)
        await db.commit()
        await callback.message.edit_text(
            f"✅ Kanal o‘chirildi:\n<b>{channel.username}</b>",
            reply_markup=channel_management_menu()
        )
    else:
        await callback.message.edit_text("❌ Kanal topilmadi!")

    await state.clear()
    await callback.answer()


@router.callback_query(F.data == "force_channels")
async def force_channels_list(callback: CallbackQuery, db: AsyncSession):
    result = await db.execute(select(Channel).where(Channel.channel_type == "mandatory"))
    channels = result.scalars().all()

    if not channels:
        await callback.message.edit_text("❌ Majburiy obuna kanallari yo‘q!")
        return

    text = "<b>📌 Majburiy obuna kanallari:</b>\n\n"
    for c in channels:
        text += f"📢 <b>{c.title}</b>\nID: <code>{c.channel_id}</code>\n\n"

    await callback.message.edit_text(text, parse_mode="HTML")

@router.callback_query(F.data == "list_channels")
async def list_channels(callback: CallbackQuery, db: AsyncSession):
    result = await db.execute(select(Channel))
    channels = result.scalars().all()

    if not channels:
        await callback.message.edit_text("❌ Hali hech qanday kanal qo‘shilmagan!")
        return

    text = "<b>📃 Barcha kanallar:</b>\n\n"

    for c in channels:
        text += f"📌 <b>{c.title}</b>\nID: <code>{c.channel_id}</code>\nUsername: @{c.username}\n\n"

    await callback.message.edit_text(text, parse_mode="HTML")




# Statistics
@router.message(F.text == "📊 Statistika")
async def statistics(message: Message, db: AsyncSession):
    if not await is_admin(message.from_user.id, db):
        return
    
    text = """
📊 <b>STATISTIKA</b>

Qaysi davr statistikasini ko'rmoqchisiz?
    """
    
    await message.answer(text, reply_markup=statistics_menu(), parse_mode="HTML")


@router.callback_query(F.data.startswith("stats_"))
async def show_statistics(callback: CallbackQuery, db: AsyncSession):
    stats_type = callback.data.split("_")[1]
    
    # Get counts
    users_result = await db.execute(select(func.count(User.id)))
    total_users = users_result.scalar()
    
    movies_result = await db.execute(select(func.count(Movie.id)))
    total_movies = movies_result.scalar()
    
    views_result = await db.execute(select(func.sum(Movie.views)))
    total_views = views_result.scalar() or 0
    
    ratings_result = await db.execute(select(func.count(Rating.id)))
    total_ratings = ratings_result.scalar()
    
    # Time-based stats
    if stats_type == "daily":
        period = datetime.now() - timedelta(days=1)
        period_name = "Bugun"
    elif stats_type == "weekly":
        period = datetime.now() - timedelta(days=7)
        period_name = "Bu hafta"
    elif stats_type == "monthly":
        period = datetime.now() - timedelta(days=30)
        period_name = "Bu oy"
    else:
        period = None
        period_name = "Umumiy"
    
    if period:
        new_users_result = await db.execute(
            select(func.count(User.id)).where(User.joined_at >= period)
        )
        new_users = new_users_result.scalar()
    else:
        new_users = total_users
    
    text = f"""
📊 <b>STATISTIKA - {period_name.upper()}</b>

👥 Foydalanuvchilar: {total_users} ta
   └ Yangi: {new_users} ta

🎬 Kinolar: {total_movies} ta
👁 Ko'rilgan: {total_views} marta
⭐️ Baholanganlar: {total_ratings} ta

📅 Sana: {datetime.now().strftime('%d.%m.%Y %H:%M')}
    """
    
    await callback.message.edit_text(text, reply_markup=back_button(), parse_mode="HTML")
    await callback.answer()


# Super statistics
@router.message(F.text == "🔝 Super statistika")
async def super_statistics(message: Message, db: AsyncSession):
    if not await is_admin(message.from_user.id, db):
        return
    
    text = """
🔝 <b>SUPER STATISTIKA</b>

Qaysi ma'lumotni ko'rmoqchisiz?
    """
    
    await message.answer(text, reply_markup=super_stats_menu(), parse_mode="HTML")


@router.callback_query(F.data == "top_movies")
async def top_movies(callback: CallbackQuery, db: AsyncSession):
    result = await db.execute(
        select(Movie)
        .where(Movie.is_active == True)
        .order_by(desc(Movie.views))
        .limit(10)
    )
    movies = result.scalars().all()
    
    text = "🏆 <b>TOP 10 ENG KO'P KO'RILGAN KINOLAR</b>\n\n"
    
    medals = ["🥇", "🥈", "🥉"]
    for i, movie in enumerate(movies, 1):
        medal = medals[i-1] if i <= 3 else f"{i}."
        text += f"{medal} {movie.title}\n"
        text += f"   👁 {movie.views} | ⭐️ {movie.likes}👍 {movie.dislikes}👎\n\n"
    
    await callback.message.edit_text(text, reply_markup=back_button(), parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "top_users")
async def top_users(callback: CallbackQuery, db: AsyncSession):
    result = await db.execute(
        select(User)
        .where(User.is_blocked == False)
        .order_by(desc(User.watched_movies))
        .limit(10)
    )
    users = result.scalars().all()
    
    text = "👥 <b>TOP 10 ENG FAOL FOYDALANUVCHILAR</b>\n\n"
    
    medals = ["🥇", "🥈", "🥉"]
    for i, user in enumerate(users, 1):
        medal = medals[i-1] if i <= 3 else f"{i}."
        name = user.first_name or "Unknown"
        text += f"{medal} {name}\n"
        text += f"   🎬 Ko'rgan: {user.watched_movies} | ⭐️ Baholagan: {user.total_ratings}\n\n"
    
    await callback.message.edit_text(text, reply_markup=back_button(), parse_mode="HTML")
    await callback.answer()


# Broadcast message
@router.message(F.text == "📨 Xabar yuborish")
async def broadcast_start(message: Message, state: FSMContext, db: AsyncSession):
    if not await is_admin(message.from_user.id, db):
        return
    
    text = """
📨 <b>OMMAVIY XABAR YUBORISH</b>

Barcha foydalanuvchilarga yubormoqchi bo'lgan xabaringizni yozing:

⚠️ Xabar text, foto, video yoki file bo'lishi mumkin.

❌ Bekor qilish: /cancel
    """
    
    await message.answer(text, reply_markup=cancel_button(), parse_mode="HTML")
    await state.set_state(AdminStates.waiting_broadcast)


@router.message(AdminStates.waiting_broadcast)
async def broadcast_confirm(message: Message, state: FSMContext, db: AsyncSession):
    # Get total users
    result = await db.execute(select(func.count(User.id)).where(User.is_blocked == False))
    total = result.scalar()
    
    await state.update_data(broadcast_message=message.message_id, broadcast_chat=message.chat.id)
    
    text = f"""
✅ Xabar qabul qilindi!

👥 Jo'natiladi: {total} ta foydalanuvchiga

Xabarni yuborishni tasdiqlaysizmi?
    """
    
    await message.answer(text, reply_markup=broadcast_menu(), parse_mode="HTML")


@router.callback_query(F.data == "broadcast_confirm")
async def broadcast_send(callback: CallbackQuery, state: FSMContext, db: AsyncSession):
    data = await state.get_data()
    
    # Get all users
    result = await db.execute(select(User).where(User.is_blocked == False))
    users = result.scalars().all()
    
    sent = 0
    failed = 0
    
    progress_msg = await callback.message.answer("📤 Xabar yuborilmoqda... 0%")
    
    total = len(users)
    for i, user in enumerate(users, 1):
        try:
            await callback.bot.copy_message(
                chat_id=user.tg_id,
                from_chat_id=data['broadcast_chat'],
                message_id=data['broadcast_message']
            )
            sent += 1
        except Exception:
            failed += 1
        
        # Update progress every 10%
        if i % max(1, total // 10) == 0:
            percent = int((i / total) * 100)
            await progress_msg.edit_text(f"📤 Xabar yuborilmoqda... {percent}%")
    
    # Save broadcast stats
    broadcast = Broadcast(
        message_text="Broadcast message",
        sent_count=sent,
        failed_count=failed,
        created_by=callback.from_user.id,
        completed_at=datetime.now()
    )
    db.add(broadcast)
    await db.commit()
    
    text = f"""
✅ <b>XABAR YUBORILDI!</b>

✅ Muvaffaqiyatli: {sent} ta
❌ Xato: {failed} ta
📊 Jami: {total} ta
    """
    
    await progress_msg.edit_text(text, parse_mode="HTML")
    await state.clear()
    await callback.answer()


# Cancel operation
@router.message(Command("cancel"), StateFilter("*"))
@router.callback_query(F.data == "cancel", StateFilter("*"))
async def cancel_operation(event, state: FSMContext):
    await state.clear()
    
    text = "❌ Amal bekor qilindi!"
    
    if isinstance(event, Message):
        await event.answer(text, reply_markup=admin_main_menu())
    else:
        await event.message.answer(text, reply_markup=admin_main_menu())
        await event.answer()


# Back to admin
@router.callback_query(F.data == "back_to_admin")
async def back_to_admin(callback: CallbackQuery):
    text = """
🎛 <b>ADMIN PANEL</b>

Botni boshqarish uchun quyidagi bo'limlardan birini tanlang:
    """
    
    await callback.message.answer(text, reply_markup=admin_main_menu(), parse_mode="HTML")
    await callback.message.delete()
    await callback.answer()