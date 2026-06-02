import sqlite3
import os


def get_db_path():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(base_dir, "shadow", "shadow.db")


def init_db():
    path = get_db_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)

    conn = sqlite3.connect(path)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

def add_password(service, password):
    conn = sqlite3.connect(get_db_path())
    cur = conn.cursor()

    cur.execute("""
        INSERT OR REPLACE INTO passwords (service, password)
        VALUES (?, ?)
    """, (service, password))

    conn.commit()
    conn.close()

def update_password(service, password):
    conn = sqlite3.connect(get_db_path())
    cur = conn.cursor()

    cur.execute("""
        UPDATE passwords
        SET password = ?
        WHERE service = ?
    """, (password, service))

    conn.commit()
    conn.close()

def get_all_services():
    conn = sqlite3.connect(get_db_path())
    cur = conn.cursor()

    cur.execute("SELECT service FROM passwords")
    rows = cur.fetchall()

    conn.close()
    return [r[0] for r in rows]

def get_password(service):
    conn = sqlite3.connect(get_db_path())
    cur = conn.cursor()

    cur.execute("SELECT password FROM passwords WHERE service = ?", (service,))
    row = cur.fetchone()

    conn.close()
    return row[0] if row else None