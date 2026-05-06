import sqlite3
import os
import pandas as pd
import bcrypt

DB_PATH = "data/choir.db"

def connect_db(row_factory=False):
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    if row_factory:
        conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = connect_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS choir_data (
            id INTEGER PRIMARY KEY,
            identification_no TEXT UNIQUE,
            name TEXT,
            choir TEXT,
            gender TEXT,
            status TEXT DEFAULT 'alive',
            comment TEXT DEFAULT ''
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS graduation_data (
            id INTEGER PRIMARY KEY,
            identification_no TEXT,
            name TEXT,
            institute TEXT,
            course_name TEXT,
            duration TEXT,
            year_of_graduation INTEGER
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'viewer',
            created_at TEXT DEFAULT (datetime('now')),
            created_by TEXT
        )
    """)

    # ── SEED DEFAULT ADMIN ──
    existing = conn.execute(
        "SELECT * FROM users WHERE username = 'admin'"
    ).fetchone()
    if not existing:
        hashed = bcrypt.hashpw(b"admin123", bcrypt.gensalt()).decode()
        conn.execute("""
            INSERT INTO users (username, password_hash, role, created_by)
            VALUES (?, ?, 'admin', 'system')
        """, ("admin", hashed))

    conn.commit()
    conn.close()

def clean_choir_duplicates():
    conn = connect_db()
    df = pd.read_sql("SELECT * FROM choir_data", conn)
    df["identification_no"] = df["identification_no"].astype(str).str.strip().str.lower()
    df = df.drop_duplicates(subset=["identification_no"], keep="first")
    df.to_sql("choir_data", conn, if_exists="replace", index=False)
    conn.close()