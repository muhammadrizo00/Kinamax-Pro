from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


# Admin main menu
def admin_main_menu() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text="🎬 Kino boshqaruvi"), KeyboardButton(text="📢 Kanal boshqaruvi")],
        [KeyboardButton(text="📊 Statistika"), KeyboardButton(text="📨 Xabar yuborish")],
        [KeyboardButton(text="👥 Foydalanuvchilar"), KeyboardButton(text="🔝 Super statistika")],
        [KeyboardButton(text="⚙️ Sozlamalar")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def delete_movie_confirm_btn(movie_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🗑 O'chirishni tasdiqlash",
                    callback_data=f"confirm_delete_movie_{movie_id}"
                )
            ],
            [
                InlineKeyboardButton(text="◀️ Orqaga", callback_data="back_admin")
            ]
        ]
    )

# Movie management
def movie_management_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="➕ Kino qo'shish", callback_data="add_movie")],
        [InlineKeyboardButton(text="🗑 Kino o'chirish", callback_data="delete_movie")],
        [InlineKeyboardButton(text="📋 Barcha kinolar", callback_data="list_movies")],
        [InlineKeyboardButton(text="🔍 Kino qidirish", callback_data="search_movie")],
        [InlineKeyboardButton(text="🔙 Ortga", callback_data="back_to_admin")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def channel_management_menu():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Kanal qo‘shish", callback_data="add_channel")],
        [InlineKeyboardButton(text="🗑 Kanal o‘chirish", callback_data="delete_channel")],
        [InlineKeyboardButton(text="📃 Barcha kanallar", callback_data="list_channels")],
        [InlineKeyboardButton(text="📌 Majburiy obunalar", callback_data="force_channels")],
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_admin")]
    ])
    return kb


def channel_delete_confirm(channel_id: int):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🗑 Ha, o‘chirish", callback_data=f"confirm_delete_channel_{channel_id}")],
        [InlineKeyboardButton(text="◀️ Bekor qilish", callback_data="cancel")]
    ])
    return kb


def force_switch(channel_id: int, is_active: bool):
    text = "❌ O‘chirish" if is_active else "✅ Yoqish"
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=text, callback_data=f"switch_force_{channel_id}")],
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="force_channels")]
    ])

def confirm_delete_channel_btn(channel_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🗑 O‘chirishni tasdiqlash",
                    callback_data=f"confirm_delete_channel_{channel_id}"
                )
            ],
            [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="channel_management")]
        ]
    )


# Channel type selection
def channel_type_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="📺 Asosiy kanal", callback_data="channel_type_main")],
        [InlineKeyboardButton(text="🔒 Majburiy kanal", callback_data="channel_type_mandatory")],
        [InlineKeyboardButton(text="👥 Guruh", callback_data="channel_type_group")],
        [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# Statistics menu
def statistics_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="📅 Kunlik", callback_data="stats_daily")],
        [InlineKeyboardButton(text="📆 Haftalik", callback_data="stats_weekly")],
        [InlineKeyboardButton(text="🗓 Oylik", callback_data="stats_monthly")],
        [InlineKeyboardButton(text="📊 Umumiy", callback_data="stats_total")],
        [InlineKeyboardButton(text="🔙 Ortga", callback_data="back_to_admin")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# Super statistics menu
def super_stats_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="🎬 Top kinolar", callback_data="top_movies")],
        [InlineKeyboardButton(text="👥 Faol foydalanuvchilar", callback_data="top_users")],
        [InlineKeyboardButton(text="⭐️ Rating statistikasi", callback_data="rating_stats")],
        [InlineKeyboardButton(text="📈 O'sish grafigi", callback_data="growth_chart")],
        [InlineKeyboardButton(text="🔙 Ortga", callback_data="back_to_admin")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# Broadcast menu
def broadcast_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="✅ Yuborish", callback_data="broadcast_confirm")],
        [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="broadcast_cancel")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# Movie delete confirmation
def delete_movie_confirm(movie_id: int) -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="✅ Ha, o'chirish", callback_data=f"confirm_delete_movie_{movie_id}")],
        [InlineKeyboardButton(text="❌ Yo'q", callback_data="cancel_delete_movie")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# Channel delete confirmation
def delete_channel_confirm(channel_id: int) -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="✅ Ha, o'chirish", callback_data=f"confirm_delete_channel_{channel_id}")],
        [InlineKeyboardButton(text="❌ Yo'q", callback_data="cancel_delete_channel")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# Movie list pagination
def movie_list_pagination(page: int, total_pages: int) -> InlineKeyboardMarkup:
    keyboard = []
    
    nav_buttons = []
    if page > 1:
        nav_buttons.append(InlineKeyboardButton(text="◀️ Oldingi", callback_data=f"movies_page_{page-1}"))
    
    nav_buttons.append(InlineKeyboardButton(text=f"{page}/{total_pages}", callback_data="current_page"))
    
    if page < total_pages:
        nav_buttons.append(InlineKeyboardButton(text="Keyingi ▶️", callback_data=f"movies_page_{page+1}"))
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    keyboard.append([InlineKeyboardButton(text="🔙 Ortga", callback_data="movie_management")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# User management
def user_management_menu(user_id: int) -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="🚫 Bloklash", callback_data=f"block_user_{user_id}")],
        [InlineKeyboardButton(text="✅ Blokdan chiqarish", callback_data=f"unblock_user_{user_id}")],
        [InlineKeyboardButton(text="👤 Profil", callback_data=f"view_user_{user_id}")],
        [InlineKeyboardButton(text="🔙 Ortga", callback_data="back_to_admin")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# Back button
def back_button(callback: str = "back_to_admin") -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="🔙 Ortga", callback_data=callback)]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# Cancel button
def cancel_button() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)