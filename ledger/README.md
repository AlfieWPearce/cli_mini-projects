# Ledger

A small, terminal-based daily ledger for notes and tasks.
> An upgrade of the task manager that is also within this repository.

Ledger is designed to be fast, quiet, and durable - a plain-text tool you can use every day.
Each day has its own file. Tasks can be added and completed. Notes are timestamped. Nothing is hidden.

---

## Features

- Timestamped notes
- Simple task tracking
- Task completion
- Plain-text storage (one file per day)
- Zero dependencies

---

## Usage

> Anywhere that <> is used denotes your own input
```bash
ledger.py note <Revise Magnetism>
ledger.py task <Maths Homework>
ledger.py complete <Maths Homework>
ledger.py show
ledger.py tasks
ledger.py help
```

If no command is provided, `help` is shown.

---

## File Format

Each day is stored as a text file:
```
2026-02-05
[09:12] NOTE  Revised magnetism
[09:40]  [ ]  Maths homework
[10:15]  [X]  Maths homework
```

---

Future Ideas
- Task statistics
- Date selection
- Flags for filtering
- Shell completion
