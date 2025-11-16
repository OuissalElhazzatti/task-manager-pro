from flask_sqlalchemy import SQLAlchemy
from datetime import datetime  #Füge einen Zeitstempel hinzu, damit jede Aufgabe weiß, wann sie erstellt wurde — 
                               #das hilft später bei Sortierung oder Anzeige.

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "username": self.username
        }                              


    
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default="To Do")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer)

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "user_id": self.user_id
        }    