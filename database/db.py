import sqlite3
import time

DB = "bot.db"


def connect():
    return sqlite3.connect(DB)


def init_db():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        admin_id INTEGER,
        category TEXT,
        text TEXT,
        status INTEGER DEFAULT 0,
        created_at INTEGER
    )
    """)

    conn.commit()
    conn.close()


# ---------------- CREATE TICKET ----------------
def create_ticket(user_id, admin_id, category, text):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO tickets (user_id, admin_id, category, text, status, created_at)
        VALUES (?, ?, ?, ?, 0, ?)
    """, (user_id, admin_id, category, text, int(time.time())))

    conn.commit()
    ticket_id = cur.lastrowid
    conn.close()

    return ticket_id


# ---------------- GET TICKETS ----------------
def get_tickets():

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM tickets ORDER BY id DESC")
    rows = cur.fetchall()

    conn.close()
    return rows


# ---------------- GET ONE ----------------
def get_ticket(ticket_id):

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM tickets WHERE id=?", (ticket_id,))
    row = cur.fetchone()

    conn.close()
    return row


# ---------------- CLOSE / ANSWER ----------------
def mark_answered(ticket_id):

    conn = connect()
    cur = conn.cursor()

    cur.execute("UPDATE tickets SET status=1 WHERE id=?", (ticket_id,))

    conn.commit()
    conn.close()


# ---------------- STATS ----------------
def get_stats():

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM tickets")
    total = cur.fetchone()[0]

    cur.execute("""
        SELECT category, COUNT(*)
        FROM tickets
        GROUP BY category
    """)

    by_cat = cur.fetchall()

    conn.close()
    return total, by_cat
