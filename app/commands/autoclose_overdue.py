import datetime

from repositories import *

def close_overdue():
    scheduler_repository = TaskRepository
    for task in scheduler_repository.get_all():
        if task.deadline < datetime.now() :
            inputs : TaskDict = {
                "name" = task.name,
                "description" = task.description,
                "status" = "done",
                "deadline" = task.deadline,
                "project_id" = task.project_id
            }
            scheduler_repository.update(task.id, inputs)