# Task Manager

A task manager. Simple really.
This project exists to explore building a _usable CLI application_. It favours simplicity over... everything.

---

## Features

- Manage tasks
- Persistent storage using a plain .txt file

---

## Usage

| Running the program | Args |
|--|--|
| Run the program from the project directory | Can use these args |
| `python task_manager.py` | `-c COMMAND -t TASK` |
| Then the following commands can be completed by answering the two questions | Auto-fills questions |

---

## Commands

| Feature | Code | Description |
|--|--|--|
| Add task | `-c add -t taskName` | Creates task entitled -t |
| Remove task | `-c remove -t taskId` | Removes task -t |
| Complete task | `-c done -t taskId` | Completes task -t |
| list tasks | `-c list` | Prints the current tasklist |

---

## Storage

Tasks are stored locally in a plain text file:
```
tasks.txt
```
This means that the data is:
- Human-readable
- Easy to debug
- Easy to migrate/extend later
> Future versions may improve the formatting.

---

## Dependencies

- none beyond standard libraries
