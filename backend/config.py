# ===============================
# config.py
# ===============================

# Diese Datei enthält die Konfiguration für Flask,
# insbesondere die Einstellungen für die Datenbank.

import os  # os = erlaubt uns, Pfade zu erstellen oder Umgebungsvariablen zu lesen

class Config:
    """
    Die Config-Klasse speichert alle wichtigen Einstellungen für unsere Flask-App.
    Flask liest diese Werte später über app.config.from_object(Config)
    """

    # -------------------------------
    # 1) Verbindungs-URL der Datenbank
    # -------------------------------
    # Wir benutzen SQLite → eine Datei "app.db" in deinem Backend-Ordner.
    # sqlite:/// bedeutet:
    #   - 3 / = relativer Pfad
    #   - "app.db" = Name der Datenbankdatei
    #
    # Das ist perfekt für lokale Entwicklung.
    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"

    # -------------------------------
    # 2) SQLAlchemy Warnung ausschalten
    # -------------------------------
    # Flask will uns sonst eine unnötige Warnung anzeigen.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # -------------------------------
    # 3) (Optional) Debug-Ausgabe
    # -------------------------------
    # Du kannst das ändern, aber standardmäßig ist es ok.
    DEBUG = True