from abc import ABC, abstractmethod
from models import *
from sqlalchemy import *
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError
from typing import List, TypeVar, Generic, Literal

from db.session import Session


T = TypeVar("T")
class Repository(ABC, Generic[T]):
    @abstractmethod
    def get(self, id: int) -> T:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> list[T]:
        raise NotImplementedError
    
    @abstractmethod
    def add(self, **kwargs: object) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def update(self, id: int, **kwargs: object) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def delete(self, id: int) -> None:
        raise NotImplementedError
    

class ProjectRepository(Repository[Project]):
    def get(self, id: int) -> Project | None:
        with Session() as session:
            return session.query(Project).options(joinedload(Project.tasks)).filter(Project.id == id).first()

    def get_all(self) -> List[Project]:
        with Session() as session:
            return session.query(Project).all()

    def add(self, name: str, description: str = "") -> Project:
        with Session() as session:
            project = Project(name=name, description=description)
            session.add(project)
            session.commit()
            session.refresh(project)
            return project

    def update(self, id: int, name: str, description: str) -> Project:
        with Session() as session:
            project = session.query(Project).filter(Project.id == id).first()
            if project == None:
                raise ValueError(f"Project with id {id} not found")
            project.name = name
            project.description = description
            session.commit()
            session.refresh(project)
            return project

    def delete(self, id: int) -> None:
        with Session() as session:
            project = session.query(Project).filter(Project.id == id).first()
            if project is None:
                raise ValueError(f"Project with id {id} not found")
            session.delete(project)
            session.commit()


class TaskRepository(Repository[Task]):
    def __init__(self) -> None :
        pass

    def get(self, id: int) -> Task | None:
        with Session() as session:
            return session.query(Task).filter(Task.id == id).first()

    def get_all(self) -> List[Task]:
        with Session() as session:
            return session.query(Task).all()

    def get_all_by_project(self, project_id: int) -> List[Task]:
        with Session() as session:
            return session.query(Task).filter(Task.project_id == project_id).all()
        
    def add(self, inputs: TaskDict) -> Task:
        with Session() as session:
            task = Task(inputs)
            session.add(task)
            session.commit()
            session.refresh(task)
            return task
        
    def update(self, id: int, inputs: TaskDict) -> Task:
        with Session() as session:
            task = session.query(Task).filter(Task.id == id).first()
            if task == None:
                raise ValueError(f"Project with id {id} not found")
            task.name = inputs["name"]
            task.description = inputs["description"]
            task.status = inputs["status"]
            task.deadline = inputs["deadline"]
            session.commit()
            session.refresh(task)
            return task
        
    def delete(self, id: int) -> None:
        with Session() as session:
            task = session.query(Task).filter(Task.id == id).first()
            if task is None:
                raise ValueError(f"Task with id {id} not found")
            
            session.delete(task)
            session.commit()