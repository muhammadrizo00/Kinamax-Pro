# 🎬 KinaMax Bot - ULTRA PRO MAX

Professional Telegram bot kino tarqatish uchun. Kod orqali kino yuborish, majburiy obuna, rating va admin panel.

## ⚡ Xususiyatlar

### User qismi:
- ✅ 4-xonali kod orqali kino qidirish
- ⭐️ Kinolarni baholash (Like/Dislike + 5 yulduzli)
- 👤 Shaxsiy profil va statistika
- 📊 Ko'rilgan va baholangan kinolar
- 🔒 Majburiy obuna tekshiruvi

### Admin qismi:
- 🎬 Kino qo'shish/o'chirish (avtomatik kod generatsiya)
- 📢 Kanal boshqaruvi
- 📨 Ommaviy xabar yuborish (broadcast)
- 📊 Statistika (kunlik, haftalik, oylik)
- 🔝 Super statistika (top kinolar, faol userlar)
- 👥 Foydalanuvchilar boshqaruvi

## 🚀 O'rnatish

### 1. Repozitoriyani clone qiling:
```bash
git clone https://github.com/yourusername/kinamax-bot.git
cd kinamax-bot
```

### 2. Virtual environment yarating:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# yoki
venv\Scripts\activate  # Windows
```

### 3. Kerakli kutubxonalarni o'rnating:
```bash
pip install -r requirements.txt
```

### 4. .env faylini sozlang:
```bash
cp .env.example .env
# .env faylini tahrirlang va o'z ma'lumotlaringizni kiriting
```

### 5. Admin qo'shish:
Database'da admin yaratish uchun botni ishga tushiring va bazaga qo'lda admin qo'shing yoki
database.py'da birinchi userni avtomatik admin qilish uchun kod qo'shing.

```python
# Birinchi foydalanuvchini admin qilish uchun (user_handlers.py'da):
if user.id == 1:  # Birinchi user
    user.is_admin = True
    await db.commit()
```

### 6. Botni ishga tushiring:
```bash
python bot.py
```

## 📋 Fayl strukturasi

```
kinamax-bot/
├── bot.py                 # Asosiy bot fayli
├── database.py            # Database modellari va config
├── admin_handlers.py      # Admin handlerlari
├── user_handlers.py       # User handlerlari
├── admin_keyboard.py      # Admin klaviaturalari
├── user_keyboard.py       # User klaviaturalari
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables namunasi
├── .env                  # Sizning sozlamalaringiz (git'ga yuklamang!)
├── README.md             # Bu fayl
└── kinamax.db           # SQLite database (avtomatik yaratiladi)
```

## 🔧 Bot Token olish

1. Telegram'da [@BotFather](https://t.me/BotFather) botiga boring
2. `/newbot` buyrug'ini yuboring
3. Bot nomini va username'ini kiriting
4. Token'ni `.env` fayliga qo'shing

## 📢 Kanal yaratish va sozlash

1. Telegram'da yangi kanal yarating
2. Botni kanalga admin qiling (barcha huquqlar)
3. Kanal ID'sini olish uchun [@userinfobot](https://t.me/userinfobot)'ga kanaldan xabar forward qiling
4. ID'ni `.env` fayliga qo'shing

## 💡 Foydalanish

### User uchun:
1. Botni `/start` qiling
2. Majburiy kanallarga obuna bo'ling
3. 4-xonali kod yuboring (masalan: `1234`)
4. Kinoni tomosha qiling va baholang!

### Admin uchun:
1. `/admin` buyrug'ini yuboring
2. "🎬 Kino boshqaruvi" tugmasini bosing
3. "➕ Kino qo'shish" tugmasini tanlang
4. Video faylni yuboring
5. Nom va tavsif kiriting
6. Bot avtomatik 4-xonali kod beradi!

## 🔒 Xavfsizlik

- `.env` faylini hech qachon git'ga yuklamang
- Bot token'ini hech kim bilan bo'lishmang
- Admin ID'larini ehtiyotkorlik bilan saqlang
- Database backup'larini muntazam oling

## 📊 Database struktura

- **users** - Foydalanuvchilar ma'lumotlari
- **movies** - Kinolar va kodlar
- **channels** - Kanallar ro'yxati
- **ratings** - Foydalanuvchilar baholari
- **subscriptions** - Obuna ma'lumotlari
- **stats** - Statistika
- **broadcasts** - Yuborilgan xabarlar

## 🆘 Muammolarni hal qilish

### Bot ishlamayapti?
- Token to'g'riligini tekshiring
- Bot internetga ulangan ekanligini tekshiring
- Log fayllarni ko'rib chiqing (`bot.log`)

### Kino yuklanmayapti?
- File hajmi 50MB dan oshmaganligini tekshiring (Telegram limit)
- Bot kanalda admin ekanligini tekshiring
- File ID to'g'ri saqlanganligini tekshiring

### Majburiy obuna ishlamayapti?
- Bot kanal/guruhda admin bo'lishi kerak
- Kanal ID to'g'ri kiritilganligini tekshiring
- Bot'ga "Get chat member" huquqi berilganligini tekshiring

## 🤝 Hissa qo'shish

Pull request'lar xush kelibsiz! Katta o'zgarishlar uchun avval issue oching.

## 📝 Litsenziya

MIT License

## 👨‍💻 Muallif

KinaMax Bot - ULTRA PRO MAX versiya

---

**⚠️ E'tibor:** Bu bot faqat ta'lim maqsadida. Mualliflik huquqini hurmat qiling!

## 🎯 Keyingi yangilanishlar

- [ ] Inline mode qo'shish
- [ ] Kino kategoriyalari
- [ ] Qidiruv funksiyasi
- [ ] Payment integratsiyasi
- [ ] Web admin panel
- [ ] Bot statistika dashboard
- [ ] Telegram Stars integratsiyasi

---

💬 Savollar bo'lsa: [Telegram](https://t.me/yourusername)
🌟 Loyha yoqqan bo'lsa, star qo'yishni unutmang!