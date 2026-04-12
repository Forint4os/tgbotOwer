import sqlite3
import time

DB_NAME = "bot.db"


# ---------------- INIT DB ----------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        admin_id INTEGER NOT NULL,
        category TEXT NOT NULL,
        message TEXT NOT NULL,
        status INTEGER DEFAULT 0,
        created_at INTEGER
    )
    """)

    conn.commit()
    conn.close()


# ---------------- CREATE TICKET ----------------
def create_ticket(user_id: int, admin_id: int, category: str, message: str):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO tickets (user_id, admin_id, category, message, status, created_at)
        VALUES (?, ?, ?, ?, 0, ?)
    """, (user_id, admin_id, category, message, int(time.time())))

    conn.commit()

    ticket_id = cur.lastrowid

    conn.close()
    return ticket_id


# ---------------- GET ALL TICKETS ----------------
def get_all_tickets():
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


# ---------------- GET TICKETS BY ADMIN ----------------
def get_tickets_by_admin(admin_id: int):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        SELECT id, user_id, category, message, status
        FROM tickets
        WHERE admin_id = ?
        ORDER BY id DESC
    """, (admin_id,))

    rows = cur.fetchall()
    conn.close()
    return rows


# ---------------- GET SINGLE TICKET ----------------
def get_ticket(ticket_id: int):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        SELECT id, user_id, admin_id, category, message, status, created_at
        FROM tickets
        WHERE id = ?
    """, (ticket_id,))

    row = cur.fetchone()
    conn.close()
    return row


# ---------------- MARK AS ANSWERED ----------------
def mark_answered(ticket_id: int):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        UPDATE tickets
        SET status = 1
        WHERE id = ?
    """, (ticket_id,))

    conn.commit()
    conn.close()


# ---------------- STATS ----------------
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
