import enum
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class StatEnum(str, enum.Enum):
    todo = "todo"
    doing = "doing"
    done = "done"

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, default="none")
    deadline = Column(Date, nullable=True)
    status = Column(Enum(StatEnum), nullable=False, default=StatEnum.todo)
    closed_at = Column(DateTime, nullable=True)

    project = relationship("Project", back_populates="tasks")
