from enum import Enum
from argparse import ArgumentParser, Namespace

from chardet.cli.chardetect import description_of

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
    def __repr__(self):
        print(f'{self.year}/{self.month}/{self.day}')

class Project:
    def __init__(self, name : str):
        self.name = name
        Projects_dict[name] = self
    def set_description(self, desc : str) -> None:
        Project.description = desc
    tasks = dict()
    description : str
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
#parser = ArgumentParser()
def setup_parser():
    """Configures and returns the main argument parser."""
    parser = ArgumentParser(description="A simple project and task manager.")
    #📁
    subparsers = parser.add_subparsers(dest='command',
                                        required = True, help = 'Available commands')
    #add_project command
    parser_add_project=subparsers.add_parser('add_project', help = 'Add a project')
    parser_add_project.add_argument('project_name', help = 'the name of the project to add'
                                    , type = str)
    #verbose argument
    parser.add_argument('-v', '--verbose', help = 'verbose description')

    args : Namespace = parser.parse_args()

    if args.command == 'add_project':
        if args.project_name not in Projects_dict :
            proj = Project(args.project_name)
            Projects_dict[args.project_name] = {proj}
            print("Success!")
        else :
            print(f'Project with name {args.project_name} already exists!')
#    if args.add_proj.verbose:
#        print(f'Project {args.add_project} created successfully!')

    parser_delete_project=subparsers.add_parser('delete_project', help = 'Delete a project')
    parser_delete_project.add_argument('project_name' ,
                                       help = 'the name of the project to delete',
                                       type = str)
    if args.command == 'delete_project':
        if args.project_name in Projects_dict :
            del Projects_dict[args.project_name]
            Projects_dict.pop(args.project_name)
            print("Success!")
        else :
            print(f'Project with name {args.project_name} doesn\'t exist!')
    #if args.delete_project.verbose:
    #    print(f'Project {args.add_project} deleted successfully!')


    parser_add_task = subparsers.add_parser('add_task',
                                            help = 'add task X to project Y : add_task Y X')
    parser_add_task.add_argument('project_name'
                                 , help = 'the name of the project to add task to')
    parser_add_task.add_argument('task_name'
                                 , help = 'the name of the task to add to project')

    if args.command == 'add_task':
        if args.project_name not in Projects_dict :
            print(f'project with name {args.project_name} does not exist!')
        else :
            if args.project_name not in Projects_dict[args.project_name].tasks :
                Projects_dict[args.project_name].tasks[args.task_name]["description"] = "none"
                Projects_dict[args.project_name].tasks[args.task_name]["deadline"] = "00/00/00"
            else :
                print(f'Task with name {args.task_name} already exists in project {args.project_name}!')
    # verbose?

    parse_set_task_deadline = subparsers.add_parser('set_task_deadline'
                                                    , help = 'add deadline to task')
    parse_set_task_deadline.add_argument('project_name' , help = 'project name' , type = str)
    parse_set_task_deadline.add_argument('task_name', help='task name' , type = str)
    parse_set_task_deadline.add_argument('deadline_year', help='deadline year' , type = int)
    parse_set_task_deadline.add_argument('deadline_month', help='deadline month' , type = int)
    parse_set_task_deadline.add_argument('deadline_day', help='deadline day' , type = int)

    if args.command == 'set_task_deadline' :
        if args.projcet_name not in Projects_dict :
            pass
        else :
            if args.task_name not in Projects_dict[args.projcet_name].tasks :
                pass
            else :
                ddl = Date(args.deadline_year , args.deadline_month , args.deadline_day)
                Projects_dict[args.project_name].set_task_deadline(args.task_name , ddl)
                print('Deadline set successfully!')
