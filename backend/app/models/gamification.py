import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Float, Text
from sqlalchemy.orm import relationship
from app.db.session import Base


class Badge(Base):
    __tablename__ = "badges"

    id = Column(Integer, primary_key=True)
    code = Column(String(50), unique=True, index=True)
    title = Column(String(100))
    description = Column(String(255))
    icon_name = Column(String(50))
    xp_reward = Column(Integer, default=0, nullable=False)


class UserBadge(Base):
    __tablename__ = "user_badges"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    badge_id = Column(Integer, ForeignKey("badges.id"))
    unlocked_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("Student", back_populates="badges")
    badge = relationship("Badge")


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id"), nullable=False, index=True)
    code = Column(Text, nullable=True)
    passed = Column(Boolean, default=False, nullable=False)
    execution_time_ms = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
