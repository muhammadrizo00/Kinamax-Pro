import random
import string
from datetime import datetime, timedelta
from typing import Optional, List
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import Movie, User, Rating, Stats


class CodeGenerator:
    """Generate unique movie codes"""
    
    @staticmethod
    async def generate_unique_code(db: AsyncSession, length: int = 4) -> str:
        """Generate unique numeric code"""
        max_attempts = 100
        
        for _ in range(max_attempts):
            code = ''.join(random.choices(string.digits, k=length))
            
            # Check if code exists
            result = await db.execute(select(Movie).where(Movie.code == code))
            if not result.scalar_one_or_none():
                return code
        
        raise ValueError("Could not generate unique code after maximum attempts")
    
    @staticmethod
    async def validate_code(code: str) -> bool:
        """Validate code format"""
        return code.isdigit() and len(code) == 4


class StatsCalculator:
    """Calculate various statistics"""
    
    @staticmethod
    async def get_user_stats(db: AsyncSession, user_id: int) -> dict:
        """Get user statistics"""
        result = await db.execute(select(User).where(User.tg_id == user_id))
        user = result.scalar_one_or_none()
        
        if not user:
            return {}
        
        return {
            'watched_movies': user.watched_movies,
            'total_ratings': user.total_ratings,
            'joined_at': user.joined_at,
            'last_active': user.last_active
        }
    
    @staticmethod
    async def get_movie_stats(db: AsyncSession, movie_id: int) -> dict:
        """Get movie statistics"""
        result = await db.execute(select(Movie).where(Movie.id == movie_id))
        movie = result.scalar_one_or_none()
        
        if not movie:
            return {}
        
        # Calculate rating percentage
        total_ratings = movie.likes + movie.dislikes
        like_percentage = (movie.likes / total_ratings * 100) if total_ratings > 0 else 0
        
        return {
            'views': movie.views,
            'likes': movie.likes,
            'dislikes': movie.dislikes,
            'like_percentage': round(like_percentage, 1),
            'total_ratings': total_ratings
        }
    
    @staticmethod
    async def get_period_stats(db: AsyncSession, days: int = 1) -> dict:
        """Get statistics for specific period"""
        period_start = datetime.utcnow() - timedelta(days=days)
        
        # New users
        new_users_result = await db.execute(
            select(func.count(User.id)).where(User.joined_at >= period_start)
        )
        new_users = new_users_result.scalar()
        
        # New movies
        new_movies_result = await db.execute(
            select(func.count(Movie.id)).where(Movie.created_at >= period_start)
        )
        new_movies = new_movies_result.scalar()
        
        # Active users
        active_users_result = await db.execute(
            select(func.count(User.id)).where(User.last_active >= period_start)
        )
        active_users = active_users_result.scalar()
        
        return {
            'new_users': new_users,
            'new_movies': new_movies,
            'active_users': active_users,
            'period_days': days
        }
    
    @staticmethod
    async def get_top_movies(db: AsyncSession, limit: int = 10) -> List[dict]:
        """Get top movies by views"""
        result = await db.execute(
            select(Movie)
            .where(Movie.is_active == True)
            .order_by(Movie.views.desc())
            .limit(limit)
        )
        movies = result.scalars().all()
        
        return [
            {
                'id': movie.id,
                'code': movie.code,
                'title': movie.title,
                'views': movie.views,
                'likes': movie.likes,
                'dislikes': movie.dislikes
            }
            for movie in movies
        ]
    
    @staticmethod
    async def get_top_users(db: AsyncSession, limit: int = 10) -> List[dict]:
        """Get most active users"""
        result = await db.execute(
            select(User)
            .where(User.is_blocked == False)
            .order_by(User.watched_movies.desc())
            .limit(limit)
        )
        users = result.scalars().all()
        
        return [
            {
                'id': user.id,
                'name': user.first_name,
                'watched_movies': user.watched_movies,
                'total_ratings': user.total_ratings
            }
            for user in users
        ]


