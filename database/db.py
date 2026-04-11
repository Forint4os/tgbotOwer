import sqlite3

conn = sqlite3.connect("bot.db")
cursor = conn.cursor()


def init_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        username TEXT,
        category TEXT,
        text TEXT,
        answered INTEGER DEFAULT 0
    )
    """)
    conn.commit()


def add_ticket(user_id, username, category, text):
    cursor.execute("""
    INSERT INTO tickets (user_id, username, category, text)
    VALUES (?, ?, ?, ?)
    """, (user_id, username, category, text))
    conn.commit()

    return cursor.lastrowid


def get_tickets():
    cursor.execute("SELECT * FROM tickets ORDER BY id DESC LIMIT 20")
    return cursor.fetchall()


def get_ticket(ticket_id):
    cursor.execute("SELECT * FROM tickets WHERE id=?", (ticket_id,))
    return cursor.fetchone()


def mark_answered(ticket_id):
    cursor.execute("UPDATE tickets SET answered=1 WHERE id=?", (ticket_id,))
    conn.commit()
