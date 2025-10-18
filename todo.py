from __future__ import annotations
import shlex
import sys
from enum import Enum
from argparse import ArgumentParser, Namespace
from typing import Dict, Optional

MAX_NUMBER_OF_PROJECT = 50

PROJECTS: Dict[str, "Project"] = {}

class Stat(Enum):
    todo = 0
    doing = 1
    done = 2


class Date:
    def __init__(self , yy : int , mm : int , dd : int):
        self.year : int = yy
        self.month : int = mm
        self.day : int = dd

    def __repr__(self) -> str:
        return f"{self.year:04d}/{self.month:02d}/{self.day:02d}"


class Project:
    def __init__(self, name : str):
        self.name : str = name
        self.description : str = ""
        PROJECTS[name] = self
        self.deadline: Optional[Date] = None
        self.tasks: Dict[str, Dict[str, object]] = {}

    def set_description(self, desc : str) -> None:
        Project.description = desc

    def add_task(self, task_name: str, task_desc: str = "none", task_ddline: Optional[Date] = None) -> None:
        if task_name in self.tasks:
            raise KeyError(f"Task '{task_name}' already exists in project '{self.name}'.")
        self.tasks[task_name] = {
            "description": task_desc,
            "deadline": task_ddline,
            "status": Stat.todo,
        }

    def set_task_deadline(self, task_name: str, task_ddl: Date) -> None:
        if task_name not in self.tasks:
            raise KeyError(f"Task '{task_name}' does not exist in project '{self.name}'.")
        self.tasks[task_name]["deadline"] = task_ddl

    def set_deadline(self, year_or_date, month: int = None, day: int = None) -> None:
        if isinstance(year_or_date, Date):
            self.deadline = year_or_date
        else:
            if month is None or day is None:
                raise ValueError("Provide year, month and day to set project deadline.")
            self.deadline = Date(int(year_or_date), int(month), int(day))

    def set_task_stat(self, task_name: str, stat: object) -> None:
        if task_name not in self.tasks:
            raise KeyError(f"Task '{task_name}' does not exist in project '{self.name}'.")
        if isinstance(stat, Stat):
            self.tasks[task_name]["status"] = stat
            return
        # accept string names or integer codes
        if isinstance(stat, str):
            try:
                self.tasks[task_name]["status"] = Stat[stat]
            except KeyError:
                raise ValueError("Invalid status string. Use 'todo'|'doing'|'done'.")
        elif isinstance(stat, int):
            self.tasks[task_name]["status"] = Stat(stat)
        else:
            raise ValueError("Invalid status type.")

    def set_task_description(self, task_name: str, description: str) -> None:
        if task_name not in self.tasks:
            raise KeyError(f"Task '{task_name}' does not exist in project '{self.name}'.")
        self.tasks[task_name]["description"] = description

    def delete_task(self, task_name: str) -> None:
        if task_name not in self.tasks:
            raise KeyError(f"Task '{task_name}' does not exist in project '{self.name}'.")
        self.tasks.pop(task_name)

    def __repr__(self) -> str:
        return f"Project(name={self.name!r}, tasks={len(self.tasks)})"

    def __del__(self):
        print(f'Object {self.name!r} is being deleted!')


def setup_parser() -> ArgumentParser:
    """Configures and returns the main argument parser."""
    parser = ArgumentParser(description="A simple project and task manager.")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    # add_project command
    parser_add_project = subparsers.add_parser("add_project", help="Add a project")
    parser_add_project.add_argument("project_name", help="the name of the project to add", type=str)

    parser_delete_project = subparsers.add_parser("delete_project", help="Delete a project")
    parser_delete_project.add_argument("project_name", help="the name of the project to delete", type=str)

    parser_add_task = subparsers.add_parser("add_task", help="Add task X to project Y: add_task Y X")
    parser_add_task.add_argument("project_name", help="the name of the project to add task to", type=str)
    parser_add_task.add_argument("task_name", help="the name of the task to add to project", type=str)

    parser_set_task_deadline = subparsers.add_parser("set_task_deadline", help="Add deadline to task")
    parser_set_task_deadline.add_argument("project_name", help="project name", type=str)
    parser_set_task_deadline.add_argument("task_name", help="task name", type=str)
    parser_set_task_deadline.add_argument("deadline_year", help="deadline year", type=int)
    parser_set_task_deadline.add_argument("deadline_month", help="deadline month", type=int)
    parser_set_task_deadline.add_argument("deadline_day", help="deadline day", type=int)

    parser_set_project_description = subparsers.add_parser("set_project_description", help="Set description for project")
    parser_set_project_description.add_argument("project_name", help="project name", type=str)
    parser_set_project_description.add_argument("description", help="description for your project", type=str)

    parser_set_task_status = subparsers.add_parser("set_task_status", help="Set status for a task")
    parser_set_task_status.add_argument("project_name", help="project name", type=str)
    parser_set_task_status.add_argument("task_name", help="task name", type=str)
    parser_set_task_status.add_argument("status", help="status : todo | doing | done", type=str)

    parser_set_project_deadline = subparsers.add_parser("set_project_deadline", help="Set a deadline for a project")
    parser_set_project_deadline.add_argument("project_name", help="project name", type=str)
    parser_set_project_deadline.add_argument("deadline_year", help="deadline year", type=int)
    parser_set_project_deadline.add_argument("deadline_month", help="deadline month", type=int)
    parser_set_project_deadline.add_argument("deadline_day", help="deadline day", type=int)

    parser_delete_task = subparsers.add_parser("delete_task", help="Delete a task")
    parser_delete_task.add_argument("project_name", help="project name", type=str)
    parser_delete_task.add_argument("task_name", help="task name", type=str)

    parser_set_task_description = subparsers.add_parser("set_task_description", help="Set description for task")
    parser_set_task_description.add_argument("project_name", help="project name", type=str)
    parser_set_task_description.add_argument("task_name", help="task name", type=str)
    parser_set_task_description.add_argument("description", help="description", type=str)

    return parser

