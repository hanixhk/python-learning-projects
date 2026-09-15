import json

tasks = []

def add_task(title, description, due_date):
    tasks.append({"Title": title, "Description": description, "Due Date": due_date, "Completed": False})

def view_tasks():
    if not tasks:
        print("No tasks recorded.")
        return
    for task in tasks:
        print(f"Title: {task['Title']}, Description: {task['Description']}, Due Date: {task['Due Date']}, Completed: {task['Completed']}")

def search_task_by_title(title):
    found_tasks = []
    for task in tasks:
        if title.lower() in task["Title"].lower():
            found_tasks.append(task)
    if not found_tasks:
        print("No tasks found.")
    else:
        for task in found_tasks:
            print(f"Title: {task['Title']}, Description: {task['Description']}, Due Date: {task['Due Date']}, Completed: {task['Completed']}")

def delete_task(title):
    for task in tasks:
        if title.lower() == task["Title"].lower():
            tasks.remove(task)
            print(f"Task {task['Title']} deleted.")
            return
    print("Task not found.")

def update_task(old_title, new_title, new_description, new_due_date):
    for task in tasks:
        if old_title.lower() == task["Title"].lower():
            task["Title"] = new_title
            task["Description"] = new_description
            task["Due Date"] = new_due_date
            print(f"Task {old_title} updated.")
            return
    print("Task not found.")

def save_tasks_to_file(filename):
    try:
        with open(filename, 'w') as file:   

            json.dump(tasks, file)
    except Exception as e:
        print(f"Error saving tasks to file: {e}")


def mark_task_as_completed(title):
    for task in tasks:
        if title.lower() == task["Title"].lower():
            task["Completed"] = True
            print(f"Task {task['Title']} marked as completed.")
            return
    print("Task not found.")


def load_tasks_from_file(filename):
    try:
        with open(filename, 'r') as file:
            loaded_tasks = json.load(file)
            tasks.extend(loaded_tasks)  


    except Exception as e:
        print(f"Error loading tasks from file: {e}")


def filter_completed_tasks():
    completed_tasks = [task for task in tasks if task.get("Completed")]
    if not completed_tasks:
        print("No completed tasks found.")
    else:
        for task in completed_tasks:
            print(f"Title: {task['Title']}, Description: {task['Description']}, Due Date: {task['Due Date']}, Completed: {task['Completed']}")


while True:
    print("1. Add task 2. View tasks 3. Search task 4. Delete task 5. Update task 6. Mark as completed 7. Filter completed tasks 8. Save to file 9. Load from file 10. Exit")
    choice = input("Choose an option: ")
    if choice == '1':
        title = input("Enter task title: ")
        description = input("Enter task description: ")
        due_date = input("Enter task due date: ")
        add_task(title, description, due_date)
    elif choice == '2':
        view_tasks()
    elif choice == '3':
        title = input("Enter task title to search: ")
        search_task_by_title(title)
    elif choice == '4':
        title = input("Enter task title to delete: ")
        delete_task(title)
    elif choice == '5':
        old_title = input("Enter the title of the task to update: ")
        new_title = input("Enter new task title: ")
        new_description = input("Enter new task description: ")
        new_due_date = input("Enter new task due date: ")
        update_task(old_title, new_title, new_description, new_due_date)
    elif choice == '6':
        title = input("Enter task title to mark as completed: ")
        mark_task_as_completed(title)
    elif choice == '7':
        filter_completed_tasks()
    elif choice == '8':
        filename = input("Enter filename to save tasks: ")
        save_tasks_to_file(filename)
    elif choice == '9':
        filename = input("Enter filename to load tasks from: ")
        load_tasks_from_file(filename)
    elif choice == '10':
        print("Exiting the task manager. Goodbye!")
        break
    else:
        print("Invalid choice. Please select a valid option.")