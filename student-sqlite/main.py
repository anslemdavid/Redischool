import sqlite3
from pathlib import Path
from typing import Dict, List

DB_PATH = Path(__file__).with_name("students.db")


def get_connection() -> sqlite3.Connection:
    """Gibt eine Verbindung zur SQLite-Datenbank zurück."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def create_students_table() -> None:
    """Erstellt die students-Tabelle, falls sie noch nicht existiert."""
    conn = get_connection()
    try:
        with conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER,
                    course TEXT
                )
                """
            )
    finally:
        conn.close()


def insert_students() -> None:
    """Fügt Beispieldaten ein, wenn die Tabelle noch leer ist."""
    students = [
        ("Anna Schmidt", 22, "Python"),
        ("Max Müller", 25, "Data Science"),
        ("Lisa Weber", 21, "Web Development"),
        ("Tom Becker", 24, "Python"),
    ]

    conn = get_connection()
    try:
        with conn:
            has_students = conn.execute(
                "SELECT 1 FROM students LIMIT 1"
            ).fetchone()
            if has_students is None:
                conn.executemany(
                    "INSERT INTO students (name, age, course) VALUES (?, ?, ?)",
                    students,
                )
    finally:
        conn.close()


def get_all_students() -> List[Dict[str, object]]:
    """Gibt alle Studenten als Liste von Dictionaries zurück."""
    conn = get_connection()
    try:
        rows = conn.execute("SELECT * FROM students").fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def main() -> None:
    """Erstellt die Tabelle, fügt Beispieldaten ein und zeigt alle Studenten."""
    create_students_table()
    insert_students()

    print("Alle Studenten in der Datenbank:")
    for student in get_all_students():
        print(student)


if __name__ == "__main__":
    main()
