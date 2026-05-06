import sqlite3
import os
import pandas as pd
DB_PATH = "data/choir.db"

def connect_db():
    os.makedirs("data", exist_ok=True)
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def create_tables():
    conn = connect_db()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS choir_data (
        id INTEGER PRIMARY KEY,
        choir TEXT,
        name TEXT,
        identification_no TEXT UNIQUE,
        gender TEXT,
        status TEXT DEFAULT 'alive',
        comment TEXT DEFAULT ''
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS graduation_data (
        id INTEGER PRIMARY KEY,
        name TEXT,
        identification_no TEXT,
        institute TEXT,
        course_name TEXT,
        duration TEXT,
        year_of_graduation INTEGER
    )
    """)
    
    conn.commit()
    conn.close()

def clean_choir_duplicates():
    conn = connect_db()

    df = pd.read_sql("SELECT * FROM choir_data", conn)

    # normalize IDs FIRST
    df["identification_no"] = df["identification_no"].astype(str).str.strip().str.lower()

    # keep first occurrence only
    df = df.drop_duplicates(subset=["identification_no"], keep="first")

    # replace table
    df.to_sql("choir_data", conn, if_exists="replace", index=False)

    conn.close()
