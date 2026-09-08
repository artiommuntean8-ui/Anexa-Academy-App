from sqlalchemy import Column, Integer, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class TestCase(Base):
    __tablename__ = 'test_cases'
    id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey('assignments.id', ondelete='CASCADE'), nullable=False)
    input_data = Column(Text, nullable=True) 
    expected_output = Column(Text, nullable=False) 
    is_hidden = Column(Boolean, default=False)
    
    assignment = relationship('Assignment', back_populates='test_cases')
