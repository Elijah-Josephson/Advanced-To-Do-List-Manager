from enum import Enum
from argparse import ArgumentParser, Namespace

MAX_NUMBER_OF_PROJECT = 50

Projects_dict = dict()

class Stat(Enum):
    todo = 0
    doing = 1
    done = 2


class Date:
    def __init__(self , yy : int , mm : int , dd : int):
        self.year = yy
        self.month = mm
        self.day = dd
    year : int
    month : int
    day : int
    def __repr__(self) -> str:
        return f'{self.year}/{self.month}/{self.day}'


class Project:
    def __init__(self, name : str):
        self.name : str = name
        self.description : str = ""
        Projects_dict[name] = self
    def set_description(self, desc : str) -> None:
        Project.description = desc
    tasks = dict()
    Deadline : Date
    def add_task(self, task_name : str , task_desc : str,
                 task_ddline : Date) -> None:
        self.tasks[task_name] = {"description" : task_desc , "deadline" : task_ddline}
    def set_task_deadline(self, task_name : str , task_ddl : Date):
        self.tasks[task_name]["deadline"] = task_ddl
    def set_deadline(self, year : int , month : int , day : int):
        self.Deadline = Date(year , month, day)
    def set_task_stat(self , task_name : str , stat : int) -> None:
        self.tasks[task_name]["status"] = Stat(stat)
    def __del__(self):
        print(f'Object {self.name} is being deleted!')


def setup_parser():
    """Configures and returns the main argument parser."""
    parser = ArgumentParser(description="A simple project and task manager.")
    subparsers = parser.add_subparsers(dest='command',
                                        required = True, help = 'Available commands')
    #add_project command
    parser_add_project=subparsers.add_parser('add_project', help = 'Add a project')
    parser_add_project.add_argument('project_name', help = 'the name of the project to add'
                                    , type = str)
    args : Namespace = parser.parse_args()

    parser_delete_project=subparsers.add_parser('delete_project', help = 'Delete a project')
    parser_delete_project.add_argument('project_name' ,
                                       help = 'the name of the project to delete',
                                       type = str)

    parser_add_task = subparsers.add_parser('add_task',
                                            help = 'add task X to project Y : add_task Y X')
    parser_add_task.add_argument('project_name'
                                 , help = 'the name of the project to add task to')
    parser_add_task.add_argument('task_name'
                                 , help = 'the name of the task to add to project')

    parse_set_task_deadline = subparsers.add_parser('set_task_deadline'
                                                    , help = 'add deadline to task')
    parse_set_task_deadline.add_argument('project_name' , help = 'project name' , type = str)
    parse_set_task_deadline.add_argument('task_name', help='task name' , type = str)
    parse_set_task_deadline.add_argument('deadline_year', help='deadline year' , type = int)
    parse_set_task_deadline.add_argument('deadline_month', help='deadline month' , type = int)
    parse_set_task_deadline.add_argument('deadline_day', help='deadline day' , type = int)

    parser_set_project_description = subparsers.add_parser('set_project_description'
                                   ,help = 'set description for project')
    parser_set_project_description.add_argument('project_name'
                                                , help = 'project name'
                                                , type = str)
    parser_set_project_description.add_argument('description'
                                                , help = 'description for your project'
                                                , type = str)

    parser_set_task_stat = subparsers.add_parser('set_task_stat'
                                                 , help = 'set status for a task')
    parser_set_task_stat.add_argument('project_name' , help = 'project name'
                                      , type = str)
    parser_set_task_stat.add_argument('task_name', help='task name'
                                      , type = str)
    parser_set_task_stat.add_argument('status'
                                      , help='status : todo | doing | done'
                                      , type = str)

    parser_set_project_deadline = subparsers.add_parser('set_project_deadline'
                                                        ,help = 'set a deadline for a project')
    parser_set_project_deadline.add_argument('project_name'
                                             , help = 'project name'
                                             , type = str)
    parser_set_project_deadline.add_argument('task_name'
                                             , help = 'task name'
                                             , type = str)
    parser_set_project_deadline.add_argument('deadline_year'
                                             , help = 'deadline year'
                                             , type = int)
    parser_set_project_deadline.add_argument('deadline_month'
                                             , help = 'deadline month'
                                             , type = int)
    parser_set_project_deadline.add_argument('deadline_day'
                                             , help = 'deadline day'
                                             , type = int)

    parser_delete_task = subparsers.add_parser('delete_task'
                                               , help = 'delete a task')
    parser_delete_task.add_argument('project_name'
                                    , help = 'project name'
                                    , type = str)
    parser_delete_task.add_argument('task_name'
                                    , help = 'task name'
                                    , type = str)
    parser_set_task_description = subparsers.add_parser('set_task_description'
                                                        , help = 'set description for task')
    parser_set_task_description.add_argument('project_name'
                                             , help = 'project name'
                                             , type = str)
    parser_set_task_description.add_argument('task_name'
                                             , help = 'task name'
                                             , type = str)
    parser_set_task_description.add_argument('description'
                                             , help = 'description'
                                             , type = str)
    return parser

