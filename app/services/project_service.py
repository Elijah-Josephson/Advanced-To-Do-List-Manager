from dotenv import load_dotenv
import os

from exceptions.service_exceptions import *
from repositories.repositories import *

load_dotenv()

project_repository = ProjectRepository()
    

def create_project(name: str, description: str) -> Project:
    projects = project_repository.get_all()
    if len(projects) >= int(os.getenv("MAX_NUMBER_OF_PROJECT")):
        raise MaximumNumberOfProjectsReached
    for project in projects:
        if name == project.name:
            raise ProjectNameAlreadyExists
    return project_repository.add(name, description)
    

def list_projects() -> List[Project] :
    return project_repository.get_all()


def validate_project_id(target_id: int) -> int:
    project = project_repository.get(target_id)
    if project != None :
        return target_id
    else:
        raise ProjectNotFound


def edit_project(target_id: int, name: str = None, description: str = None) -> Project:
    validate_project_id(target_id)
    return project_repository.update(target_id, name, description)   


def delete_project(target_id: int) -> None:
    validate_project_id(target_id)
    project_repository.delete(target_id)