def process_args(args: Namespace) -> None:
    """Execute a single parsed command (args)."""
    try:
        if args.command == "set_task_deadline":
            if args.project_name not in PROJECTS:
                print(f"Project with name {args.project_name} does not exist!")
            elif args.task_name not in PROJECTS[args.project_name].tasks:
                print(f"Task with name {args.task_name} does not exist in project {args.project_name}!")
            else:
                ddl = Date(args.deadline_year, args.deadline_month, args.deadline_day)
                PROJECTS[args.project_name].set_task_deadline(args.task_name, ddl)
                print("Deadline set successfully!")

        elif args.command == "add_task":
            if args.project_name not in PROJECTS:
                print(f"Project with name {args.project_name} does not exist!")
            else:
                project = PROJECTS[args.project_name]
                if args.task_name in project.tasks:
                    print(f"Task with name {args.task_name} already exists in project {args.project_name}!")
                else:
                    project.add_task(args.task_name)
                    print("Task added successfully!")

        elif args.command == "add_project":
            if args.project_name in PROJECTS:
                print(f"Project with name {args.project_name} already exists!")
            elif len(PROJECTS) >= MAX_NUMBER_OF_PROJECT:
                print(f"Cannot create project: reached MAX_NUMBER_OF_PROJECT ({MAX_NUMBER_OF_PROJECT}).")
            else:
                proj = Project(args.project_name)
                PROJECTS[args.project_name] = proj
                print("Project created successfully!")

        elif args.command == "delete_project":
            if args.project_name in PROJECTS:
                del PROJECTS[args.project_name]
                print("Project deleted successfully!")
            else:
                print(f"Project with name {args.project_name} does not exist!")

        elif args.command == "set_task_status":
            if args.project_name not in PROJECTS:
                print(f"Project with name {args.project_name} does not exist!")
            elif args.task_name not in PROJECTS[args.project_name].tasks:
                print(f"Task with name {args.task_name} does not exist!")
            else:
                status_str = args.status
                try:
                    PROJECTS[args.project_name].set_task_stat(args.task_name, status_str)
                    print("Task status updated successfully!")
                except Exception as exc:
                    print(f"Failed to set status: {exc}")

        elif args.command == "set_project_deadline":
            if args.project_name not in PROJECTS:
                print(f"Project with name {args.project_name} does not exist!")
            else:
                ddl = Date(args.deadline_year, args.deadline_month, args.deadline_day)
                PROJECTS[args.project_name].set_deadline(ddl)
                print("Project deadline set successfully!")

        elif args.command == "set_project_description":
            if args.project_name not in PROJECTS:
                print(f"Project with name {args.project_name} does not exist!")
            else:
                PROJECTS[args.project_name].set_description(args.description)
                print("Project description updated successfully!")

        elif args.command == "delete_task":
            if args.project_name not in PROJECTS:
                print(f"Project with name {args.project_name} does not exist!")
            elif args.task_name not in PROJECTS[args.project_name].tasks:
                print(f"Task with name {args.task_name} does not exist!")
            else:
                PROJECTS[args.project_name].delete_task(args.task_name)
                print("Task deleted successfully!")

        elif args.command == "set_task_description":
            if args.project_name not in PROJECTS:
                print(f"Project with name {args.project_name} does not exist!")
            elif args.task_name not in PROJECTS[args.project_name].tasks:
                print(f"Task with name {args.task_name} does not exist!")
            else:
                PROJECTS[args.project_name].set_task_description(args.task_name, args.description)
                print("Task description updated successfully!")

        elif args.command == "list_projects":
            if not PROJECTS:
                print("No projects available.")
            else:
                for name, proj in PROJECTS.items():
                    print(f"- {name}: {len(proj.tasks)} tasks")

        elif args.command == "show_project":
            if args.project_name not in PROJECTS:
                print(f"Project with name {args.project_name} does not exist!")
            else:
                p = PROJECTS[args.project_name]
                print(f"Project: {p.name}")
                print(f"  Description: {p.description!r}")
                print(f"  Deadline: {p.deadline!r}")
                print(f"  Tasks ({len(p.tasks)}):")
                for tname, meta in p.tasks.items():
                    print(f"   - {tname}: desc={meta['description']!r}, deadline={meta['deadline']!r}, status={meta['status'].name}")

        else:
            print("Unknown command. Use 'help'.")

    except Exception as exc:
        print(f"Error: {exc}")

