from fastapi import FastAPI , status, HTTPException
from pydantic import BaseModel
from typing import Optional

from services import *


class ProjectData(BaseModel):
    name: str
    description: Optional[str] = None

class TaskData(BaseModel):
    name: str
    description: Optional[str] = None
    status: Literal["todo", "doing", "done"] = "todo"
    deadline: Optional[datetime] = None
    project_id: int


app = FastAPI()


@app.post("/projects", status_code = status.HTTP_201_CREATED)
def api_create_project(inputs: ProjectData):
    try:
        project = create_project(inputs.name, inputs.description)
        response = {"id: " : project.id,
                    "name: " : project.name,
                    "description: " : project.description}
        return response
    except MaximumNumberOfProjectsReached:
        raise HTTPException(status_code = status.HTTP_406_NOT_ACCEPTABLE, detail="Maximum number of projects reached") 
    except ProjectNameAlreadyExists:
        raise HTTPException(status_code = status.HTTP_406_NOT_ACCEPTABLE, detail="A Project with this name already exists")


@app.get("/projects/all",status_code = status.HTTP_200_OK)
def api_list_projects():
    try:
        projects = {}
        for project in list_projects():
            projects[project.id] = {
                "name" : project.name,
                "description" : project.description
            }
        return projects
    except:
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@app.patch("/projects/{target_id}",status_code = status.HTTP_200_OK)
def api_edit_project(target_id: int, inputs: ProjectData):
    try:
        project = edit_project(target_id = target_id, name = inputs.name,
            description = inputs.description)
        response = {"id: " : project.id,
                    "name: " : project.name,
                    "description: " : project.description}
        return response
    except ProjectNotFound:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Project not found")


@app.delete("/projects/{target_id}", status_code = status.HTTP_200_OK)
def api_delete_project(target_id: int):
    try:
        delete_project(target_id)
        return {"message: " : "Project deleted successfully"}
    except ProjectNotFound:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Project not found")
    

@app.post("/tasks", status_code = status.HTTP_201_CREATED)
def api_create_task(inputs: TaskData):
    try:
        inputs2: TaskDict = {
            "name" : inputs.name,
            "description" : inputs.description,
            "status" : inputs.status,
            "deadline" : inputs.deadline,
            "project_id" : inputs.project_id
        }
        task = create_task(inputs2)
        response = {"id: " : task.id,
            "name" : task.name,
            "description" : task.description,
            "status" : task.status,
            "deadline" : task.deadline,
            "project_id" : task.project_id }
        return response
    except ProjectNotFound:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Project not found")
    except:
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.get("/projects/{target_id}/tasks/all",status_code = status.HTTP_200_OK)
def api_list_tasks_by_project(target_id: int):
    try:
        task_list = list_tasks_by_project(target_id)
        tasks = {}
        for task in task_list:
            tasks[task.id] = {
                "name" : task.name,
                "description" : task.description,
                "status" : task.status,
                "deadline" : task.deadline,
                "project_id" : task.project_id }
        return tasks
    except:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Project not found")
    

@app.patch("/tasks/{target_id}/{new_status}", status_code=status.HTTP_200_OK)
def api_change_task_status(target_id: int, new_status: Literal["todo", "doing", "done"]):
    try:
        task = change_task_status(target_id, new_status)
        return {
            "id": task.id,
            "name": task.name,
            "description": task.description,
            "status": task.status,
            "deadline": task.deadline,
            "project_id": task.project_id
        }
    except TaskNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    

@app.patch("/tasks/{target_id}", status_code = status.HTTP_200_OK)
def api_edit_task(target_id: int, inputs: TaskData):
    try:
        inputs2: TaskDict = {
            "name" : inputs.name,
            "description" : inputs.description,
            "status" : inputs.status,
            "deadline" : inputs.deadline,
            "project_id" : inputs.project_id
        }
        task = edit_task(target_id = target_id, inputs = inputs2)
        response = {"id: " : task.id,
            "name" : task.name,
            "description" : task.description,
            "status" : task.status,
            "deadline" : task.deadline,
            "project_id" : task.project_id }
        return response
    except TaskNotFound:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Task not found")
    

@app.delete("/tasks/{target_id}", status_code = status.HTTP_200_OK)
def api_delete_task(target_id: int):
    try:
        delete_task(target_id)
        return {"message: " : "Task deleted successfully"}
    except TaskNotFound:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Task not found")