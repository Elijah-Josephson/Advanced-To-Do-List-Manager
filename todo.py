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
class Project:
    Task list
    deadline date
    method >> create task
    method >> delete task
    method >> delete project
    method >> create project

parser = ArgumentParser()

parser.add_argument('add_proj', help='Add a project',
                    type= str)
# adding verbose
#parser.add_argument('-v', '--verbose', action=verb())
args : Namespace = parser.parse_args()

