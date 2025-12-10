from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


# User main menu
def user_main_menu() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text="ℹ️ Yordam"), KeyboardButton(text="👤 Profil")],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


# Movie rating keyboard
def movie_rating_keyboard(movie_id: int) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="👍 Yoqdi", callback_data=f"rate_like_{movie_id}"),
            InlineKeyboardButton(text="👎 Yoqmadi", callback_data=f"rate_dislike_{movie_id}")
        ],
        [
            InlineKeyboardButton(text="⭐️", callback_data=f"star_1_{movie_id}"),
            InlineKeyboardButton(text="⭐️⭐️", callback_data=f"star_2_{movie_id}"),
            InlineKeyboardButton(text="⭐️⭐️⭐️", callback_data=f"star_3_{movie_id}"),
        ],
        [
            InlineKeyboardButton(text="⭐️⭐️⭐️⭐️", callback_data=f"star_4_{movie_id}"),
            InlineKeyboardButton(text="⭐️⭐️⭐️⭐️⭐️", callback_data=f"star_5_{movie_id}")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# Subscription check keyboard
def subscription_check_keyboard(channels: list) -> InlineKeyboardMarkup:
    keyboard = []
    
    for channel in channels:
        if channel.get('username'):
            url = f"https://t.me/{channel['username']}"
        elif channel.get('invite_link'):
            url = channel['invite_link']
        else:
            continue
            
        keyboard.append([InlineKeyboardButton(
            text=f"📢 {channel['title']}", 
            url=url
        )])
    
    keyboard.append([InlineKeyboardButton(
        text="✅ Obuna bo'ldim, tekshirish",
        callback_data="check_subscription"
    )])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# User profile menu
def user_profile_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="🎬 Ko'rilgan kinolar", callback_data="my_movies")],
        [InlineKeyboardButton(text="⭐️ Baholangan kinolar", callback_data="my_ratings")],
        [InlineKeyboardButton(text="📊 Mening statistikam", callback_data="my_stats")],
        [InlineKeyboardButton(text="🔙 Ortga", callback_data="back_to_main")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# Help menu
def help_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="📝 Qo'llanma", callback_data="help_guide")],
        [InlineKeyboardButton(text="❓ Savol-javob", callback_data="help_faq")],
        [InlineKeyboardButton(text="📞 Bog'lanish", url="https://t.me/support")],
        [InlineKeyboardButton(text="🔙 Ortga", callback_data="back_to_main")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# Share movie keyboard
def share_movie_keyboard(movie_code: str) -> InlineKeyboardMarkup:
    share_text = f"Bu kinoni tomosha qiling! Kod: {movie_code}"
    share_url = f"https://t.me/share/url?url={share_text}"
    
    keyboard = [
        [InlineKeyboardButton(text="🔄 Ulashish", url=share_url)],
        [InlineKeyboardButton(text="⭐️ Baholash", callback_data=f"rate_movie_{movie_code}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# Movie info keyboard
def movie_info_keyboard(movie_id: int, movie_code: str) -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="⭐️ Baholash", callback_data=f"open_rating_{movie_id}")],
        [InlineKeyboardButton(text="🔄 Ulashish", callback_data=f"share_movie_{movie_code}")],
        [InlineKeyboardButton(text="📊 Statistika", callback_data=f"movie_stats_{movie_id}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# Back to main button
def back_to_main_button() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="🔙 Asosiy menyu", callback_data="back_to_main")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# Rating thank you keyboard
def rating_thanks_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="🔍 Yana kino qidirish", callback_data="search_again")],
        [InlineKeyboardButton(text="🔙 Asosiy menyu", callback_data="back_to_main")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# Movie search results
def movie_search_results(movies: list) -> InlineKeyboardMarkup:
    keyboard = []
    
    for movie in movies:
        keyboard.append([InlineKeyboardButton(
            text=f"🎬 {movie['title'][:40]}...",
            callback_data=f"get_movie_{movie['code']}"
        )])
    
    keyboard.append([InlineKeyboardButton(text="🔙 Ortga", callback_data="back_to_main")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# Close button
def close_button() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="❌ Yopish", callback_data="close")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)