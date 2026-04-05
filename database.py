import sqlite3

conn = sqlite3.connect("bot.db")
cursor = conn.cursor()

def init_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        from_user INTEGER,
        to_user INTEGER,
        category TEXT,
        text TEXT,
        status TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS replies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message_id INTEGER,
        admin_id INTEGER,
        text TEXT
    )
    """)
    conn.commit()

def add_message(from_user, to_user, category, text):
    cursor.execute(
        "INSERT INTO messages (from_user, to_user, category, text, status) VALUES (?, ?, ?, ?, ?)",
        (from_user, to_user, category, text, '🆕')
    )
    conn.commit()
    return cursor.lastrowid

def get_messages_for_admin(admin_id):
    cursor.execute("SELECT id, from_user, category, text, status FROM messages WHERE to_user=?", (admin_id,))
    return cursor.fetchall()

def update_message_status(msg_id, status):
    cursor.execute("UPDATE messages SET status=? WHERE id=?", (status, msg_id))
    conn.commit()