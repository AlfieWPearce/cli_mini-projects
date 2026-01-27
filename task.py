import argparse

parser = argparse.ArgumentParser(
        prog='Task Manager',
        description='Handle to-dos quickly with minimal hassle',
        epilog='Enjoy using this tool :)')
parser.add_argument('-c', '--command', type=str, help='What to do? [add|remove|done|list]')
parser.add_argument('-t', '--task', type=str, help='What task address / task name to handle / affect?')
args = parser.parse_args()

def getTask():
    return args.task if hasattr(args, "task") and args.task is not None else input("What task to handle? ")
def getCommand():
    return input("What to do? [add|remove|done|list|exit] ")

def addTask(task):
    with open("tasks.txt", "a") as f:
        f.write("0," + task + "\n")

def completeTask(task_number):
    index = int(task_number) - 1
    with open("tasks.txt", "r") as f:
        tasks = f.read().split("\n")

    if 0 <= index < len(tasks):
        splitTask = tasks[index].split(",")
        tasks[index] = "1," + splitTask[1]
    else:
        print("Invalid task number")
        return

    with open("tasks.txt", "w") as f:
        f.write("\n".join(tasks))


def removeTask(task_number):
    index = int(task_number) - 1
    with open("tasks.txt", "r") as f:
        tasks = f.read().splitlines()

    if 0 <= index < len(tasks):
        tasks.pop(index)
    else:
        print("Invalid task number")
        return

    with open("tasks.txt", "w") as f:
        f.write("\n".join(tasks))

def listTasks():
    with open ("tasks.txt", "r") as f:
        tasks = f.read().splitlines()
    for index, task in enumerate(tasks, start=1):
        taskSplit = task.split(",")
        print(f"{index}. [{'X' if taskSplit[0]=='1' else ' '}] {taskSplit[1]}")

def parseCommand(command):
    match command.lower():
        case "add":
            addTask(getTask())
        case "remove":
            removeTask(getTask())
        case "done":
            completeTask(getTask())
        case "list":
            listTasks()
        case "exit":
            return True
        case _:
            print("Please enter a valid command!")
def main():
    if hasattr(args, 'command') and args.command is not None:
        parseCommand(args.command)
        return
    while True:
        command = getCommand()
        if parseCommand(command):
            return
if __name__ == "__main__":
    main()
