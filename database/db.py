import sqlite3

conn = sqlite3.connect("bot.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    category TEXT,
    message TEXT,
    status TEXT DEFAULT 'open'
)
""")

conn.commit()


def create_ticket(user_id, category, message):
    cursor.execute(
        "INSERT INTO tickets (user_id, category, message) VALUES (?, ?, ?)",
        (user_id, category, message)
    )
    conn.commit()
    return cursor.lastrowid


def get_tickets():
    cursor.execute("SELECT * FROM tickets WHERE status='open'")
    return cursor.fetchall()


def get_ticket_by_id(ticket_id):
    cursor.execute("SELECT * FROM tickets WHERE id=?", (ticket_id,))
    return cursor.fetchone()


def close_ticket(ticket_id):
    cursor.execute("UPDATE tickets SET status='closed' WHERE id=?", (ticket_id,))
    conn.commit()


def get_stats():
    cursor.execute("SELECT category, COUNT(*) FROM tickets GROUP BY category")
    return cursor.fetchall()
