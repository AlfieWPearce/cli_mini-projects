from datetime import datetime
import os
import sys
import subprocess
import difflib
from random import randint

NOTE_DIR = 'notes'
STATE_FILE = '.note_state'

def load_state():
    state = {}
    if not os.path.exists(STATE_FILE):
        return state

    with open(STATE_FILE, 'r') as f:
        for line in f:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                state[key] = value
    return state
def save_state(**kwargs):
    state = load_state()
    state.update(kwargs)

    with open(STATE_FILE, 'w') as f:
        for k, v in state.items():
            f.write(f'{k}={v}\n')


def generate_id():
    return datetime.now().strftime('%d-%m-%YT%H-%M-%S')  

def create_note():
    note_id = generate_id()
    os.makedirs(NOTE_DIR, exist_ok=True)

    path = os.path.join(NOTE_DIR, f'{note_id}.txt')
    template = f"""# Title

Created: {note_id}

---

Write one idea here.

---

Links:
- place IDs here

"""

    with open(path, 'w', encoding='utf-8') as f:
        f.write(template)

    print(f'Create note {note_id}')
    edit_note(note_id)
    return note_id

def edit_note(note_id):
    path = os.path.join(NOTE_DIR, f'{note_id}.txt')
    if not os.path.exists(path):
        print('Note not found.')
        return

    editor = os.environ.get('EDITOR')
    if not editor:
        editor = 'nano'

    subprocess.run([editor, path])

def read_note(note_id):
    path = os.path.join(NOTE_DIR, f'{note_id}.txt')
    if not os.path.exists(path):
        print('Note not found.')
        return
    with open(path,'r',encoding='utf-8') as f:
        print(f.read())

def backlinks(note_id):
    if not os.path.exists(NOTE_DIR):
        return []

    results = []

    for filename in os.listdir(NOTE_DIR):
        if not filename.endswith('.txt'):
            continue

        path = os.path.join(NOTE_DIR, filename)
        with open(path, 'r', encoding='utf-8') as f:
            if note_id in f.read() and not filename == '{note_id}.txt':
                results.append(filename.replace('.txt',''))
    return results
def read_with_backlinks(note_id):
    read_note(note_id)

    links = backlinks(note_id)
    if links:
        print('Backlinks:')
        for l in links:
            print(f'- {l}')

def list_notes(predicate=lambda _id, _content: True):
    notes_list = []
    for note_file in os.listdir(NOTE_DIR):
        if not note_file.endswith('txt'):
            continue

        note_id = note_file.replace('.txt','')
        note_path = os.path.join(NOTE_DIR, note_file)
        with open(note_path, 'r') as f:
            content = f.read()

        if predicate(note_id, content):
            notes_list.append(note_id)

    return notes_list

def fuzzy_search(query):
    def search_predicate(note_id, content):
        content = content.lower()
        words = content.split()

        for word in words:
            ratio = difflib.SequenceMatcher(None, query, word).ratio()
            if ratio > 0.8:
                return True
        return False

    candidates = list_notes(search_predicate)
    scored = []
    for note_id in candidates:
        note_path = os.path.join(NOTE_DIR, f'{note_id}.txt')

        with open(note_path, 'r') as f:
            content = f.read().lower()

        best_ratio = 0.0
        best_word = ''
        for word in content.split():
            ratio = difflib.SequenceMatcher(None, query, word).ratio()
            best_word = word if ratio > best_ratio else best_word
            best_ratio = max(best_ratio, ratio)

        scored.append((note_id, best_ratio, best_word))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored 

def get_title(note_id):
    path = os.path.join(NOTE_DIR, f'{note_id}.txt')
    try:
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if line.startswith('#'):
                    return line.lstrip('#').strip()
                return line # fallback - first non-empty line
    except FileNotFoundError:
        return '(Missing note)'

def format_note_line(note_id, score=None, word=None):
    title = get_title(note_id)
    if score is not None and score < 1:
        return f'{note_id} ({score:.2f} | {word}) - {title}'
    return f'{note_id} - {title}'

def main():
    if len(sys.argv) < 2:
        print('Usage: note.py [help|create|edit|read|random|list|search|fzf] [id|content]')
        return

    command = sys.argv[1].lower()

    if command == 'help' or command == 'h' or command == '-h':
        print("""Usage of note.py:
Core:
 [help]             Shows this list
 [create]           Creates a note and starts the editor
 [edit]   [id]      Edits note [id] in $EDITOR (fallback: nano)
 [read]   [id]      Reads note [id] and shows backlinks

Navigation:
 [random]           Reads a random note
 [list]             Lists all notes' ids
 [search] [content] Normal search finds notes with content that includes [content]
 [fzf]    [content] Fuzzy search finds notes with content alike [content]
""")

    elif command == 'create':
        note_id = create_note()
        save_state(last_note=note_id)

    elif command == 'read':
        if len(sys.argv) < 3:
            last = load_state()['last_note']
            if last:
                print(f'\nReading last note {last}:\n')
                read_with_backlinks(last)
                return
            print('Provide a note ID.')
        else:
            save_state(last_note=sys.argv[2])
            read_with_backlinks(sys.argv[2])

    
    elif command == 'random':
        note_list = list_notes()
        index = randint(0, len(note_list)-1)
        read_with_backlinks(note_list[index])
        save_state(last_note=note_list[index])

    elif command == 'edit':
        if len(sys.argv) < 3:
            last = load_state()['last_note']
            if last:
                print(f'\nEditing last note {last}:\n')
                edit_note(last)
                return
            print('Provide a note ID.')
        else:
            save_state(last_note=sys.argv[2])
            edit_note(sys.argv[2]) 
    
    elif command == 'list':
        print('\n'.join(list_notes()))

    elif command == 'search':
        if len(sys.argv) < 3:
            last = load_state()['last_search']
            if not last:
                print('Provide some contents to search.')
                return
            print(f'\nRepeating last search {last}:\n')
            query = last
        else:
            query = sys.argv[2]
            save_state(last_search=query)
        query = query.lower()
        def search_predicate(note_id, content):
            return query in content.lower()

        candidates = list_notes(search_predicate)
        if len(candidates) > 0:
            for note_id in candidates:
                print(format_note_line(note_id))
            return
        
        print('Search resulted in no results. Now trying a fuzzy find:')
        results = fuzzy_search(query)
        if len(results) > 0:
            for note_id, score, word in results:
                print(format_note_line(note_id, score, word))
            return

        print(f'Fuzzy Search also failed - most likely {sys.argv[2]} doesn\'t appear')
        return


    elif command == 'fzf':
        if len(sys.argv) < 3:
            last = load_state()['last_search']
            if not last:
                print('Provide some contents to search.')
                return
            print(f'\nRepeating last search {last}:\n')
            query = last
        else:
            query = sys.argv[2]
            save_state(last_search=query)
        query = query.lower()
        results = fuzzy_search(query)
        if len(results) > 0:
            for note_id, score, word in results:
                print(format_note_line(note_id, score, word))
            return
        
        print(f'Fuzzy search failed - most likely {sys.argv[2]} doesn\t appear')

    else:
        print('Unkown command.')

if __name__ == '__main__':
    main()
