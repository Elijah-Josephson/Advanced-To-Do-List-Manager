#defining classes project and task
from enum import Enum
from argparse import ArgumentParser, Namespace

MAX_NUMBER_OF_PROJECT = 50

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

class Project:
    def __init__(self, name : str):
        Project.name = name
    def set_description(self, desc : str) -> None:
        Project.description = desc
    Deadline : Date
    def add_task(self, task_name : str):
        new_task = Task(task_name)
        tasks_list.append(new_task)
    def set_deadline(self, year : int , month : int , day : int):
        self.Deadline = Date(year , month, day)
    # Need to define a destructor for Task
    #def delete task
    # Need to define a destructor for Project
    #delete project
    tasks = {}
    #task attrs name : description, deadline, status
parser = ArgumentParser()

parser.add_argument('add_proj', help='Add a project',
                    type= str)
#adding verbose
parser.add_argument('-v', '--verbose', help = 'verbose description')
args : Namespace = parser.parse_args()

if args.add_proj:
    proj = Project(args.add_proj)
if args.verbose:
    print(f'Project {args.add_proj} created successfully!')
