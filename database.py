import sqlite3
import os
import pandas as pd
import bcrypt
import streamlit as st
from pathlib import Path

# Use a more persistent location - for Streamlit Cloud, use the app's root directory
# Streamlit Cloud allows file persistence in the app directory
DB_PATH = "choir_data.db"  # Use root directory instead of data/ subfolder

def connect_db(row_factory=False):
    """Connect to SQLite database with proper error handling"""
    try:
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        if row_factory:
            conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        st.error(f"Database connection error: {str(e)}")
        raise

def create_tables():
    """Create all necessary tables if they don't exist"""
    try:
        conn = connect_db()
        
        # Enable foreign keys
        conn.execute("PRAGMA foreign_keys = ON")
        
        # Create choir_data table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS choir_data (
                identification_no TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                choir TEXT NOT NULL,
                gender TEXT,
                status TEXT DEFAULT 'alive',
                comment TEXT DEFAULT '',
                graduated BOOLEAN DEFAULT 0
            )
        """)
        
        # Create graduation_data table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS graduation_data (
                id_grad INTEGER PRIMARY KEY AUTOINCREMENT,
                identification_no TEXT,
                name TEXT,
                institute TEXT,
                course_name TEXT,
                duration TEXT,
                year_of_graduation INTEGER,
                FOREIGN KEY (identification_no) REFERENCES choir_data(identification_no)
            )
        """)
        
        # Create users table
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
        
        # Create index for faster lookups
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_choir_name 
            ON choir_data(name)
        """)
        
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_choir_id 
            ON choir_data(identification_no)
        """)
        
        # Seed default admin user if not exists
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
        
    except Exception as e:
        st.error(f"Error creating tables: {str(e)}")
        raise

def clean_choir_duplicates():
    """Remove duplicate entries based on identification number"""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        
        # Get all records
        cursor.execute("SELECT identification_no, MIN(rowid) as min_id FROM choir_data GROUP BY identification_no")
        keep_ids = [row[1] for row in cursor.fetchall()]
        
        if keep_ids:
            # Delete duplicates
            cursor.execute(f"""
                DELETE FROM choir_data 
                WHERE rowid NOT IN ({','.join('?' * len(keep_ids))})
            """, keep_ids)
            
        conn.commit()
        conn.close()
        
    except Exception as e:
        st.error(f"Error cleaning duplicates: {str(e)}")
        raise

def backup_database():
    """Create a backup of the database"""
    try:
        import shutil
        from datetime import datetime
        
        if os.path.exists(DB_PATH):
            backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{DB_PATH}"
            shutil.copy2(DB_PATH, backup_name)
            return backup_name
    except Exception as e:
        st.warning(f"Backup failed: {str(e)}")
        return None

def get_db_size():
    """Get database file size"""
    if os.path.exists(DB_PATH):
        size = os.path.getsize(DB_PATH)
        if size < 1024:
            return f"{size} bytes"
        elif size < 1024 * 1024:
            return f"{size / 1024:.2f} KB"
        else:
            return f"{size / (1024 * 1024):.2f} MB"
    return "0 bytes"

# Add this to check database health
def verify_database():
    """Verify database integrity"""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        
        # Check if tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        required_tables = ['choir_data', 'graduation_data', 'users']
        existing_tables = [t[0] for t in tables]
        
        missing_tables = [t for t in required_tables if t not in existing_tables]
        
        if missing_tables:
            st.warning(f"Missing tables: {missing_tables}. Recreating...")
            create_tables()
            return False
            
        # Check row counts
        for table in required_tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            st.sidebar.info(f"{table}: {count} records")
        
        conn.close()
        return True
        
    except Exception as e:
        st.error(f"Database verification failed: {str(e)}")
        return False