def main():
    parser = setup_parser()
    args: Namespace = parser.parse_args()

    try:
        if args.command == "set_task_deadline":
            if args.project_name not in PROJECTS:
                print(f"Project with name {args.project_name} does not exist!")
            elif args.task_name not in PROJECTS[args.project_name].tasks:
                print(f"Task with name {args.task_name} does not exist in project {args.project_name}!")
            else:
                ddl = Date(args.deadline_year, args.deadline_month, args.deadline_day)
                PROJECTS[args.project_name].set_task_deadline(args.task_name, ddl)
                print("Deadline set successfully!")

        elif args.command == "add_task":
            if args.project_name not in PROJECTS:
                print(f"Project with name {args.project_name} does not exist!")
            else:
                project = PROJECTS[args.project_name]
                if args.task_name in project.tasks:
                    print(f"Task with name {args.task_name} already exists in project {args.project_name}!")
                else:
                    project.add_task(args.task_name)
                    print("Task added successfully!")

        elif args.command == "add_project":
            if args.project_name in PROJECTS:
                print(f"Project with name {args.project_name} already exists!")
            elif len(PROJECTS) >= MAX_NUMBER_OF_PROJECT:
                print(f"Cannot create project: reached MAX_NUMBER_OF_PROJECT ({MAX_NUMBER_OF_PROJECT}).")
            else:
                proj = Project(args.project_name)
                PROJECTS[args.project_name] = proj
                print("Project created successfully!")

        elif args.command == "delete_project":
            if args.project_name in PROJECTS:
                del PROJECTS[args.project_name]
                print("Project deleted successfully!")
            else:
                print(f"Project with name {args.project_name} does not exist!")

        elif args.command == "set_task_status":
            if args.project_name not in PROJECTS:
                print(f"Project with name {args.project_name} does not exist!")
            elif args.task_name not in PROJECTS[args.project_name].tasks:
                print(f"Task with name {args.task_name} does not exist!")
            else:
                status_str = args.status
                try:
                    PROJECTS[args.project_name].set_task_stat(args.task_name, status_str)
                    print("Task status updated successfully!")
                except Exception as exc:
                    print(f"Failed to set status: {exc}")

        elif args.command == "set_project_deadline":
            if args.project_name not in PROJECTS:
                print(f"Project with name {args.project_name} does not exist!")
            else:
                ddl = Date(args.deadline_year, args.deadline_month, args.deadline_day)
                PROJECTS[args.project_name].set_deadline(ddl)
                print("Project deadline set successfully!")

        elif args.command == "set_project_description":
            if args.project_name not in PROJECTS:
                print(f"Project with name {args.project_name} does not exist!")
            else:
                PROJECTS[args.project_name].set_description(args.description)
                print("Project description updated successfully!")

        elif args.command == "delete_task":
            if args.project_name not in PROJECTS:
                print(f"Project with name {args.project_name} does not exist!")
            elif args.task_name not in PROJECTS[args.project_name].tasks:
                print(f"Task with name {args.task_name} does not exist!")
            else:
                PROJECTS[args.project_name].delete_task(args.task_name)
                print("Task deleted successfully!")

        elif args.command == "set_task_description":
            if args.project_name not in PROJECTS:
                print(f"Project with name {args.project_name} does not exist!")
            elif args.task_name not in PROJECTS[args.project_name].tasks:
                print(f"Task with name {args.task_name} does not exist!")
            else:
                PROJECTS[args.project_name].set_task_description(args.task_name, args.description)
                print("Task description updated successfully!")

        else:
            print("Unknown command. Use -h for help.")

    except Exception as exc:
        print(f"Error: {exc}")

if __name__ == "__main__":
    main()