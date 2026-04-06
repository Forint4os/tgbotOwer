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
    conn.commit()

def add_message(from_user, to_user, category, text):
    cursor.execute(
        "INSERT INTO messages (from_user, to_user, category, text, status) VALUES (?, ?, ?, ?, ?)",
        (from_user, to_user, category, text, '🆕')
    )
    conn.commit()
    return cursor.lastrowid

def get_messages_for_admin(admin_id):
    cursor.execute(
        "SELECT id, from_user, category, text, status FROM messages WHERE to_user=? ORDER BY id DESC",
        (admin_id,)
    )
    return cursor.fetchall()

def get_messages_by_category(admin_id, category):
    cursor.execute(
        "SELECT id, from_user, category, text, status FROM messages WHERE to_user=? AND category=? ORDER BY id DESC",
        (admin_id, category)
    )
    return cursor.fetchall()

def get_message_by_id(msg_id):
    cursor.execute(
        "SELECT id, from_user, category, text, status FROM messages WHERE id=?",
        (msg_id,)
    )
    return cursor.fetchone()

def update_message_status(msg_id, status):
    cursor.execute("UPDATE messages SET status=? WHERE id=?", (status, msg_id))
    conn.commit()

def get_stats(admin_id):
    cursor.execute("SELECT COUNT(*) FROM messages WHERE to_user=?", (admin_id,))
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM messages WHERE to_user=? AND status='🆕'", (admin_id,))
    new = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM messages WHERE to_user=? AND status='✅'", (admin_id,))
    done = cursor.fetchone()[0]

    cursor.execute("""
        SELECT category, COUNT(*) 
        FROM messages 
        WHERE to_user=? 
        GROUP BY category
    """, (admin_id,))
    categories = cursor.fetchall()

    return total, new, done, categories