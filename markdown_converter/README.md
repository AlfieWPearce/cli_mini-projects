# Mdview

`mdview` is a small, intentionally limited Markdown -> HTML converter written in Python.

It is **not** a full Markdown implementation.
It exists to explore parsing, text processing, and rendering pipelines in a controlled and understandable way.

The goal is clarity over completeness.

---

## Why this exists

Markdown looks simple, but it hides complexity:
- overlapping syntax
- ambiguous formatting
- nested structures
- stateful parsing (e.g. code blocks)

Rather than rely on the existing library, this project implements a **small, explicit subset** of Markdown to better understand:
- how text formats are parsed
- how structure emerges from plain text
- how HTML can be generated safely and predictably

---

## Planned & Current Supported Markdown Syntax

### Block Elements
- Headings
```md
# Heading 1
## Heading 2
### Heading 3
```
- Paragraphs
Any non-empty line not matching another rule
- Unordered lists
```md
- item
- item
```
- Ordered lists
```md
1. item 1
2. item 2
```
- Code blocks
```
`code here`
```
- Blockquotes
```md
> quoted text
```
- Lines
```md
---
```

### Inline Elements
```md
**bold**
*italic*
`code`
[text](url)
```

### Tables

```md
| Head 1 | Head 2 |
| ------ | ------ |
| cell 1 | cell 2 |
| row 2  | row 2  |
```

---

## Architecture Overview

The conversion will follow three clear stages
1. Read
- Load the `.md` file as UTF-8 text
- Split into lines
2. Parse
- Walks through lines sequentially
- Detect block structures
- Maintain minimal parser state (e.g. inside code block)
3. Render
- Convert parsed elements into HTML
- Wrap output in a full HTML document
- Apply a simple CSS stylesheet

---

## Example Usage

```
python mdview.py --input input.md --output output.html --css styles.css
```

> Converts `index.md` into a standalone HTML file `output.html` styled with `styles.css`
Using no arguments will default to input file being `input.md`, and output to `output.html`, linked to `styles.css`.

---
