import unittest
import sqlite3
from core.tagger import analyze_content
import core.database as db

class TestSmartNotesSystem(unittest.TestCase):
    
    def setUp(self):
        # Override the database config to target an in-memory instance for testing
        db.DB_NAME = ":memory:"
        db.init_db()

    def test_tagger_heuristics(self):
        category, priority = analyze_content("Fix the bug inside my django backend codebase immediately ASAP")
        self.assertEqual(category, "Coding")
        self.assertEqual(priority, "High")

    def test_database_lifecycle(self):
        db.add_note("Sample system unit processing context statement.", "Testing", "Low")
        records = db.get_active_notes()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0][2], "Testing") # Verifying Category storage
        
        # Test soft deletion cycle
        note_id = records[0][0]
        db.soft_delete_note(note_id)
        self.assertEqual(len(db.get_active_notes()), 0)
        self.assertEqual(len(db.get_trash_notes()), 1)

if __name__ == "__main__":
    unittest.main()