import sqlite3
import time

DB_NAME = "bot.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        admin_id INTEGER,
        category TEXT,
        message TEXT,
        status INTEGER DEFAULT 0,
        created_at INTEGER
    )
    """)

    conn.commit()
    conn.close()


def create_ticket(user_id, admin_id, category, message):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO tickets (user_id, admin_id, category, message, status, created_at)
        VALUES (?, ?, ?, ?, 0, ?)
    """, (user_id, admin_id, category, message, int(time.time())))

    conn.commit()
    tid = cur.lastrowid
    conn.close()
    return tid


def get_tickets():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        SELECT id, user_id, admin_id, category, message, status, created_at
        FROM tickets
        ORDER BY id DESC
    """)

    rows = cur.fetchall()
    conn.close()
    return rows


def get_stats():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM tickets")
    total = cur.fetchone()[0]

    cur.execute("""
        SELECT category, COUNT(*)
        FROM tickets
        GROUP BY category
    """)

    by_category = cur.fetchall()
    conn.close()

    return {
        "total": total,
        "by_category": by_category
    }
