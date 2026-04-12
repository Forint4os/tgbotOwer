import sqlite3

conn = sqlite3.connect("bot.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    category TEXT,
    text TEXT
)
""")

conn.commit()

def create_ticket(user_id, category, text):
    cursor.execute(
        "INSERT INTO tickets (user_id, category, text) VALUES (?, ?, ?)",
        (user_id, category, text)
    )
    conn.commit()

def get_tickets():
    cursor.execute("SELECT * FROM tickets")
    return cursor.fetchall()
