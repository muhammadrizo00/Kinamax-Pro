# 🚀 KinaMax Bot - Tezkor Boshlash

## ⚡ 5 daqiqada ishga tushiring!

### 1️⃣ Kerakli narsalar
```bash
✓ Python 3.8+
✓ Telegram Bot Token
✓ 5 daqiqa vaqt
```

### 2️⃣ O'rnatish (3 buyruq)
```bash
# 1. Loyihani yuklang
git clone https://github.com/yourusername/kinamax-bot.git
cd kinamax-bot

# 2. Virtual environment va dependencies
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# yoki: venv\Scripts\activate  # Windows
pip install -r requirements.txt

# 3. Sozlang va ishga tushiring
cp .env.example .env
# .env faylini tahrirlab, BOT_TOKEN qo'shing
python bot.py
```

### 3️⃣ Bot Token olish (2 daqiqa)
1. [@BotFather](https://t.me/BotFather) → `/newbot`
2. Bot nomini kiriting → Username kiriting
3. Token'ni `.env` fayliga qo'shing:
```env
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

### 4️⃣ Birinchi admin
```bash
# .env faylida o'z Telegram ID'ngizni qo'shing
ADMIN_IDS=123456789

# ID'ni olish: @userinfobot → /start
```

### 5️⃣ Ishlatish

**User:**
```
/start → Obuna → 1234 (kod) → Kino! ⭐️
```

**Admin:**
```
/admin → 🎬 Kino qo'shish → Video → Nom → Tavsif → ✅
```

---

## 🐳 Docker bilan (3 buyruq)

```bash
# 1. Build
docker-compose build

# 2. Run
docker-compose up -d

# 3. Logs
docker-compose logs -f
```

---

## 🆘 Muammo?

### Bot ishlamayapti?
```bash
# Token'ni tekshiring
cat .env | grep BOT_TOKEN

# Log'ni ko'ring
tail -f logs/bot.log
```

### Kino yuklanmayapti?
- File hajmi < 50MB
- Bot kanal admini
- Kanal ID to'g'ri

### Obuna ishlamayapti?
- Bot kanal/guruh admini
- Barcha admin huquqlar

---

## 📚 To'liq qo'llanma
- [README.md](README.md) - Batafsil ma'lumot
- [TUTORIAL.md](TUTORIAL.md) - Qadam-baqadam
- [GitHub Issues](https://github.com/yourusername/kinamax-bot/issues) - Yordam

---

## 🎯 Keyingi qadamlar

1. ✅ Bot ishga tushdi
2. 📢 Kanal yarating
3. 🎬 Birinchi kino qo'shing
4. 👥 Majburiy obuna sozlang
5. 📊 Statistikani kuzating

---

## ⚙️ Muhim sozlamalar

### Minimum (.env):
```env
BOT_TOKEN=your_token
ADMIN_IDS=your_id
```

### To'liq (.env):
```env
BOT_TOKEN=your_token
ADMIN_IDS=123456789,987654321
DATABASE_URL=sqlite+aiosqlite:///./kinamax.db
MOVIE_CHANNEL_ID=-1001234567890
```

---

## 🎬 Birinchi kino qo'shish

```
1. /admin
2. 🎬 Kino boshqaruvi
3. ➕ Kino qo'shish
4. Video yuborish
5. "Avatar 2023" (nom)
6. "Janr: Fantastika..." (tavsif)
7. ✅ Kod: 1234
8. Kanal/Guruhda e'lon qiling!
```

---

## 💡 Pro Tip
```bash
# Botni background'da ishlatish (Linux)
nohup python bot.py &

# Yoki screen bilan
screen -S kinamax
python bot.py
# Ctrl+A+D (detach)

# Yoki systemd service
sudo systemctl start kinamax
```

---

## 🌟 Xususiyatlar

✅ Kod orqali kino yuborish
✅ Majburiy obuna
✅ Rating (👍👎 + ⭐️)
✅ Admin panel
✅ Statistika
✅ Broadcast
✅ User profil
✅ Auto kod generatsiya

---

## 📞 Bog'lanish

- Telegram: [@yourusername](https://t.me/yourusername)
- GitHub: [kinamax-bot](https://github.com/yourusername/kinamax-bot)
- Email: support@kinamax.uz

---

**Omad tilaymiz! Bot bilan ishingiz samarali bo'lsin! 🚀**