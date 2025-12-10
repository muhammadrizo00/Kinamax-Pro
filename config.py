import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Bot configuration"""
    
    # Bot settings
    BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN")
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./kinamax.db")
    
    # Admin IDs
    ADMIN_IDS = [
        int(admin_id.strip()) 
        for admin_id in os.getenv("ADMIN_IDS", "ADMIN_IDS").split(",") 
        if admin_id.strip()
    ]
    
    # Movie Channel
    MOVIE_CHANNEL_ID = int(os.getenv("MOVIE_CHANNEL_ID", "0"))
    
    # Bot settings
    MOVIES_PER_PAGE = 10
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    CODE_LENGTH = 4
    
    # Messages
    WELCOME_MESSAGE = """
👋 Assalomu aleykum, <b>{name}</b>!

🎬 <b>KinaMax</b> botiga xush kelibsiz!

Bu bot orqali siz:
✅ 4-xonali kod bilan kinolarni topishingiz
✅ Kinolarni baholashingiz
✅ O'z profilingizni ko'rishingiz mumkin!

🔍 Kino qidirish uchun 4-xonali kodni yuboring.
Masalan: <code>1234</code>
    """
    
    SUBSCRIPTION_REQUIRED = """
🔒 Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling:
    """
    
    MOVIE_NOT_FOUND = """
❌ Bunday kodli kino topilmadi!

Iltimos, to'g'ri kodni kiriting yoki admin bilan bog'laning.
    """
    
    @classmethod
    def validate(cls):
        """Validate configuration"""
        errors = []
        
        if not cls.BOT_TOKEN or cls.BOT_TOKEN == "YOUR_BOT_TOKEN":
            errors.append("BOT_TOKEN is not set!")
        
        if not cls.ADMIN_IDS:
            errors.append("ADMIN_IDS is not set!")
        
        if errors:
            raise ValueError("Configuration errors:\n" + "\n".join(errors))
    
    @classmethod
    def get_info(cls):
        """Get configuration info"""
        return f"""
🔧 Bot Configuration:
├─ Database: {cls.DATABASE_URL.split('///')[0]}
├─ Admins: {len(cls.ADMIN_IDS)}
├─ Movies per page: {cls.MOVIES_PER_PAGE}
└─ Max file size: {cls.MAX_FILE_SIZE / (1024*1024):.0f}MB
        """


# Auto-validate on import
try:
    Config.validate()
    print("✅ Configuration loaded successfully!")
    print(Config.get_info())
except ValueError as e:
    print(f"❌ Configuration error: {e}")
    print("Please check your .env file!")