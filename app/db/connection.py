import sqlite3

DB_NAME = "vnpr.db"

def get_connection():
    conn = sqlite3.connect(
        "vnpr.db",
        timeout=30,
        check_same_thread=False
    )
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn 