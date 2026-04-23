from __future__ import annotations

import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Any

STORAGE_FILE = Path(__file__).with_name("storage.json")
DATE_FORMAT = "%Y-%m-%d"
DEFAULT_CATEGORIES = ["Personal", "Work", "Study"]


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def load_storage() -> dict[str, Any]:
    if not STORAGE_FILE.exists():
        initial_data = {"users": {}, "tasks": {}}
        save_storage(initial_data)
        return initial_data

    with STORAGE_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if "users" not in data or "tasks" not in data:
        data = {"users": {}, "tasks": {}}
        save_storage(data)

    return data


def save_storage(data: dict[str, Any]) -> None:
    with STORAGE_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def print_header(title: str) -> None:
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def pause() -> None:
    input("\nPress Enter to continue...")


class TodoApp:
    def __init__(self) -> None:
        self.storage = load_storage()
        self.current_user: str | None = None

    def run(self) -> None:
        while True:
            print_header("Python To-Do App")
            print("1. Register")
            print("2. Login")
            print("3. Exit")

            choice = input("\nChoose an option: ").strip()
            if choice == "1":
                self.register_user()
            elif choice == "2":
                self.login_user()
            elif choice == "3":
                print("\nGoodbye!")
                break
            else:
                print("\nInvalid option. Please choose 1, 2, or 3.")
                pause()

    def register_user(self) -> None:
        print_header("Register")
        username = input("Enter username: ").strip().lower()

        if not username:
            print("Username cannot be empty.")
            pause()
            return

        if username in self.storage["users"]:
            print("Username already exists. Please login instead.")
            pause()
            return

        password = input("Enter password (min 4 chars): ").strip()
        confirm_password = input("Confirm password: ").strip()

        if len(password) < 4:
            print("Password must be at least 4 characters.")
            pause()
            return

        if password != confirm_password:
            print("Passwords do not match.")
            pause()
            return

        self.storage["users"][username] = {
            "password_hash": hash_password(password),
            "created_at": now_iso(),
            "categories": DEFAULT_CATEGORIES.copy(),
        }
        self.storage["tasks"][username] = []
        save_storage(self.storage)

        print("Registration successful. You can now login.")
        pause()

    def login_user(self) -> None:
        print_header("Login")
        username = input("Username: ").strip().lower()
        password = input("Password: ").strip()

        user = self.storage["users"].get(username)
        if not user:
            print("User not found.")
            pause()
            return

        if user["password_hash"] != hash_password(password):
            print("Incorrect password.")
            pause()
            return

        self.current_user = username
        print(f"Login successful. Welcome, {username}!")
        self.user_menu()

    def user_menu(self) -> None:
        while self.current_user:
            print_header(f"To-Do Menu - User: {self.current_user}")
            print("1. Add Category")
            print("2. View Categories")
            print("3. Add Task")
            print("4. View Tasks")
            print("5. Edit Task")
            print("6. Delete Task")
            print("7. Mark Task as Completed")
            print("8. Logout")

            choice = input("\nChoose an option: ").strip()
            if choice == "1":
                self.add_category()
            elif choice == "2":
                self.view_categories()
            elif choice == "3":
                self.add_task()
            elif choice == "4":
                self.view_tasks()
            elif choice == "5":
                self.edit_task()
            elif choice == "6":
                self.delete_task()
            elif choice == "7":
                self.mark_completed()
            elif choice == "8":
                self.current_user = None
                print("Logged out successfully.")
                pause()
            else:
                print("Invalid option. Try again.")
                pause()

    def get_categories(self) -> list[str]:
        if self.current_user is None:
            return []
        return self.storage["users"][self.current_user].setdefault("categories", DEFAULT_CATEGORIES.copy())

    def view_categories(self) -> None:
        print_header("Categories")
        categories = self.get_categories()
        for idx, category in enumerate(categories, start=1):
            print(f"{idx}. {category}")
        pause()

    def add_category(self) -> None:
        print_header("Add Category")
        new_category = input("Enter new category name: ").strip()

        if not new_category:
            print("Category name cannot be empty.")
            pause()
            return

        categories = self.get_categories()
        if new_category in categories:
            print("This category already exists.")
            pause()
            return

        categories.append(new_category)
        save_storage(self.storage)
        print("Category added successfully.")
        pause()

    def add_task(self) -> None:
        print_header("Add Task")
        title = input("Task title: ").strip()
        description = input("Task description (optional): ").strip()

        if not title:
            print("Task title cannot be empty.")
            pause()
            return

        category = self.select_category()
        if category is None:
            return

        due_date = input(f"Due date ({DATE_FORMAT}) optional: ").strip()
        if due_date and not self.is_valid_date(due_date):
            print(f"Invalid date. Use {DATE_FORMAT}.")
            pause()
            return

        tasks = self.get_tasks()
        task_id = 1 if not tasks else max(task["id"] for task in tasks) + 1

        task = {
            "id": task_id,
            "title": title,
            "description": description,
            "category": category,
            "due_date": due_date,
            "status": "pending",
            "created_at": now_iso(),
            "updated_at": now_iso(),
        }
        tasks.append(task)
        save_storage(self.storage)

        print(f"Task #{task_id} added successfully.")
        pause()

    def view_tasks(self) -> None:
        print_header("View Tasks")
        tasks = self.get_tasks()
        if not tasks:
            print("No tasks available.")
            pause()
            return

        category_filter = input("Filter by category (leave blank for all): ").strip()
        status_filter = input("Filter by status (pending/completed, blank for all): ").strip().lower()

        filtered_tasks = tasks
        if category_filter:
            filtered_tasks = [task for task in filtered_tasks if task["category"].lower() == category_filter.lower()]
        if status_filter in {"pending", "completed"}:
            filtered_tasks = [task for task in filtered_tasks if task["status"] == status_filter]

        if not filtered_tasks:
            print("No tasks match your filters.")
            pause()
            return

        for task in filtered_tasks:
            print("-" * 60)
            print(f"ID       : {task['id']}")
            print(f"Title    : {task['title']}")
            print(f"Desc     : {task['description'] or '-'}")
            print(f"Category : {task['category']}")
            print(f"Due Date : {task['due_date'] or '-'}")
            print(f"Status   : {task['status']}")
            print(f"Updated  : {task['updated_at']}")

        print("-" * 60)
        pause()

    def edit_task(self) -> None:
        print_header("Edit Task")
        tasks = self.get_tasks()
        if not tasks:
            print("No tasks available to edit.")
            pause()
            return

        task_id = self.read_task_id()
        if task_id is None:
            return

        task = self.find_task(task_id)
        if task is None:
            print("Task ID not found.")
            pause()
            return

        print("Leave fields blank to keep existing values.")
        new_title = input(f"New title [{task['title']}]: ").strip()
        new_description = input(f"New description [{task['description'] or '-'}]: ").strip()
        new_due_date = input(f"New due date [{task['due_date'] or '-'}] ({DATE_FORMAT}): ").strip()

        change_category = input("Change category? (y/n): ").strip().lower()
        new_category = task["category"]
        if change_category == "y":
            selected_category = self.select_category()
            if selected_category is None:
                return
            new_category = selected_category

        if new_due_date and not self.is_valid_date(new_due_date):
            print(f"Invalid date. Use {DATE_FORMAT}.")
            pause()
            return

        if new_title:
            task["title"] = new_title
        if new_description:
            task["description"] = new_description
        if new_due_date:
            task["due_date"] = new_due_date
        task["category"] = new_category
        task["updated_at"] = now_iso()

        save_storage(self.storage)
        print("Task updated successfully.")
        pause()

    def delete_task(self) -> None:
        print_header("Delete Task")
        tasks = self.get_tasks()
        if not tasks:
            print("No tasks available to delete.")
            pause()
            return

        task_id = self.read_task_id()
        if task_id is None:
            return

        task = self.find_task(task_id)
        if task is None:
            print("Task ID not found.")
            pause()
            return

        confirm = input(f"Delete task #{task_id} ({task['title']})? (y/n): ").strip().lower()
        if confirm != "y":
            print("Delete cancelled.")
            pause()
            return

        tasks.remove(task)
        save_storage(self.storage)
        print("Task deleted successfully.")
        pause()

    def mark_completed(self) -> None:
        print_header("Mark Task as Completed")
        tasks = self.get_tasks()
        pending_tasks = [task for task in tasks if task["status"] == "pending"]

        if not pending_tasks:
            print("No pending tasks found.")
            pause()
            return

        task_id = self.read_task_id()
        if task_id is None:
            return

        task = self.find_task(task_id)
        if task is None:
            print("Task ID not found.")
            pause()
            return

        task["status"] = "completed"
        task["updated_at"] = now_iso()
        save_storage(self.storage)

        print("Task marked as completed.")
        pause()

    def get_tasks(self) -> list[dict[str, Any]]:
        if self.current_user is None:
            return []
        return self.storage["tasks"].setdefault(self.current_user, [])

    def find_task(self, task_id: int) -> dict[str, Any] | None:
        for task in self.get_tasks():
            if task["id"] == task_id:
                return task
        return None

    def read_task_id(self) -> int | None:
        raw = input("Enter task ID: ").strip()
        if not raw.isdigit():
            print("Task ID must be a number.")
            pause()
            return None
        return int(raw)

    def select_category(self) -> str | None:
        categories = self.get_categories()
        print("Available categories:")
        for idx, category in enumerate(categories, start=1):
            print(f"{idx}. {category}")

        raw = input("Select category number (or type new category name): ").strip()
        if not raw:
            print("Category cannot be empty.")
            pause()
            return None

        if raw.isdigit():
            index = int(raw)
            if 1 <= index <= len(categories):
                return categories[index - 1]
            print("Invalid category number.")
            pause()
            return None

        if raw not in categories:
            categories.append(raw)
            save_storage(self.storage)

        return raw

    @staticmethod
    def is_valid_date(date_text: str) -> bool:
        try:
            datetime.strptime(date_text, DATE_FORMAT)
            return True
        except ValueError:
            return False


if __name__ == "__main__":
    app = TodoApp()
    app.run()
