import os
from cs50 import SQL
from datetime import datetime
from zoneinfo import ZoneInfo

def add_category(user_id, category_name):
    """Add a new category for the user."""
    category_name = category_name.strip().upper()
    if not category_name:
        return "Category Field Empty"
    if len(category_name) >= 30:
        return "Category length too high"
    existing_categories = db.execute("SELECT category_name FROM category WHERE user_id = ?", user_id)
    if category_name in [row["category_name"] for row in existing_categories]:
        return "Category already exists"
    db.execute("INSERT INTO category (user_id, category_name) VALUES (?, ?)", user_id, category_name)
    return "Category Successfully Added"

def delete_category(user_id, category_name):
    """Delete a category for the user."""
    if category_name == "General":
        return "Cannot delete General category"
    existing_categories = db.execute("SELECT category_name FROM category WHERE user_id = ?", user_id)
    if category_name not in [row["category_name"] for row in existing_categories]:
        return "Category does not exist"
    db.execute("DELETE FROM category WHERE user_id = ? AND category_name = ?", user_id, category_name)
    db.execute("DELETE FROM tasks WHERE user_id = ? AND category = ?", user_id, category_name)
    return f"Category '{category_name}' deleted successfully."

def add_task(user_id, task_name, category_name, target_date):
    """Add a new task for the user."""
    task_name = task_name.strip().upper()
    if not task_name:
        return "Task Field Empty"
    if len(task_name) > 30:
        return "Task name too long"
    existing_tasks = db.execute("SELECT task FROM tasks WHERE user_id = ?", user_id)
    if task_name in [row["task"] for row in existing_tasks]:
        return "Task already exists"
    if not target_date:
        target_date = datetime.now(ZoneInfo("Asia/Kolkata")).date()
    db.execute(
        "INSERT INTO tasks (user_id, task, category, status, target, created_at, completed_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
        user_id, task_name, category_name, "NOT STARTED", target_date, datetime.now(ZoneInfo("Asia/Kolkata")), None
    )
    return "Task added successfully!"

def main():
    print("This is a logic module and is designed to be tested via test_project.py")

# Setup the database connection for use in functions
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "database.db")
db = SQL(f"sqlite:///{db_path}")

if __name__ == "__main__":
    main()
