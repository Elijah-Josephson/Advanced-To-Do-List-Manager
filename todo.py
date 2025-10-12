#defining classes project and task
from argparse import ArgumentParser, Namespace

from babel.dates import format_interval

MAX_NUMBER_OF_PROJECT = 50
class Status:

class Date:
    year : int
    month : int
    day : int
class Task():
    title : str
    deadline : Date
    description : str
    Status : todo | doing | done
class Project(name : str):
    Task list
    deadline date
    method >> create task
    method >> delete task
    method >> delete project
    method >> create project

parser = ArgumentParser()

parser.add_argument('add_proj', help='Add a project',
                    type= str)
adding verbose
parser.add_argument('-v', '--verbose', help = 'verbose description')
args : Namespace = parser.parse_args()

if args.add_proj:
    proj = new Project(name = args.add_proj)
if args.verbose:
    print(f'Project {args.add_proj} created succesfully!')