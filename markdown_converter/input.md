# mdview Test Document

This file exists to test the **mdview** Markdown to HTML converter.
If something looks wrong in the output, the parser is probably lying to you.

---

## Basic Text

This is a normal paragraph.  
It should be wrapped in a ***<p>*** tag and flow like sensible prose.

Blank lines separate paragraphs.

---

## Inline Formatting

You should see **bold text**, *italic text*, and `inline code` rendered correctly.

Formatting can appear in the middle of a sentence without breaking anything.

Check out [Example Link](https://example.com/) for search.

---

## Headings

### Heading Level 3

Headings should stack neatly and never skip levels unless the input does.

---

## Lists

- First item
- Second item with **bold**
- Third item with `code`
- Fourth item

1. Ordered first item
2. Second item with *italics*
3. Third item is a thing too

Text after a list should not accidentally become part of it.

---

## Code Block

```python
def hello(name):
    print(f'Hello, {name}')

hello(world)
```

---

## Quotes work too

> This is a quote
> Written by a certain AlfieWPearce

---

## And so do tables

| Name | Age | Role |
| ---- | --- | ---- |
| Alfie | ... | Wizard |
| Vim | ∞ | Editor |
|* **Inline*** | `code` | ~Strike-through~ |
