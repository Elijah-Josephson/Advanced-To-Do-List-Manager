from sqlalchemy import *
from sqlalchemy.orm import relationship
from typing import Literal, TypedDict
from datetime import datetime, timedelta

from db.base import Base


class Project(Base):
    __tablename__ = "Project"
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    description = Column(String(150), nullable=True)
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
    
    def __init__(self, name: str = "default_name", description: str = "-"):
        if len(name) > 30 :
            raise ValueError("Project name can't be longer than 30 characters.")
        if len(description) > 150 :
            raise ValueError("Project description can't be longer than 150 characters.")
        self.name = name
        self.description = description


class TaskDict(TypedDict):
    name: str
    description: str = "-"
    status: Literal["todo", "doing", "done"] = "todo"
    deadline: datetime = None
    project_id: int = 1


class Task(Base):
    __tablename__ = "Task"
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    description = Column(String(150))
    status = Column(
        Enum("todo", "doing", "done", name="status"),
        nullable=False
    )
    deadline = Column(DateTime)
    project_id = Column(Integer, ForeignKey("Project.id"), nullable=False)
    project = relationship("Project", back_populates="tasks")

    def __init__(self, inputs = TaskDict):
        if len(inputs["name"]) > 30 :
            raise ValueError("Task name can't be longer than 30 characters.")
        if len(inputs["description"]) > 150 :
            raise ValueError("Task description can't be longer than 150 characters.")
        self.name = inputs["name"]
        self.description = inputs["description"]
        self.status = inputs["status"]
        self.deadline = inputs["deadline"] or (datetime.now() + timedelta(days=10))
        self.project_id = inputs["project_id"]


