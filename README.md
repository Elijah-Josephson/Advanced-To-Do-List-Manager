# Advanced-To-Do-List-Manager
TL;DR: Small, dependency-free Python app that manages projects and tasks in memory. Starts an interactive prompt by default (REPL). Also supports one-shot CLI invocations. No persistence — state is lost when the program exits. Use it for quick demos, learning, or extend it later to add persistence.

Quick facts

Language: Python 3.8+ (typing, f-strings)

Mode: Interactive REPL (default) and one-shot CLI

Storage: In-memory only (no DB / file by default)

Max projects: MAX_NUMBER_OF_PROJECT = 50 (adjustable in code)

Main file: p.py

Why this repo exists

You want a tiny, robust project/task manager you can run locally to:

experiment with CLI/REPL patterns,

learn Python OOP and argparse,

use as a base for adding persistence, UI, tests, or deployment.

This implementation intentionally keeps the design minimal and predictable so it’s easy to extend.

Features

Create / delete projects

Add / delete tasks inside projects

Set deadlines (project / task) and descriptions

Change task status (todo, doing, done)

Inspect projects and tasks (list_projects, show_project)

Interactive prompt with command parsing (handles quotes)

Still supports running single commands directly from shell (backwards compatible)
