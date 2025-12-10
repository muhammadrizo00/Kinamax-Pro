# 📚 KinaMax Bot - Batafsil Qo'llanma

## 🎯 Kirish

KinaMax Bot - bu Telegram orqali kino tarqatish uchun professional bot. Bu qo'llanmada botni o'rnatish va ishlatishni batafsil o'rganamiz.

---

## 📥 1-QADAM: O'rnatish

### 1.1. Python o'rnatish
```bash
# Linux/Mac
sudo apt install python3 python3-pip python3-venv

# Windows
# Python.org saytidan yuklab oling
```


### 1.2. Loyihani yuklab olish
```bash
git clone https://github.com/yourusername/kinamax-bot.git
cd kinamax-bot
```

### 1.3. Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# yoki
venv\Scripts\activate  # Windows
```

### 1.4. Kutubxonalarni o'rnatish
```bash
pip install -r requirements.txt
```

---

## 🤖 2-QADAM: Bot yaratish

### 2.1. BotFather orqali bot yaratish

1. Telegram'da [@BotFather](https://t.me/BotFather) botiga boring
2. `/newbot` buyrug'ini yuboring
3. Bot nomini kiriting (masalan: `KinaMax Bot`)
4. Username kiriting (masalan: `KinaMaxBot`)
5. Token'ni nusxalang va saqlang

### 2.2. Bot sozlamalari

BotFather'da qo'shimcha sozlamalar:
```
/setdescription - Bot haqida ma'lumot
/setabouttext - Qisqacha tavsif
/setuserpic - Bot rasmi
/setcommands - Buyruqlar ro'yxati
```

Buyruqlar ro'yxati:
```
start - Botni ishga tushirish
help - Yordam
profile - Profil
admin - Admin panel (faqat adminlar uchun)
```

---

## 📢 3-QADAM: Kanal yaratish

### 3.1. Kino kanali

1. Yangi kanal yarating (`KinaMax Movies`)
2. Public yoki Private qiling
3. Botni kanalga admin qiling
4. Kanal ID'sini oling:
   - [@userinfobot](https://t.me/userinfobot) botiga kanaldan xabar forward qiling
   - ID'ni nusxalang (masalan: `-1001234567890`)

### 3.2. Majburiy obuna kanali

1. Yangi kanal yarating (`KinaMax Channel`)
2. Public qiling (`@KinaMaxChannel`)
3. Botni admin qiling
4. ID'sini oling

---

## ⚙️ 4-QADAM: Konfiguratsiya

### 4.1. .env fayli

`.env.example` faylini `.env` ga nusxalang:
```bash
cp .env.example .env
```

`.env` faylini tahrirlang:
```env
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
DATABASE_URL=sqlite+aiosqlite:///./kinamax.db
ADMIN_IDS=123456789,987654321
MOVIE_CHANNEL_ID=-1001234567890
```

### 4.2. Admin ID olish

O'z Telegram ID'ngizni bilish uchun:
1. [@userinfobot](https://t.me/userinfobot) botiga `/start` yuboring
2. ID'ni nusxalang
3. `.env` fayliga qo'shing

---

## 🚀 5-QADAM: Botni ishga tushirish

### 5.1. Database yaratish

Bot birinchi marta ishga tushganda database avtomatik yaratiladi:
```bash
python bot.py
```

### 5.2. Admin huquqini berish

Agar siz birinchi foydalanuvchi bo'lsangiz, avtomatik admin bo'lasiz. Agar yo'q bo'lsa, database'ga qo'lda qo'shing:

```python
# Python shell'da
from database import *
import asyncio

async def make_admin():
    await init_db()
    async for db in get_db():
        result = await db.execute(select(User).where(User.tg_id == YOUR_TELEGRAM_ID))
        user = result.scalar_one_or_none()
        if user:
            user.is_admin = True
            await db.commit()
            print("✅ Admin qo'shildi!")

