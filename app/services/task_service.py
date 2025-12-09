from datetime import datetime, timedelta
from typing import Literal, TypedDict

#from repositories.repositories import *
from services.project_service import *


task_repository = TaskRepository()

class TaskDict(TypedDict):
    name: str
    description: str = "-"
    status: Literal["todo", "doing", "done"] = "todo"
    deadline: datetime = None
    project_id: int


def create_task(inputs: TaskDict) -> Task:
    id = inputs["project_id"]
    if validate_project_id(id) == None:
        raise ProjectNotFound
    length = len(project_repository.get(id).tasks)
    if length >= int(os.getenv("MAX_NUMBER_OF_TASK")) :
        raise MaximumNumberOfTasksReached
    return task_repository.add(inputs)


def list_tasks_by_project(id: int) -> List[Task]:
    if validate_project_id(id) == None :
        raise ProjectNotFound
    return project_repository.get(id).tasks


def validate_task_id(target_id: int) -> int:
    task = task_repository.get(target_id)
    if task != None :
        return target_id 
    else:
        raise TaskNotFound
    
def change_task_status(target_id: int, new_status: str) -> Task:
    validate_task_id(target_id)
    if new_status not in ("todo", "doing", "done"):
        raise TaskStatusIncorrect
    task = task_repository.get(target_id)
    inputs: TaskDict = {
        "name": task.name,
        "description": task.description,
        "status": new_status,
        "deadline": task.deadline,
        "project_id": task.project_id
    }
    return task_repository.update(target_id, inputs)



def edit_task(target_id: int, inputs: TaskDict) -> Task :
    validate_task_id(target_id)
    inputs["project_id"] = task_repository.get(target_id).project_id
    return task_repository.update(target_id, inputs)


def delete_task(target_id: int) -> None:
    validate_task_id(target_id)
    task_repository.delete(target_id)