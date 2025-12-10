from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from database import get_db, User
from config import Config

logger = logging.getLogger(__name__)


class DatabaseMiddleware(BaseMiddleware):
    """Middleware to inject database session"""
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        async for session in get_db():
            data['db'] = session
            try:
                return await handler(event, data)
            except Exception as e:
                logger.error(f"Error in handler: {e}")
                await session.rollback()
                raise


class LoggingMiddleware(BaseMiddleware):
    """Middleware to log all events"""
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        # Log message
        if isinstance(event, Message):
            user = event.from_user
            text = event.text or event.caption or "[Media]"
            logger.info(
                f"Message from {user.id} (@{user.username}): {text[:50]}"
            )
        
        # Log callback
        elif isinstance(event, CallbackQuery):
            user = event.from_user
            logger.info(
                f"Callback from {user.id} (@{user.username}): {event.data}"
            )
        
        return await handler(event, data)


class ThrottlingMiddleware(BaseMiddleware):
    """Middleware to prevent spam"""
    
    def __init__(self, rate_limit: int = 1):
        self.rate_limit = rate_limit
        self.user_timings: Dict[int, float] = {}
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        import time
        
        user_id = None
        if isinstance(event, Message):
            user_id = event.from_user.id
        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id
        
        if user_id:
            current_time = time.time()
            last_time = self.user_timings.get(user_id, 0)
            
            if current_time - last_time < self.rate_limit:
                # Too fast, ignore
                if isinstance(event, CallbackQuery):
                    await event.answer(
                        "⏳ Iltimos, biroz kutib turing...",
                        show_alert=True
                    )
                return
            
            self.user_timings[user_id] = current_time
        
        return await handler(event, data)


class AdminCheckMiddleware(BaseMiddleware):
    """Middleware to check admin rights"""
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        # Get user ID
        user_id = None
        if isinstance(event, Message):
            user_id = event.from_user.id
            text = event.text or ""
        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id
            text = event.data or ""
        else:
            return await handler(event, data)
        
        # Check if admin command
        is_admin_command = (
            text.startswith("/admin") or
            text.startswith("admin_") or
            "🎬 Kino boshqaruvi" in text or
            "📢 Kanal boshqaruvi" in text or
            "📊 Statistika" in text or
            "📨 Xabar yuborish" in text
        )
        
        if is_admin_command:
            # Check if user is admin
            db: AsyncSession = data.get('db')
            if db:
                from sqlalchemy import select
                result = await db.execute(
                    select(User).where(User.tg_id == user_id)
                )
                user = result.scalar_one_or_none()
                
                if not user or not user.is_admin:
                    if isinstance(event, Message):
                        await event.answer("❌ Sizda admin huquqi yo'q!")
                    elif isinstance(event, CallbackQuery):
                        await event.answer(
                            "❌ Sizda admin huquqi yo'q!",
                            show_alert=True
                        )
                    return
        
        return await handler(event, data)


class UserActivityMiddleware(BaseMiddleware):
    """Middleware to track user activity"""
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        # Update user activity
        user_id = None
        if isinstance(event, Message):
            user_id = event.from_user.id
        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id
        
        if user_id:
            db: AsyncSession = data.get('db')
            if db:
                from sqlalchemy import select
                from datetime import datetime
                
                result = await db.execute(
                    select(User).where(User.tg_id == user_id)
                )
                user = result.scalar_one_or_none()
                
                if user:
                    user.last_active = datetime.utcnow()
                    await db.commit()
        
        return await handler(event, data)


class BlockCheckMiddleware(BaseMiddleware):
    """Middleware to check if user is blocked"""
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        # Get user ID
        user_id = None
        if isinstance(event, Message):
            user_id = event.from_user.id
        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id
        
        if user_id:
            db: AsyncSession = data.get('db')
            if db:
                from sqlalchemy import select
                
                result = await db.execute(
                    select(User).where(User.tg_id == user_id)
                )
                user = result.scalar_one_or_none()
                
                if user and user.is_blocked:
                    if isinstance(event, Message):
                        await event.answer(
                            "❌ Siz bloklangansiz! Admin bilan bog'laning."
                        )
                    elif isinstance(event, CallbackQuery):
                        await event.answer(
                            "❌ Siz bloklangansiz!",
                            show_alert=True
                        )
                    return
        
        return await handler(event, data)


def setup_middlewares(dp):
    """Setup all middlewares"""
    
    # Database middleware (must be first)
    dp.message.middleware(DatabaseMiddleware())
    dp.callback_query.middleware(DatabaseMiddleware())
    
    # Logging middleware
    dp.message.middleware(LoggingMiddleware())
    dp.callback_query.middleware(LoggingMiddleware())
    
    # Block check
    dp.message.middleware(BlockCheckMiddleware())
    dp.callback_query.middleware(BlockCheckMiddleware())
    
    # Throttling
    dp.message.middleware(ThrottlingMiddleware(rate_limit=1))
    dp.callback_query.middleware(ThrottlingMiddleware(rate_limit=0.5))
    
    # User activity tracking
    dp.message.middleware(UserActivityMiddleware())
    dp.callback_query.middleware(UserActivityMiddleware())
    
    logger.info("✅ Middlewares registered successfully!")