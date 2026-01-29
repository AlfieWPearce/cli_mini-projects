# Zettelkasten-style note system

A note taking system inspired by the Zettelkasten method.
The goal for these types of notes is not to store information but to think in small, connected ideas.

---

## Philosophy

1. Notes are atomic
    Each note contains a single idea or thought
2. Notes are linked, not categorised
    Relations between ideas are expressed explicitly through links, not folders.
3. Structure emerges through use
    Connections are discovered through searching and backlinks - and thus not imposed.

---

## What this tool is (and is not)

This tool is:
- A plain-text note system
- CLI-first
- Search-driven
- Long-term and tool-agnostic
This tool is not:
- A task manager
- A wiki generator
- A database-backed app
- A knowledge graph engine
- A replacement for thinking

---

## Note structure

> Each note is self-contained and readable on its own
A typical note contains:
- ID - derived from filename
- Title - short and descriptive
- Body - the idea (one and only)
- Links - references to other notes by ID
- Optional tags and/or sources

---

## Hierarchy

By default, the project uses the following layout:
```
note.py  "the script
notes\   "the dumb storage
| ID.txt "all notes are stored as ID.txt
...
```

---

## Linking notes

Notes are linked by referencing other note IDs in plain text

Links are:
- Explicit
- Human-written
- Stored directly in the note body

This tool does not store relationships separately.
All connections are derived by scanning files, allowing:
- Backlinks
- Contextual navigation
- Organic idea growth

---

## Navigation Model

Notes are navigated through:
- Full-text search
- ID-based lookup
- Following links
- Viewing backlinks

> Searching is the main way ideas are rediscovered, mirroring how memory works

---

## Core commands

This tool supports a small set of core actions:
- *Create* a new note
- *Open* an existing note
- *Search* across all notes
- *Show backlinks* to a note
- *List or Explore* notes (optionally random)

---

## Backlinks

Backlinks are generated dynamically.
When viewing a note, the tool scans all other notes to find references to its ID and displays them.
No index is stored, no relationship is cached.
This keeps the system flexible and resistant to corruption

---

## Workflow

A typical workflow looks like:
1. Encounter an interesting idea
2. Create a new note
3. Write the idea clearly and concisely in your own words
4. Link it to existing notes where relevant
5. Revisit notes later through search or backlinks

Notes are rarely deleted and typically edited only to improve clarity.

---

## Design constraints

This project intentionally avoids:
- Folders / Nested structures
- Automatic categorisation
- Silent note modification
- Hidden metadata
- Complex configuration

---

## Dependencies

- none beyond standard libraries
