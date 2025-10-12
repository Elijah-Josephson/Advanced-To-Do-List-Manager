#defining classes project and task
from enum import Enum
from argparse import ArgumentParser, Namespace

from babel.dates import format_interval

MAX_NUMBER_OF_PROJECT = 50

class Stat(Enum):
    todo = 0
    doing = 1
    done = 2


class Date:
    year : int
    month : int
    day : int
class Task:
    def __init__(self, name : str):
        self.title = name
    deadline : Date
    description : str
    status : Stat
    def set_description(self, desc : str) -> None:
        self.description = desc
    def set_status(self, num : int) -> None:
        self.status = Stat(num)

class Project:
    def __init__(self, name : str):
        Project.name = name
    def set_description(self, desc : str) -> None:
        Project.description = desc
    tasks = []
    Deadline : Date
    def add_task(self, task_name : str):
        new_task = Task(task_name)

    # Need to define a destructor for Task
    #def delete task
    # Need to define a destructor for Project
    #delete project

parser = ArgumentParser()

parser.add_argument('add_proj', help='Add a project',
                    type= str)
#adding verbose
parser.add_argument('-v', '--verbose', help = 'verbose description')
args : Namespace = parser.parse_args()

if args.add_proj:
    proj = Project()
if args.verbose:
    print(f'Project {args.add_proj} created successfully!')
