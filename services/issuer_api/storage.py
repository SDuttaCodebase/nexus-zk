import sqlite3

DB_NAME = "issuer.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS credentials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            payload TEXT,
            signature TEXT,
            revocation_hash TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS revocations (
            revocation_hash TEXT PRIMARY KEY
        )
    """)

    conn.commit()
    conn.close()
