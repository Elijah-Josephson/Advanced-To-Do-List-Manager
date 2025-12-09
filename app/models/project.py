from sqlalchemy import Column, Integer, String, Text, Date
from sqlalchemy.orm import relationship
from app.db.base import Base

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text, default="")
    deadline = Column(Date, nullable=True)

    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
