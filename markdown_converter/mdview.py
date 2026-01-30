from pathlib import Path
import re
import argparse

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>mdview</title>
    <link rel="stylesheet" href="{css_path}">
</head>
<body>
<main class="markdown-body">
{content}
</main>
</body>
</html>
"""

def is_table_header(lines, i):
    if i + 1 >= len(lines):
        return False
    return (
        lines[i].startswith('|')
        and set(lines[i + 1].replace('|', '').strip()) <= {'-', ' '}
    )
def split_row(line):
    return [
        cell.strip()
        for cell in line.strip().strip('|').split('|')
    ]
def parse_table(lines, i):
    header = split_row(lines[i])
    i += 2 # Skip header & seperator
    rows = []

    while i < len(lines) and lines[i].startswith('|'):
        rows.append(split_row(lines[i]))
        i += 1

    return {
        'type': 'table',
        'text': '',
        'header': header,
        'rows': rows
    }, i


def is_blockquote(line: str) -> bool:
    return line[:2] == '> '

def is_code_fence(line: str) -> bool:
    return line[:3] == '```'

def is_ul_item(line: str) -> bool:
    return line[:2] == '- ' or line[:2] == '* '

def is_ol_item(line: str) -> bool:
    return (
        len(line) >= 3
        and line[0].isdigit()
        and line[1] == '.'
        and line[2] == ' '
    )

def parse_markdown(md_text: str) -> str:
    lines = md_text.splitlines()
    i = 0
    blocks = []

    while i < len(lines):
        line = lines[i]

        if not line.strip():
            i += 1
            continue
        elif is_table_header(lines, i):
            block, i = parse_table(lines, i)
            blocks.append(block)
            continue
        elif is_blockquote(line):
            quote_lines = []
            while i < len(lines) and is_blockquote(lines[i]):
                stripped = lines[i][1:].lstrip()
                quote_lines.append(stripped)
                i += 1

            blocks.append({
                'type': 'blockquote',
                'text': '',
                'lines': quote_lines
            })
            continue
        elif is_code_fence(line):
            fence = line.strip()
            lang = fence[3:].strip() or None

            i += 1
            code_lines = []

            while i < len(lines) and not is_code_fence(lines[i]):
                code_lines.append(lines[i])
                i += 1

            if i < len(lines) and is_code_fence(lines[i]):
                i += 1

            blocks.append({
                'type': 'code',
                'text': '',
                'lang': lang,
                'lines': code_lines
            })
            continue
        elif is_ul_item(line):
            list_items = []
            while i < len(lines) and is_ul_item(lines[i]):
                list_items.append(lines[i][2:])
                i += 1

            blocks.append({
                'type':'ul',
                'text':'',
                'items':list_items
            })
            continue
        elif is_ol_item(line):
            list_items = []
            while i < len(lines) and is_ol_item(lines[i]):
                list_items.append(lines[i][3:])
                i += 1

            blocks.append({
                'type':'ol',
                'text':'',
                'items':list_items
            })
            continue
        elif line == '---':
            line_type = '---'
        elif line[:3] == '###':
            line_type = '###'
            line = line[4:]
        elif line[:2] == '##':
            line_type = '##'
            line = line[3:]
        elif line[:1] == '#':
            line_type = '#'
            line = line[2:]
        else:
            line_type = 'p'
        blocks.append({
            'type':line_type,
            'text':line
        })
        i += 1
        
    return blocks

def escape_html(text: str) -> str:
    return (
        text.replace('&', '&amp')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
    )

def render_inline(text: str) -> str:
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*\*([^\*]+)\*\*\*", r"<strong><em>\1</em></strong>", text)
    text = re.sub(r"\*\*([^\*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*([^\*]+)\*", r"<em>\1</em>", text)
    text = re.sub(r"~([^~]+)~", r"<del>\1</del>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2" target="_blank" rel="noopener noreferrer">\1</a>', text)
    return text

def render_text(text: str) -> str:
    text = escape_html(text)
    text = render_inline(text)
    return text

def render_table(block):
    parts = ['<table>']
    
    parts.append('<thead><tr>')
    for cell in block['header']:
        parts.append(f'<th>{render_text(cell)}</th>')
    parts.append('</tr></thead>')

    parts.append('<tbody>')
    for row in block['rows']:
        parts.append('<tr>')
        for cell in row:
            parts.append(f'<td>{render_text(cell)}</td>')
        parts.append('</tr>')
    parts.append('</tbody></table>')

    return ''.join(parts)

def render_block(block: dict) -> str:
    block_type = block['type']
    
    text = render_text(block['text'])

    if block_type == '---':
        return '<hr>'
    elif block_type == 'p':
        return f'<p>{text}</p>'
    elif block_type == '#':
        return f'<h1>{text}</h1>'
    elif block_type == '##':
        return f'<h2>{text}</h2>'
    elif block_type == '###':
        return f'<h3>{text}</h3>'
    elif block_type == 'ul' or block_type == 'ol':
        items = '\n'.join(
            f'<li>{render_text(item)}</li>'
            for item in block['items']
        )
        return f'<{block_type}>\n{items}\n</{block_type}>'
    elif block_type == 'code':
        code_text = escape_html('\n'.join(block['lines']))
        lang_class = ''
        if block.get('lang'):
            lang_class = f' class="language-{block["lang"]}"'

        return f'<pre><code{lang_class}>\n{code_text}\n</code></pre>'
    elif block_type == 'blockquote':
        inner = []
        for line in block['lines']:
            if line.strip():
                text = render_text(line)
                inner.append(f'<p>{text}</p>')

        content = '\n'.join(inner)
        return f'<blockquote>\n{content}\n</blockquote>'
    elif block_type == 'table':
        return render_table(block)
    return ''

def render_blocks(blocks: list[dict]) -> str:
    return '\n'.join(render_block(block) for block in blocks)

def main():
    parser = argparse.ArgumentParser("Convert Markdown to HTML")
    parser.add_argument('--input', type=Path, help='Input Markdown file', default=Path('input.md'))
    parser.add_argument('--output', type=Path, help='Output HTML file', default=Path('output.html'))
    parser.add_argument('--css', type=Path, help='CSS file to link', default=Path('styles.css'))
    args = parser.parse_args()

    if not args.input.exists():
        raise FileNotFoundError(f'Input file not found: {args.input}')

    md_text = args.input.read_text(encoding='utf-8')
    blocks = parse_markdown(md_text)
    html_body = render_blocks(blocks)

    full_html = HTML_TEMPLATE.format(content=html_body, css_path=args.css)
    args.output.write_text(full_html, encoding='utf-8')

if __name__ == '__main__':
    main()
