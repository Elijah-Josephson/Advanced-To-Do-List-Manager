from enum import Enum
from argparse import ArgumentParser, Namespace

MAX_NUMBER_OF_PROJECT = 50

Projects = dict()

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
        Projects[name] = self
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
