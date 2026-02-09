import sqlite3
import uuid

DB_NAME = "verifier_b.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS nonces (
            nonce TEXT PRIMARY KEY
        )
    """)

    conn.commit()
    conn.close()


def generate_nonce():
    nonce = str(uuid.uuid4())

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO nonces (nonce) VALUES (?)", (nonce,))
    conn.commit()
    conn.close()

    return nonce


def consume_nonce(nonce: str) -> bool:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT nonce FROM nonces WHERE nonce = ?", (nonce,))
    row = cur.fetchone()

    if row is None:
        conn.close()
        return False

    cur.execute("DELETE FROM nonces WHERE nonce = ?", (nonce,))
    conn.commit()
    conn.close()
    return True
