from datetime import datetime  #Füge einen Zeitstempel hinzu, damit jede Aufgabe weiß, wann sie erstellt wurde — 
                               #das hilft später bei Sortierung oder Anzeige.

class Task:
    def __init__(self, id, title, description, status="To Do", user_id=None):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.user_id = user_id
        self.created_at = datetime.now().isoformat(timespec="seconds")

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "user_id": self.user_id,
            "created_at": self.created_at
        }
    



class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def to_json(self):
        return {
            "id": self.id,
            "username": self.username
        }    
    