asyncio.run(make_admin())
```

---

## 🎬 6-QADAM: Kino qo'shish

### 6.1. Bot orqali

1. Botga `/admin` buyrug'ini yuboring
2. "🎬 Kino boshqaruvi" tugmasini bosing
3. "➕ Kino qo'shish" tugmasini tanlang
4. Video faylni yuboring
5. Kino nomini kiriting
6. Tavsif kiriting (yoki "yuq")
7. Bot avtomatik kod beradi!

### 6.2. Kod tizimi

- Har bir kino 4-xonali kod oladi (masalan: `1234`)
- Kod noyob bo'lishi kerak
- Foydalanuvchilar kod orqali kino topadi

---

## 👥 7-QADAM: Foydalanish

### 7.1. User uchun

1. Botga `/start` yuboring
2. Majburiy kanallarga obuna bo'ling
3. 4-xonali kod yuboring
4. Kinoni tomosha qiling!
5. Baholang (👍/👎 yoki ⭐️)

### 7.2. Admin uchun

**Kino boshqaruvi:**
- Kino qo'shish
- Kino o'chirish
- Barcha kinolar ro'yxati
- Kino qidirish

**Kanal boshqaruvi:**
- Kanal qo'shish
- Kanal o'chirish
- Majburiy obuna

**Statistika:**
- Kunlik/Haftalik/Oylik
- Top kinolar
- Faol foydalanuvchilar

**Xabar yuborish:**
- Barcha foydalanuvchilarga
- Progress ko'rsatish

---

## 📊 8-QADAM: Statistika

### 8.1. Bot statistikasi

Admin panelda statistikani ko'rish:
1. `/admin` → "📊 Statistika"
2. Davrni tanlang (kunlik/haftalik/oylik)
3. Ma'lumotlarni ko'ring

### 8.2. Super statistika

1. `/admin` → "🔝 Super statistika"
2. Tanlang:
   - Top kinolar
   - Faol foydalanuvchilar
   - Rating statistikasi

---

## 🔧 9-QADAM: Muammolarni hal qilish

### 9.1. Bot ishlamayapti

**Sabablari:**
- Token noto'g'ri
- Internet yo'q
- Python versiyasi eski

**Yechim:**
```bash
# Log'larni ko'ring
cat bot.log

# Bot'ni qayta ishga tushiring
python bot.py
```

### 9.2. Kino yuklanmayapti

**Sabablari:**
- File hajmi katta (50MB limit)
- Bot kanal admini emas
- File ID noto'g'ri

**Yechim:**
- File hajmini kichraytiring
- Bot'ni kanal adminiga qo'shing
- File ID'ni tekshiring

### 9.3. Majburiy obuna ishlamayapti

**Sabablari:**
- Bot kanal admini emas
- Kanal ID noto'g'ri
- Bot huquqlari yetarli emas

**Yechim:**
- Bot'ga barcha admin huquqlarini bering
- Kanal ID'ni tekshiring
- Bot'ni qayta ishga tushiring

---

## 💡 10-QADAM: Pro Maslahatlar

### 10.1. Xavfsizlik

- Token'ni hech qachon ulashmang
- `.env` faylini git'ga yuklamang
- Admin ID'larini ehtiyotkorlik bilan saqlang
- Database backup'larini oling

### 10.2. Optimizatsiya

- Database'ni muntazam tozalang
- Eski kinolarni arxivlang
- Log fayllarni tekshiring
- Server resurslarini monitoring qiling

### 10.3. Marketing

- Kino kodlarini kanallarda e'lon qiling
- Majburiy obuna kanalini faol qiling
- Reklama videolarini qo'shing
- Foydalanuvchilar bilan muloqot qiling

---

## 📱 11-QADAM: Qo'shimcha funksiyalar

### 11.1. Inline Mode (keyingi versiya)

```python
# inline_handlers.py
@router.inline_query()
async def inline_search(inline_query: InlineQuery):
    # Kino qidirish inline mode orqali
    pass
```

### 11.2. Payment integratsiyasi

```python
# payment_handlers.py
@router.message(F.successful_payment)
async def successful_payment(message: Message):
    # Premium funksiyalar
    pass
```

### 11.3. Web Admin Panel

React yoki Vue.js bilan admin panel yaratish.

---

## 🆘 Yordam

### Savollar uchun:
- Telegram: [@yourusername](https://t.me/yourusername)
- Email: support@kinamax.uz
- GitHub Issues: [kinamax-bot/issues](https://github.com/yourusername/kinamax-bot/issues)

### Foydali linklar:
- [Aiogram Documentation](https://docs.aiogram.dev/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Telegram Bot API](https://core.telegram.org/bots/api)

---

## 📝 Xulosa

KinaMax Bot professional va kuchli bot bo'lib, kino tarqatish uchun barcha kerakli funksiyalarga ega. Bu qo'llanma orqali siz botni to'liq o'rganib oldingiz.

**Omad tilaymiz! 🎬**

---

**Yaratildi:** 2024
**Versiya:** 1.0 ULTRA PRO MAX
**Muallif:** KinaMax Team