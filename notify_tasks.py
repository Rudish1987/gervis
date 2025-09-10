import os
from datetime import datetime, timedelta
from plyer import notification

def get_yesterdays_tasks(note_dir="notes"):
    yesterday = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    note_file = os.path.join(note_dir, f"{yesterday}.txt")
    if not os.path.exists(note_file):
        return []

    tasks = []
    with open(note_file, "r") as f:
        lines = f.readlines()
        extract = False
        for line in lines:
            if "Pending / Tomorrow:" in line:
                extract = True
                continue
            if extract:
                if line.strip().startswith("-"):
                    tasks.append(line.strip())
                elif line.strip() == "":
                    break
    return tasks

def notify(tasks):
    if not tasks:
        message = "No tasks found from yesterday's note."
    else:
        message = "\n".join(tasks)
    notification.notify(
        title="Today's Tasks",
        message=message,
        timeout=10
    )

if __name__ == "__main__":
    tasks = get_yesterdays_tasks()
    notify(tasks)
