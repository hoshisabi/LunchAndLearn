#!/usr/bin/env python3
"""
Migration script to add a Priority column to the Issues table and populate it
based on the previous IsUrgent boolean field.

Rules:
- If IsUrgent == 1 (True)  => Priority = 2 (High)
- If IsUrgent == 0 (False) => Priority = 0 (Low)

This script is idempotent: running it multiple times is safe.
"""

import sqlite3
import os
import sys


def migrate(db_path: str = "issues.db") -> bool:
    if not os.path.exists(db_path):
        print(f"Database file '{db_path}' not found.")
        return False

    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        # Ensure Issues table exists
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Issues'")
        if not cur.fetchone():
            print("Table 'Issues' does not exist. Nothing to migrate.")
            conn.close()
            return True

        # Check existing columns
        cur.execute("PRAGMA table_info(Issues)")
        columns = {row[1] for row in cur.fetchall()}  # row[1] is column name

        # Add Priority column if missing
        if "Priority" not in columns:
            print("Adding 'Priority' column to Issues table...")
            cur.execute("ALTER TABLE Issues ADD COLUMN Priority INTEGER NOT NULL DEFAULT 1")
            conn.commit()
        else:
            print("'Priority' column already exists. Skipping add column step.")

        # Populate Priority values from IsUrgent when present
        if "IsUrgent" in columns:
            print("Backfilling 'Priority' from 'IsUrgent' values...")
            # IsUrgent = 1 -> Priority = 2 (High)
            cur.execute("UPDATE Issues SET Priority = 2 WHERE IsUrgent = 1")
            # IsUrgent = 0 -> Priority = 0 (Low)
            cur.execute("UPDATE Issues SET Priority = 0 WHERE IsUrgent = 0")
            conn.commit()
        else:
            print("'IsUrgent' column not found. Assuming Priority already populated or new schema in use.")

        # Note: We intentionally keep 'IsUrgent' for backwards compatibility.
        # Dropping columns in SQLite may not be supported depending on version.
        print("Migration completed successfully.")
        conn.close()
        return True

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False


if __name__ == "__main__":
    db_path = sys.argv[1] if len(sys.argv) > 1 else "issues.db"
    success = migrate(db_path)
    sys.exit(0 if success else 1)
