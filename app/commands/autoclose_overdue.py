from datetime import datetime, date

def autoclose_overdue(task_service):
    now_date = date.today()
    tasks = task_service.list_overdue(now_date)
    for task in tasks:
        task_service.set_task_status_by_id(task.id, StatEnum.done)
        task_service.set_closed_at(task.id, datetime.utcnow())
    return len(tasks)
