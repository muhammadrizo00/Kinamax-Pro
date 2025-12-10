from sqlalchemy import Column, Integer, String, BigInteger, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import datetime
from typing import AsyncGenerator
import os

# Database URL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./kinamax.db")

# Engine va Session
engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(BigInteger, unique=True, nullable=False, index=True)
    first_name = Column(String(255))
    username = Column(String(255), nullable=True)
    is_admin = Column(Boolean, default=False)
    is_blocked = Column(Boolean, default=False)
    watched_movies = Column(Integer, default=0)
    total_ratings = Column(Integer, default=0)
    joined_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    ratings = relationship("Rating", back_populates="user", cascade="all, delete-orphan")
    subscriptions = relationship("Subscription", back_populates="user", cascade="all, delete-orphan")


class Movie(Base):
    __tablename__ = "movies"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(4), unique=True, nullable=False, index=True)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    file_id = Column(String(500), nullable=False)
    channel_message_id = Column(Integer, nullable=True)
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    dislikes = Column(Integer, default=0)
    average_rating = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(BigInteger, nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    ratings = relationship("Rating", back_populates="movie", cascade="all, delete-orphan")


class Channel(Base):
    __tablename__ = "channels"
    
    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(BigInteger, unique=True, nullable=False, index=True)
    channel_type = Column(String(50), nullable=False)  # main/mandatory/group
    title = Column(String(500))
    username = Column(String(255), nullable=True)
    invite_link = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
    added_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    subscriptions = relationship("Subscription", back_populates="channel", cascade="all, delete-orphan")


class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    channel_id = Column(Integer, ForeignKey("channels.id", ondelete="CASCADE"))
    subscribed_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="subscriptions")
    channel = relationship("Channel", back_populates="subscriptions")


class Rating(Base):
    __tablename__ = "ratings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"))
    rating_type = Column(String(10))  # like/dislike
    stars = Column(Integer, nullable=True)  # 1-5 stars
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="ratings")
    movie = relationship("Movie", back_populates="ratings")


class Stats(Base):
    __tablename__ = "stats"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.utcnow, index=True)
    total_users = Column(Integer, default=0)
    new_users = Column(Integer, default=0)
    active_users = Column(Integer, default=0)
    total_movies = Column(Integer, default=0)
    total_views = Column(Integer, default=0)
    total_ratings = Column(Integer, default=0)
    stats_type = Column(String(20), default="daily")  # daily/weekly/monthly


class Broadcast(Base):
    __tablename__ = "broadcasts"
    
    id = Column(Integer, primary_key=True, index=True)
    message_text = Column(Text, nullable=False)
    sent_count = Column(Integer, default=0)
    failed_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    created_by = Column(BigInteger, nullable=False)


# Database dependency
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# Initialize database
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database initialized successfully!")


# Close database
async def close_db():
    await engine.dispose()
    print("✅ Database connection closed!")