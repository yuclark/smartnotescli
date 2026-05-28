import sqlite3
import os
from datetime import datetime
from core.logger import log_info, log_error

DB_NAME = "notes.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    category TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'Todo',
                    created_at TEXT NOT NULL,
                    is_deleted INTEGER DEFAULT 0
                )
            """)
            conn.commit()
            log_info("Database initialized successfully.")
    except Exception as e:
        log_error(f"Failed to initialize database: {e}")

def add_note(content: str, category: str, priority: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO notes (content, category, priority, status, created_at) 
            VALUES (?, ?, ?, 'Todo', ?)
        """, (content, category, priority, timestamp))
        conn.commit()
        log_info(f"Note added with category '{category}' and priority '{priority}'")

def get_active_notes():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, content, category, priority, status, created_at FROM notes WHERE is_deleted = 0 ORDER BY id DESC")
        return cursor.fetchall()

def update_status(note_id: int, new_status: str):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE notes SET status = ? WHERE id = ? AND is_deleted = 0", (new_status, note_id))
        conn.commit()
        log_info(f"Updated Note ID {note_id} status to {new_status}")

def soft_delete_note(note_id: int):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE notes SET is_deleted = 1 WHERE id = ?", (note_id,))
        conn.commit()
        log_info(f"Soft deleted Note ID {note_id}")

def get_trash_notes():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, content, category FROM notes WHERE is_deleted = 1 ORDER BY id DESC")
        return cursor.fetchall()

def restore_note(note_id: int):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE notes SET is_deleted = 0 WHERE id = ?", (note_id,))
        conn.commit()
        log_info(f"Restored Note ID {note_id} from trash bin")

def search_notes(keyword: str):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, content, category, priority, status, created_at 
            FROM notes 
            WHERE is_deleted = 0 AND (content LIKE ? OR category LIKE ? OR priority LIKE ?)
            ORDER BY id DESC
        """, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
        return cursor.fetchall()

def get_analytics_payload():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT category, COUNT(*) FROM notes WHERE is_deleted = 0 GROUP BY category")
        cat_stats = cursor.fetchall()
        cursor.execute("SELECT status, COUNT(*) FROM notes WHERE is_deleted = 0 GROUP BY status")
        status_stats = cursor.fetchall()
        return cat_stats, status_stats