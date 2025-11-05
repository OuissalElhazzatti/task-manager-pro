# models.py
# ===============================

from datetime import datetime, date

# Diese Datei beschreibt, wie ein "Task" (Aufgabe) aufgebaut ist.
# Ein Task hat: id, title, description, status.
# Außerdem hat er eine Methode to_json(), damit wir ihn als JSON zurückgeben können.

class Task:
    def __init__(self, id, title, description, status="To Do", user_id=None, day_id=None):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.user_id = user_id
        self.day_id = day_id
        self.created_at = datetime.now().isoformat(timespec="seconds")

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "user_id": self.user_id,
            "day_id": self.day_id,
            "created_at": self.created_at
        }
    

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password  # später: wird verschlüsselt gespeichert (nicht im Klartext!)

    def to_json(self):
        return {
            "id": self.id,
            "username": self.username
        }
    

class Day:
    def __init__(self, id, date_value=None):
        self.id = id
        self.date = date_value or date.today().isoformat()
        self.tasks = []  # Aufgaben dieses Tages

    def add_task(self, task):
        self.tasks.append(task)

    def to_json(self):
        return {
            "id": self.id,
            "date": self.date,
            "tasks": [t.to_json() for t in self.tasks]
        }
    

class Notification:
    def __init__(self, id, message, user_id=None, task_id=None, type="info", title=None):
        self.id = id
        self.message = message
        self.user_id = user_id
        self.task_id = task_id
        self.type = type            # "info" | "warning" | "success" | "error"
        self.title = title
        self.is_read = False
        self.created_at = datetime.now().isoformat(timespec="seconds")
        self.read_at = None

    def to_json(self):
        return {
            "id": self.id,
            "message": self.message,
            "user_id": self.user_id,
            "task_id": self.task_id,
            "type": self.type,
            "title": self.title,
            "is_read": self.is_read,
            "created_at": self.created_at,
            "read_at": self.read_at
        }