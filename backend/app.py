# ===============================
# app.py
# ===============================
# Diese Datei startet den Flask-Webserver und definiert die "Routen" (URLs),
# über die der Client (z. B. dein Browser oder PowerShell) mit dem Backend kommuniziert.

from flask import Flask, jsonify, request   # Flask = Web-Framework, jsonify = JSON-Antworten, request = Eingaben lesen
from models import User, Task               # Wir importieren NUR unsere beiden Klassen: User und Task

# ===============================
# Flask-Anwendung erstellen
# ===============================
app = Flask(__name__)  # Erstellt eine Instanz der Flask-App → das Herz deines Webservers

# ===============================
# "Datenbank" (in-memory)
# ===============================
# Wir speichern Benutzer und Aufgaben nur im Arbeitsspeicher.
# D.h. die Daten verschwinden, sobald du den Server stoppst (später evtl. echte DB).
users = []  # Liste aller Benutzer
tasks = [   # Beispiel-Aufgaben
    Task(1, "Bericht schreiben", "Monatsbericht für den Chef erstellen", "Doing"),
    Task(2, "Präsentation vorbereiten", "Folien für Meeting am Montag", "To Do"),
    Task(3, "Code überprüfen", "Backend testen und Kommentare ergänzen", "Done"),
]

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
    # Gibt alle Aufgaben zurück, jede als Dictionary (über to_json())
    return jsonify([t.to_json() for t in tasks]), 200


# -------------------------------
# 3) Neue Aufgabe hinzufügen (POST)
# -------------------------------
@app.route("/tasks", methods=["POST"])
def add_task():
    # JSON-Daten vom Client lesen
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Keine Daten empfangen"}), 400

    # Felder auslesen, mit Standardwerten
    title = (data.get("title") or "").strip()
    description = data.get("description") or ""
    status = data.get("status", "To Do")

    # Pflichtfeld-Check
    if not title:
        return jsonify({"error": "title ist Pflicht"}), 400

    # Neue ID generieren (letzte ID + 1)
    new_id = tasks[-1].id + 1 if tasks else 1

    # Neues Task-Objekt erstellen
    new_task = Task(new_id, title, description, status)
    tasks.append(new_task)  # Zur Liste hinzufügen

    # Erfolgsantwort zurückgeben
    return jsonify({"message": "Aufgabe hinzugefügt!", "task": new_task.to_json()}), 201


# -------------------------------
# 4) Aufgabe löschen (DELETE)
# -------------------------------
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks  # Wir bearbeiten die globale Liste
    # Gesuchte Aufgabe nach ID finden
    task_to_delete = next((t for t in tasks if t.id == task_id), None)
    if task_to_delete is None:
        return jsonify({"error": f"Task mit ID {task_id} wurde nicht gefunden"}), 404

    # Liste neu aufbauen (ohne die gelöschte Aufgabe)
    tasks = [t for t in tasks if t.id != task_id]
    return jsonify({"message": f"Task mit ID {task_id} erfolgreich gelöscht"}), 200


# -------------------------------
# 5) Aufgabe aktualisieren (PUT)
# -------------------------------
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    # Neue Daten aus Anfrage holen
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Keine Daten empfangen"}), 400

    # Gesuchte Aufgabe finden
    task = next((t for t in tasks if t.id == task_id), None)
    if task is None:
        return jsonify({"error": f"Task mit ID {task_id} wurde nicht gefunden"}), 404

    # Felder aktualisieren, falls im JSON enthalten
    if "title" in data:
        new_title = (data["title"] or "").strip()
        if not new_title:
            return jsonify({"error": "title darf nicht leer sein"}), 400
        task.title = new_title

    if "description" in data:
        task.description = data["description"] or ""

    if "status" in data:
        task.status = data["status"]  # optional: hier prüfen, ob erlaubt

    # Erfolgsmeldung zurückgeben
    return jsonify({"message": "Task erfolgreich aktualisiert!", "task": task.to_json()}), 200


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
    if any(u.username == username for u in users):
        return jsonify({"error": "Benutzername existiert bereits"}), 400

    # Neuen Benutzer anlegen
    new_id = len(users) + 1
    new_user = User(new_id, username, password)
    users.append(new_user)

    # Erfolgsantwort zurückgeben
    return jsonify({"message": "Benutzer erfolgreich erstellt", "user": new_user.to_json()}), 201


# -------------------------------
# 7) Alle Benutzer anzeigen (GET)
# -------------------------------
@app.route("/users", methods=["GET"])
def get_users():
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