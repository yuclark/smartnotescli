import sqlite3
from datetime import datetime

DB_NAME = "notes.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    """Initializes the database and creates the notes table if it doesn't exist."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                category TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        conn.commit()

def add_note(content: str, category: str):
    """Inserts a new note into the database."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO notes (content, category, created_at) VALUES (?, ?, ?)",
            (content, category, timestamp)
        )
        conn.commit()

def get_all_notes():
    """Fetches all notes."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, content, category, created_at FROM notes ORDER BY id DESC")
        return cursor.fetchall()

def search_notes(keyword: str):
    """Searches notes by content or category."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, content, category, created_at FROM notes WHERE content LIKE ? OR category LIKE ? ORDER BY id DESC",
            (f"%{keyword}%", f"%{keyword}%")
        )
        return cursor.fetchall()

def get_note_by_id(note_id: int):
    """Fetches a single note by its ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, content, category, created_at FROM notes WHERE id = ?", (note_id,))
        return cursor.fetchone()
    
def get_category_stats():
    """Returns a list of tuples containing categories and their respective note counts."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT category, COUNT(*) as count 
            FROM notes 
            GROUP BY category 
            ORDER BY count DESC
        """)
        return cursor.fetchall()