def main():
    parser = setup_parser()
    args = parser.parse_args()

    if args.command == 'set_task_deadline' :
        if args.projcet_name not in Projects_dict :
            print(f'Project with name {args.project_name} does not exist!')
        elif args.task_name not in Projects_dict[args.projcet_name].tasks :
            print(f'Task with name {args.task_name} already exists in project {args.project_name}!')
        else :
             ddl = Date(args.deadline_year , args.deadline_month , args.deadline_day)
             Projects_dict[args.project_name].set_task_deadline(args.task_name , ddl)
             print('Deadline set successfully!')

    if args.command == 'add_task':
        if args.project_name not in Projects_dict :
            print(f'project with name {args.project_name} does not exist!')
        elif args.project_name not in Projects_dict[args.project_name].tasks :
            Projects_dict[args.project_name].tasks[args.task_name]["description"] = "none"
            Projects_dict[args.project_name].tasks[args.task_name]["deadline"] = "00/00/00"
        else :
            print(f'Task with name {args.task_name} already exists in project {args.project_name}!')

    if args.command == 'add_project':
       if args.project_name not in Projects_dict:
            proj = Project(args.project_name)
            Projects_dict[args.project_name] = {proj}
            print("Success!")
       else:
            print(f'Project with name {args.project_name} already exists!')

    if args.command == 'delete_project':
        if args.project_name in Projects_dict :
            del Projects_dict[args.project_name]
            Projects_dict.pop(args.project_name)
            print("Success!")
        else :
            print(f'Project with name {args.project_name} does not exist!')

    if args.command == 'set_task_status' :
        if args.project_name not in Projects_dict :
            print(f'Project with name {args.project_name} does not exist!')
        elif args.task_name not in Projects_dict[args.project_name].tasks :
            print(f'Task with name {args.task_name} does not exist!')
        else :
            match args.status :
                case 'todo' :
                    Projects_dict[args.project_name].set_task_stat(args.task_name , 0)
                case 'doing':
                    Projects_dict[args.project_name].set_task_stat(args.task_name, 1)
                case 'done':
                    Projects_dict[args.project_name].set_task_stat(args.task_name, 2)

    if args.command == 'set_project_deadline' :
        if args.project_name not in Projects_dict :
            print(f'Project with name {args.project_name} does not exist!')
        elif args.task_name not in Projects_dict[args.project_name].task :
            print(f'Task with name {args.task_name} does not exist!')
        else :
            ddl = Date(args.deadline_year , args.deadline_month , args.deadline_day)
            Projects_dict[args.project_name].set_deadline(ddl)

    if args.command == 'set_project_description' :
        if args.project_name not in Projects_dict :
            print(f'Project with name {args.project_name} does not exist!')
        else :
            Projects_dict[args.project_name].set_description(args.description)

    if args.command == 'delete_task' :
        if args.project_name not in Projects_dict :
            print(f'Project with name {args.project_name} does not exist!')
        elif args.task_name not in Projects_dict[args.project_name].tasks :
            print(f'Task with name {args.task_name} does not exist!')
        else :
            Projects_dict[args.project_name].tasks.pop(args.task_name)

    if args.command == 'set_task_description' :
        if args.project_name not in Projects_dict :
            print(f'Project with name {args.project_name} does not exist!')
        elif args.task_name not in Projects_dict[args.project_name].tasks :
            print(f'Task with name {args.task_name} does not exist!')
        else :
            Projects_dict[args.project_name].set_task_description(args.task_name , args.description)


if __name__ == "__main__":
    main()