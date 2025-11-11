# config.py
# ===============================
# Diese Datei speichert alle wichtigen Konfigurationen deiner Flask-App.
# Hier sagst du Flask, welche Datenbank du benutzt und wo sie sich befindet.
# ===============================

import os  # Das "os"-Modul hilft, Dateipfade zu erstellen, die auf jedem System funktionieren.

# BASE_DIR = absoluter Pfad zum aktuellen Projektordner (Backend)
# Beispiel: "C:\Users\hilcomputer\OneDrive\Bureau\Aufgaben_manager\Backend"
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Jetzt erstellen wir eine Klasse "Config".
# Flask kann diese Klasse automatisch lesen, um Einstellungen zu übernehmen.
class Config:
    # SQLALCHEMY_DATABASE_URI → sagt Flask, welche Datenbank wir verwenden.
    # "sqlite:///" bedeutet, dass wir SQLite nutzen (eine lokale Datei-Datenbank).
    # Danach fügen wir den Pfad zur Datei "app.db" hinzu, die im Backend-Ordner liegt.
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "app.db")

    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Diese Zeile schaltet eine unnötige Warnung aus.
    # (Sie würde sonst bei jeder kleinen Änderung in der DB im Terminal erscheinen.)
    SQLALCHEMY_TRACK_MODIFICATIONS = False