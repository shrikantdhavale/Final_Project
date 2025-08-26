import json
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

class Task:
    def __init__(self, title, description, category, completed=False, created_at=None):
        self.title = title
        self.description = description
        self.category = category
        self.completed = completed
        self.created_at = created_at if created_at else datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def mark_completed(self):
        self.completed = True

def save_tasks(tasks):
    """Save tasks to a JSON file."""
    with open('tasks.json', 'w') as f:
        json.dump([task.__dict__ for task in tasks], f, indent=4)

def load_tasks():
    """Load tasks from a JSON file."""
    try:
        with open('tasks.json', 'r') as f:
            data = json.load(f)
            return [Task(**task) for task in data]
    except (FileNotFoundError, json.JSONDecodeError):
        return []

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal To-Do List")
        self.tasks = load_tasks()
        self.categories = ["Work", "Personal", "Urgent"]

        # GUI Setup
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        # Task Input Frame
        input_frame = ttk.Frame(self.root, padding="10")
        input_frame.pack(fill="x")

        ttk.Label(input_frame, text="Title:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.title_entry = ttk.Entry(input_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Description:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.desc_entry = ttk.Entry(input_frame, width=30)
        self.desc_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Category:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.category_combo = ttk.Combobox(input_frame, values=self.categories, width=27)
        self.category_combo.grid(row=2, column=1, padx=5, pady=5)
        self.category_combo.set(self.categories[0])

        ttk.Button(input_frame, text="Add Task", command=self.add_task).grid(row=3, column=0, columnspan=2, pady=10)

        # Task List Frame
        list_frame = ttk.Frame(self.root, padding="10")
        list_frame.pack(fill="both", expand=True)

        self.task_tree = ttk.Treeview(list_frame, columns=("Title", "Category", "Status", "Created"), show="headings")
        self.task_tree.heading("Title", text="Title")
        self.task_tree.heading("Category", text="Category")
        self.task_tree.heading("Status", text="Status")
        self.task_tree.heading("Created", text="Created At")
        self.task_tree.column("Title", width=150)
        self.task_tree.column("Category", width=100)
        self.task_tree.column("Status", width=100)
        self.task_tree.column("Created", width=150)
        self.task_tree.pack(fill="both", expand=True)

        # Buttons Frame
        button_frame = ttk.Frame(self.root, padding="10")
        button_frame.pack(fill="x")

        ttk.Button(button_frame, text="Mark Completed", command=self.mark_completed).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Delete Task", command=self.delete_task).pack(side="left", padx=5)
        ttk.Button(button_frame, text="View Details", command=self.view_details).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Exit", command=self.exit_app).pack(side="right", padx=5)

        self.update_task_list()

    def add_task(self):
        """Add a new task to the list."""
        title = self.title_entry.get().strip()
        description = self.desc_entry.get().strip()
        category = self.category_combo.get()

        if not title or not description:
            messagebox.showerror("Error", "Title and Description cannot be empty!")
            return

        task = Task(title, description, category)
        self.tasks.append(task)
        save_tasks(self.tasks)
        self.update_task_list()
        self.title_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        messagebox.showinfo("Success", "Task added successfully!")

    def update_task_list(self):
        """Update the task list display."""
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
        for i, task in enumerate(self.tasks):
            status = "Completed" if task.completed else "Pending"
            self.task_tree.insert("", tk.END, values=(task.title, task.category, status, task.created_at), tags=(i,))

    def mark_completed(self):
        """Mark the selected task as completed."""
        selected = self.task_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a task!")
            return
        task_index = int(self.task_tree.item(selected)["tags"][0])
        self.tasks[task_index].mark_completed()
        save_tasks(self.tasks)
        self.update_task_list()
        messagebox.showinfo("Success", "Task marked as completed!")

    def delete_task(self):
        """Delete the selected task."""
        selected = self.task_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a task!")
            return
        task_index = int(self.task_tree.item(selected)["tags"][0])
        self.tasks.pop(task_index)
        save_tasks(self.tasks)
        self.update_task_list()
        messagebox.showinfo("Success", "Task deleted successfully!")

    def view_details(self):
        """Show details of the selected task."""
        selected = self.task_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a task!")
            return
        task_index = int(self.task_tree.item(selected)["tags"][0])
        task = self.tasks[task_index]
        details = f"Title: {task.title}\nDescription: {task.description}\nCategory: {task.category}\nStatus: {'Completed' if task.completed else 'Pending'}\nCreated: {task.created_at}"
        messagebox.showinfo("Task Details", details)

    def exit_app(self):
        """Save tasks and exit the application."""
        save_tasks(self.tasks)
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()