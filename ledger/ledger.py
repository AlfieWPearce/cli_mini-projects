import sys
from datetime import datetime
from pathlib import Path

BASE = Path.home() / "ledger"
BASE.mkdir(exist_ok=True)

today = datetime.now().strftime("%Y-%m-%d")
log = BASE / f"{today}.txt"

def timestamp():
    return datetime.now().strftime("%H:%M")

def write(line):
    with log.open("a") as f:
        f.write(line + "\n")

def read_log():
    lines = log.read_text().splitlines()
    return lines[0], lines[1:]

def complete(task):
    header, contents = read_log()

    for i in range(len(contents) - 1, -1, -1):
        if "[ ]" in contents[i] and task in contents[i]:
            contents[i] = contents[i].replace("[ ]", "[X]", 1)
            break
    else:
        print("No matching task")
        return

    log.write_text("\n".join([header] + contents))

def tasks():
    header, contents = read_log()
    return [header] + [line for line in contents if "NOTE" not in line]


if not log.exists():
    write(today)

commands = {
    "note":     lambda text: write(f"[{timestamp()}] NOTE  {text}"),
    "task":     lambda text: write(f"[{timestamp()}]  [ ]  {text}"),
    "complete": lambda text: complete(text),
    "show":     lambda _: print(log.read_text()),
    "tasks":    lambda _: print("\n".join(tasks())),
    "help":     lambda _: print("Usage: ledger note|task|complete|show|tasks|help"),
}

def main():
    cmd = sys.argv[1].lower() if len(sys.argv) > 1 else "help"
    text = " ".join(sys.argv[2:])

    commands.get(cmd, commands["help"])(text)

if __name__ == "__main__":
    main()
