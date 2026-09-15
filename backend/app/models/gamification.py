from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base
import datetime

class Badge(Base):
    __tablename__ = "badges"
    id = Column(Integer, primary_key=True)
    code = Column(String(50), unique=True, index=True)
    title = Column(String(100))
    description = Column(String(255))
    icon_name = Column(String(50))

class UserBadge(Base):
    __tablename__ = "user_badges"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("students.id"))
    badge_id = Column(Integer, ForeignKey("badges.id"))
    unlocked_at = Column(DateTime, default=datetime.datetime.utcnow)
