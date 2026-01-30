from pathlib import Path
import re

input_path = Path('input.md')
output_path = Path('output.html')

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>mdview</title>
    <link rel="stylesheet" href="styles.css"
</head>
<body>
<main class="markdown-body">
{content}
</main>
</body>
</html>
"""

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
    text = re.sub(r"~~([^~]+)~~", r"<del>\1</del>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2" target="_blank" rel="noopener noreferrer">\1</a>', text)
    return text

def render_text(text: str) -> str:
    text = escape_html(text)
    text = render_inline(text)
    return text

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
    return ''

def render_blocks(blocks: list[dict]) -> str:
    return '\n'.join(render_block(block) for block in blocks)

def main():
    md_text = input_path.read_text(encoding='utf-8')

    blocks = parse_markdown(md_text)
    html_body = render_blocks(blocks)

    full_html = HTML_TEMPLATE.format(content=html_body)
    output_path.write_text(full_html, encoding='utf-8')

if __name__ == '__main__':
    main()
