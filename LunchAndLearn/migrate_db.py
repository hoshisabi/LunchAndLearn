#!/usr/bin/env python3
"""
Database migration script for LunchAndLearn application.
Migrates the database from using IsUrgent to Priority.
"""

import sqlite3
import os
import sys


def migrate_database(db_path: str = "issues.db"):
    """
    Migrates the Issues table from IsUrgent to Priority.
    
    Args:
        db_path: Path to the SQLite database file
    """
    # Check if database exists
    if not os.path.exists(db_path):
        print(f"Database file '{db_path}' not found. Nothing to migrate.")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if migration is needed by checking for IsUrgent column
        cursor.execute("PRAGMA table_info(Issues)")
        columns = [row[1] for row in cursor.fetchall()]
        if "IsUrgent" not in columns:
            print("Database already migrated. Skipping.")
            conn.close()
            return True

        print("Starting database migration...")

        # Add Priority column
        cursor.execute("ALTER TABLE Issues ADD COLUMN Priority TEXT")
        print("Added Priority column.")

        # Populate Priority column based on IsUrgent
        cursor.execute("UPDATE Issues SET Priority = CASE WHEN IsUrgent = 1 THEN 'HIGH' ELSE 'LOW' END")
        print("Populated Priority column.")

        # We can't drop a column in SQLite, so we'll create a new table and copy the data
        cursor.execute("""
            CREATE TABLE Issues_new (
                Code TEXT PRIMARY KEY,
                ShortDescription TEXT,
                LongDescription TEXT,
                Priority TEXT
            )
        """)
        print("Created new Issues table.")

        cursor.execute("""
            INSERT INTO Issues_new (Code, ShortDescription, LongDescription, Priority)
            SELECT Code, ShortDescription, LongDescription, Priority FROM Issues
        """)
        print("Copied data to new Issues table.")

        cursor.execute("DROP TABLE Issues")
        print("Dropped old Issues table.")

        cursor.execute("ALTER TABLE Issues_new RENAME TO Issues")
        print("Renamed new Issues table to Issues.")
        
        conn.commit()
        print("Successfully migrated database.")
        conn.close()
        return True
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False


if __name__ == "__main__":
    # Allow custom db path via command line argument
    db_path = sys.argv[1] if len(sys.argv) > 1 else "issues.db"
    
    success = migrate_database(db_path)
    sys.exit(0 if success else 1)
