from services import *


while(True):
    print("\nHi. What can I do for you?")
    print("""\t Create new project-> 1
         See list of all existing projects-> 2
         Edit details of a project-> 3
         Delete a project-> 4
         Create a new task-> 5
         List all tasks of a project-> 6
         Change status of a task-> 7
         Edit details of a task-> 8
         Delete a task-> 9""")
    command = input()
    match command:
        case "1":
            new_project = create_project()
        case "2":
            list_projects()
        case "3":
            edit_project()
        case "4":
            delete_project()
        case "5":
            add_task()
        case "6":
            project = search_project_by_id()
            list_tasks(project)
        case "7":
            change_task_status()
        case "8":
            edit_task()
        case "9":
            delete_task()
        case _:
            pass