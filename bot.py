import asyncio
from datetime import datetime
import logging
import sys
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from database import init_db, close_db
from admin_hendlers import router as admin_router
from user_hendlers import router as user_router
from middlewares import setup_middlewares
from config import Config
from dotenv import load_dotenv

load_dotenv()


# 🔧 logs papkasini yaratish
os.makedirs("logs", exist_ok=True)

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

async def on_startup(bot: Bot):
    """Actions on bot startup"""
    logger.info("🤖 Bot starting...")
    
    # Initialize database
    await init_db()
    
    # Get bot info
    me = await bot.get_me()
    logger.info(f"✅ Bot started: @{me.username}")
    logger.info(f"📊 Bot ID: {me.id}")
    logger.info(f"👤 Bot name: {me.first_name}")
    
    # Send notification to admins
    for admin_id in Config.ADMIN_IDS:
        try:
            await bot.send_message(
                admin_id,
                "✅ <b>Bot ishga tushdi!</b>\n\n"
                f"🤖 Bot: @{me.username}\n"
                f"🕐 Vaqt: {datetime.now().strftime('%d.%m.%Y %H:%M')}",
                parse_mode="HTML"
            )
        except Exception as e:
            logger.warning(f"Could not notify admin {admin_id}: {e}")


async def on_shutdown(bot: Bot):
    """Actions on bot shutdown"""
    logger.info("🛑 Bot stopping...")
    
    # Send notification to admins
    for admin_id in Config.ADMIN_IDS:
        try:
            await bot.send_message(
                admin_id,
                "⚠️ <b>Bot to'xtatildi!</b>\n\n"
                f"🕐 Vaqt: {datetime.now().strftime('%d.%m.%Y %H:%M')}",
                parse_mode="HTML"
            )
        except Exception as e:
            logger.warning(f"Could not notify admin {admin_id}: {e}")
    
    # Close database
    await close_db()
    logger.info("✅ Bot stopped")


async def main():
    """Main bot function"""
    from datetime import datetime
    
    # Validate configuration
    try:
        Config.validate()
    except ValueError as e:
        logger.error(f"❌ Configuration error: {e}")
        return
    
    # Initialize bot and dispatcher
    bot = Bot(
        token=Config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    dp = Dispatcher(storage=MemoryStorage())
    
    # Setup middlewares
    setup_middlewares(dp)
    
    # Register routers
    dp.include_router(admin_router)
    dp.include_router(user_router)
    
    # Register startup/shutdown handlers
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    # Start polling
    logger.info("🚀 Starting polling...")
    try:
        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types(),
            drop_pending_updates=True
        )
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Bot stopped by user (Ctrl+C)")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}", exc_info=True)