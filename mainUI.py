import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import datetime
import json
from plyer import notification
import time
import threading


# Sample task data structure
tasks = []

def check_for_reminders():
    while True:
        current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        for task in tasks:
            if 'reminder_date' in task and task['reminder_date'] == current_datetime:
                # show notification
                show_notification(task['name'])
        time.sleep(60) # Check every minute

def show_notification(task_name):
    notification.notify(
        title='Task Reminder',
        message=f"Reminder: {task_name} is due!",
        timeout=10  # duration in seconds
    )

# Function to save tasks to a file
def save_to_file():
    with open("tasks.json", "w") as file:
        json.dump(tasks, file)

# Function to load tasks from a file
def load_from_file():
    global tasks
    try:
        with open("tasks.json", "r") as file:
            tasks = json.load(file)
    except FileNotFoundError:
        tasks = []

# Function to add a task using the UI
def add_task_ui():
    # Create a new window
    add_task_window = tk.Toplevel(root)
    add_task_window.title("Add Task")
    
    # Task name
    task_name = tk.StringVar()
    name_entry = ttk.Entry(add_task_window, textvariable=task_name)
    name_entry.grid(row=0, column=1, padx=20, pady=5)
    ttk.Label(add_task_window, text="Task Name: ").grid(row=0, column=0, padx=20, pady=5)
    
    # Task description
    task_description = tk.StringVar()
    description_entry = ttk.Entry(add_task_window, textvariable=task_description)
    description_entry.grid(row=1, column=1, padx=20, pady=5)
    ttk.Label(add_task_window, text="Description: ").grid(row=1, column=0, padx=20, pady=5)
    
    # Due date
    due_date = tk.StringVar()
    due_date_entry = ttk.Entry(add_task_window, textvariable=due_date)
    due_date_entry.grid(row=2, column=1, padx=20, pady=5)
    ttk.Label(add_task_window, text="Due Date (YYYY-MM-DD): ").grid(row=2, column=0, padx=20, pady=5)
    
    # Reminder date-time
    reminder_date = tk.StringVar()
    reminder_date_entry = ttk.Entry(add_task_window, textvariable=reminder_date)
    reminder_date_entry.grid(row=3, column=1, padx=20, pady=5)
    ttk.Label(add_task_window, text="Reminder Date (YYYY-MM-DD HH:MM): ").grid(row=3, column=0, padx=20, pady=5)
    
    # Add button
    ttk.Button(add_task_window, text="Add", command=lambda: save_task(task_name, task_description, due_date, reminder_date, add_task_window)).grid(row=4, column=1, pady=20)


def save_task(name, description, due, reminder, window):
    task = {
        'name': name.get(),
        'description': description.get(),
        'due_date': due.get(),
        'status': 'Not Completed',  # Changed 'completed' to 'status'
        'reminder_date': reminder.get()
    }
    tasks.append(task)
    save_to_file()  # this will save tasks to json file
    window.destroy()
    refresh_tasks()


def remove_task():
    try:
        index = tasks_listbox.curselection()[0]
        tasks.pop(index)
        save_to_file()  # Save the updated tasks list to the JSON file
        refresh_tasks()
    except:
        messagebox.showwarning("Warning", "Please select a task to remove!")

def edit_task():
    try:
        index = tasks_listbox.curselection()[0]
        task = tasks[index]
        
        new_name = simpledialog.askstring("Input", "New Task Name:", initialvalue=task["name"])
        new_description = simpledialog.askstring("Input", "New Task Description:", initialvalue=task["description"])

        if new_name and new_description:
            task["name"] = new_name
            task["description"] = new_description

            refresh_tasks()

    except:
        messagebox.showwarning("Warning", "Please select a task to edit!")

def mark_as_completed():
    try:
        index = tasks_listbox.curselection()[0]
        task = tasks[index]
        task["status"] = "Completed"  # Changed 'completed' to 'status'
        refresh_tasks()
    except:
        messagebox.showwarning("Warning", "Please select a task to mark as completed!")

def refresh_tasks():
    tasks_listbox.delete(0, tk.END)
    for task in tasks:
        if 'status' not in task:  # Check if 'status' key exists
            task['status'] = 'Not Completed'  # Add 'status' key if it doesn't exist
        task_name = task["name"]
        if task["status"] == "Completed":
            task_name += " (Completed)"
        tasks_listbox.insert(tk.END, task_name)


# Initialize the main window
root = tk.Tk()
root.title("Task Manager")
root.geometry("500x600")

#task_name_label = tk.Label(root, text="Task Name:")
#task_name_label.pack(pady=20)
#task_name_entry = tk.Entry(root, width=30)
#task_name_entry.pack()

#task_description_label = tk.Label(root, text="Task Description:")
#task_description_label.pack(pady=20)
#task_description_entry = tk.Entry(root, width=30)
#task_description_entry.pack()

add_button = tk.Button(root, text="Add Task", command=add_task_ui)
add_button.pack(pady=10)

remove_button = tk.Button(root, text="Remove Task", command=remove_task)
remove_button.pack(pady=10)

edit_button = tk.Button(root, text="Edit Task", command=edit_task)
edit_button.pack(pady=10)

mark_completed_button = ttk.Button(root, text="Mark as Completed", command=mark_as_completed)
mark_completed_button.pack(pady=10)

tasks_listbox = tk.Listbox(root, width=50, height=20)
tasks_listbox.pack(pady=20)

refresh_tasks()

# Load tasks from file at startup
load_from_file()
refresh_tasks()
# Start the reminder thread
reminder_thread = threading.Thread(target=check_for_reminders)
reminder_thread.start()
root.mainloop()
