# ===============================
# app.py
# ===============================
# Diese Datei startet den Flask-Webserver und definiert die "Routen" (URLs),
# über die der Client (z. B. dein Browser oder PowerShell) mit dem Backend kommuniziert.

from flask import Flask, jsonify, request   # Flask = Web-Framework, jsonify = JSON-Antworten, request = Eingaben lesen
from models import db,User, Task               # Wir importieren NUR unsere beiden Klassen: User und Task
                                               #2 # SQLAlchemy-Modelle und DB-Objekt importieren
from config import Config        #2 # Konfiguration für die Datenbank laden

# ===============================
# Flask-Anwendung erstellen
# ===============================
app = Flask(__name__)  # Erstellt eine Instanz der Flask-App → das Herz deines Webservers

# ⬇️ Flask mit der Datenbank verbinden
app.config.from_object(Config)  #2 # Datenbank-Konfiguration aktivieren
db.init_app(app)                #2 # SQLAlchemy mit der Flask-App verbinden

# ===============================
# "Datenbank" (in-memory)           Gelöscht
# ===============================


# ===============================
# ROUTEN (Endpoints)
# ===============================

# -------------------------------
# 1) Startseite – einfacher Test
# -------------------------------
@app.route("/")
def home():
    # Wird aufgerufen, wenn man http://127.0.0.1:5000/ im Browser öffnet
    return "Backend funktioniert ✅ (Flask läuft!)"


# ---------- TASKS ----------
# -------------------------------
# 2) Alle Aufgaben anzeigen (GET)
# -------------------------------
@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()                     # alle Tasks aus DB
    return jsonify([t.to_json() for t in tasks]), 200


# -------------------------------
# 3) Neue Aufgabe hinzufügen (POST)
# -------------------------------
@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Keine Daten empfangen"}), 400

    title = (data.get("title") or "").strip()
    description = data.get("description") or ""
    status = data.get("status", "To Do")
    user_id = data.get("user_id", None)

    if not title:
        return jsonify({"error": "title ist Pflicht"}), 400

    # neues Task speichern
    new_task = Task(
        title=title,
        description=description,
        status=status,
        user_id=user_id
    )

    db.session.add(new_task)
    db.session.commit()

    return jsonify({"message": "Aufgabe erstellt", "task": new_task.to_json()}), 201



# -------------------------------
# 4) Aufgabe löschen (DELETE)
# -------------------------------
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)

    if not task:
        return jsonify({"error": f"Task {task_id} nicht gefunden"}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({"message": f"Task {task_id} gelöscht"}), 200


# -------------------------------
# 5) Aufgabe aktualisieren (PUT)
# -------------------------------
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Keine Daten empfangen"}), 400
    
    # Gesuchte Aufgabe finden
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": f"Task {task_id} nicht gefunden"}), 404

    # Felder aktualisieren, falls im JSON enthalten
    if "title" in data:
        new_title = (data["title"] or "").strip()
        if not new_title:
            return jsonify({"error": "title darf nicht leer sein"}), 400
        task.title = new_title

    if "description" in data:
        task.description = data["description"] or ""

    if "status" in data:
        task.status = data["status"]

    db.session.commit()
    
    # Erfolgsmeldung zurückgeben
    return jsonify({"message": "Task aktualisiert", "task": task.to_json()}), 200

# ---------- USERS ----------
# -------------------------------
# 6) Benutzer erstellen (POST)
# -------------------------------
@app.route("/users", methods=["POST"])
def create_user():
    # JSON-Daten lesen
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Keine Daten empfangen"}), 400

    username = (data.get("username") or "").strip()
    password = (data.get("password") or "").strip()
    
    # Pflichtfelder prüfen
    if not username or not password:
        return jsonify({"error": "username und password sind Pflichtfelder"}), 400

    # Prüfen, ob Username schon existiert
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Benutzername existiert bereits"}), 400
    
    # Neuen Benutzer anlegen
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Benutzer erstellt", "user": new_user.to_json()}), 201


# -------------------------------
# 7) Alle Benutzer anzeigen (GET)
# -------------------------------
@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([u.to_json() for u in users]), 200

#Das was soll ich in Terminal schreiben
"""
# Alle Tasks
Invoke-RestMethod -Method GET -Uri http://127.0.0.1:5000/tasks

# Task anlegen
$body = @{ title="Neue Aufgabe"; description="Test"; status="To Do" } | ConvertTo-Json
Invoke-RestMethod -Method POST -Uri http://127.0.0.1:5000/tasks -ContentType "application/json" -Body $body

# Task updaten (Beispiel: ID 1)
$upd = @{ title="Neue Aufgabe (bearbeitet)"; status="Done" } | ConvertTo-Json
Invoke-RestMethod -Method PUT -Uri http://127.0.0.1:5000/tasks/1 -ContentType "application/json" -Body $upd

# Task löschen (Beispiel: ID 1)
Invoke-RestMethod -Method DELETE -Uri http://127.0.0.1:5000/tasks/1

# User anlegen
$u = @{ username="ouissal"; password="1234" } | ConvertTo-Json
Invoke-RestMethod -Method POST -Uri http://127.0.0.1:5000/users -ContentType "application/json" -Body $u

# User anzeigen
Invoke-RestMethod -Method GET -Uri http://127.0.0.1:5000/users
"""

# ⬇️ Tabellen einmalig erstellen (nur beim Start, wenn sie nicht existieren)
with app.app_context():
    db.create_all()


# -------------------------------
# 8) Start des Servers
# -------------------------------
# Diese Zeilen starten den Webserver.
# Wenn du "python app.py" im Terminal eingibst, läuft Flask unter http://127.0.0.1:5000/
if __name__ == "__main__":

    app.run(debug=True)  # debug=True zeigt automatisch Fehler an und lädt beim Speichern neu


    """
    git status
git add .
git commit -m "Refactor: nur User & Task + Routen (SQL-ready)"
git push -u origin main
    """