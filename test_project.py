import pytest
import warnings
from project import add_category, delete_category, add_task

# Suppress DeprecationWarnings globally
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Mock database setup
class MockDB:
    def __init__(self):
        self.data = {"category": [], "tasks": []}

    def execute(self, query, *args):
        if "SELECT category_name FROM category" in query:
            return [{"category_name": row} for row in self.data["category"]]
        elif "INSERT INTO category" in query:
            self.data["category"].append(args[1])
        elif "DELETE FROM category" in query:
            self.data["category"].remove(args[1])
        elif "SELECT task FROM tasks" in query:
            return [{"task": row} for row in self.data["tasks"]]
        elif "INSERT INTO tasks" in query:
            self.data["tasks"].append(args[1])
        elif "DELETE FROM tasks" in query:
            self.data["tasks"] = [task for task in self.data["tasks"] if task != args[1]]

# Replace the real database with the mock database
mock_db = MockDB()

def test_add_category(monkeypatch):
    monkeypatch.setattr("project.db", mock_db)
    user_id = 1
    assert add_category(user_id, "Work") == "Category Successfully Added"
    assert add_category(user_id, "") == "Category Field Empty"
    assert add_category(user_id, "A" * 31) == "Category length too high"
    assert add_category(user_id, "Work") == "Category already exists"

def test_delete_category(monkeypatch):
    monkeypatch.setattr("project.db", mock_db)
    user_id = 1
    mock_db.data["category"] = ["Work", "General"]
    assert delete_category(user_id, "General") == "Cannot delete General category"
    assert delete_category(user_id, "Nonexistent") == "Category does not exist"
    assert delete_category(user_id, "Work") == "Category 'Work' deleted successfully."

def test_add_task(monkeypatch):
    monkeypatch.setattr("project.db", mock_db)
    user_id = 1
    category_name = "Work"
    mock_db.data["category"] = ["Work"]
    assert add_task(user_id, "Task1", category_name, None) == "Task added successfully!"
    assert add_task(user_id, "", category_name, None) == "Task Field Empty"
    assert add_task(user_id, "A" * 31, category_name, None) == "Task name too long"
    assert add_task(user_id, "Task1", category_name, None) == "Task already exists"