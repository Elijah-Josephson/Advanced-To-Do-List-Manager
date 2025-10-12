#defining classes project and task
from argparse import ArgumentParser, Namespace

from babel.dates import format_interval

MAX_NUMBER_OF_PROJECT = 50
class Date:
    year : int
    month : int
    day : int
class Task:
    def __init__(self, name : str):
        self.title = name
    deadline : Date
    description : str
    def set_description(self, desc : str):
        self.description = desc
    def set_status(self, num : int):
        self.stat = num
class Project:
    def __init__(self, name : str):
        Project.name = name
    def set_description(self, desc : str) -> None:
        Project.description = desc
    tasks = []
    Deadline : Date
    def Add_Task(self, taskname : str):
        new_task = Task()
    method >> create task
    method >> delete task
    method >> delete project
    method >> create project

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