class MessageFormatter:
    """Format messages for better display"""
    
    @staticmethod
    def format_movie_info(movie: Movie, include_stats: bool = True) -> str:
        """Format movie information"""
        text = f"🎬 <b>{movie.title}</b>\n\n"
        
        if movie.description:
            text += f"{movie.description}\n\n"
        
        text += f"🔢 Kod: <code>{movie.code}</code>\n"
        
        if include_stats:
            text += f"👁 Ko'rilgan: {movie.views} marta\n"
            text += f"⭐️ Rating: {movie.likes} 👍 / {movie.dislikes} 👎\n"
        
        return text
    
    @staticmethod
    def format_user_profile(user: User) -> str:
        """Format user profile"""
        text = f"👤 <b>PROFIL</b>\n\n"
        text += f"👤 Ism: {user.first_name}\n"
        text += f"🆔 ID: <code>{user.tg_id}</code>\n"
        text += f"📅 Qo'shilgan: {user.joined_at.strftime('%d.%m.%Y')}\n\n"
        text += f"📊 STATISTIKA:\n"
        text += f"🎬 Ko'rilgan: {user.watched_movies} ta\n"
        text += f"⭐️ Baholangan: {user.total_ratings} ta\n"
        
        return text
    
    @staticmethod
    def format_stats(stats: dict, period: str = "Bugun") -> str:
        """Format statistics"""
        text = f"📊 <b>STATISTIKA - {period.upper()}</b>\n\n"
        
        if 'total_users' in stats:
            text += f"👥 Foydalanuvchilar: {stats['total_users']} ta\n"
        if 'new_users' in stats:
            text += f"   └ Yangi: {stats['new_users']} ta\n"
        
        if 'total_movies' in stats:
            text += f"\n🎬 Kinolar: {stats['total_movies']} ta\n"
        if 'new_movies' in stats:
            text += f"   └ Yangi: {stats['new_movies']} ta\n"
        
        if 'total_views' in stats:
            text += f"\n👁 Ko'rilgan: {stats['total_views']} marta\n"
        if 'total_ratings' in stats:
            text += f"⭐️ Baholanganlar: {stats['total_ratings']} ta\n"
        
        text += f"\n📅 Sana: {datetime.now().strftime('%d.%m.%Y %H:%M')}"
        
        return text
    
    @staticmethod
    def format_duration(seconds: int) -> str:
        """Format duration in human readable format"""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        
        if hours > 0:
            return f"{hours}s {minutes}m"
        return f"{minutes}m"
    
    @staticmethod
    def format_file_size(bytes: int) -> str:
        """Format file size in human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes < 1024.0:
                return f"{bytes:.1f} {unit}"
            bytes /= 1024.0
        return f"{bytes:.1f} TB"


class Validator:
    """Validate various inputs"""
    
    @staticmethod
    def is_valid_code(code: str) -> bool:
        """Check if code is valid format"""
        return isinstance(code, str) and code.isdigit() and len(code) == 4
    
    @staticmethod
    def is_valid_telegram_id(user_id: int) -> bool:
        """Check if Telegram ID is valid"""
        return isinstance(user_id, int) and user_id > 0
    
    @staticmethod
    def is_valid_channel_id(channel_id: int) -> bool:
        """Check if channel ID is valid"""
        return isinstance(channel_id, int) and channel_id < 0


class DateHelper:
    """Helper functions for dates"""
    
    @staticmethod
    def get_period_start(period_type: str) -> datetime:
        """Get start date for period"""
        now = datetime.utcnow()
        
        if period_type == "daily":
            return now - timedelta(days=1)
        elif period_type == "weekly":
            return now - timedelta(weeks=1)
        elif period_type == "monthly":
            return now - timedelta(days=30)
        else:
            return datetime.min
    
    @staticmethod
    def format_date(date: datetime, format: str = "%d.%m.%Y") -> str:
        """Format date"""
        return date.strftime(format)
    
    @staticmethod
    def get_time_ago(date: datetime) -> str:
        """Get human readable time ago"""
        now = datetime.utcnow()
        diff = now - date
        
        if diff.days > 365:
            return f"{diff.days // 365} yil oldin"
        elif diff.days > 30:
            return f"{diff.days // 30} oy oldin"
        elif diff.days > 0:
            return f"{diff.days} kun oldin"
        elif diff.seconds > 3600:
            return f"{diff.seconds // 3600} soat oldin"
        elif diff.seconds > 60:
            return f"{diff.seconds // 60} daqiqa oldin"
        else:
            return "hozirgina"