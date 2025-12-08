#!/usr/bin/env python3
"""
Database migration script for LunchAndLearn application.
Migrates existing databases from IsUrgent (boolean) to Priority (enum).

This script performs an in-place upgrade:
1. Adds a new Priority column (if it doesn't exist)
2. Migrates data: IsUrgent=True -> Priority=High, IsUrgent=False -> Priority=Low
3. Removes the old IsUrgent column
"""

import sqlite3
import os
import sys


def migrate_database(db_path: str = "issues.db"):
    """
    Migrates the database from IsUrgent boolean to Priority enum.
    
    Args:
        db_path: Path to the SQLite database file
        
    Returns:
        True if migration succeeded, False otherwise
    """
    # Check if database exists
    if not os.path.exists(db_path):
        print(f"Database file '{db_path}' not found. Nothing to migrate.")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Issues'")
        if not cursor.fetchone():
            print("Table 'Issues' does not exist. Nothing to migrate.")
            conn.close()
            return False
        
        # Check current schema
        cursor.execute("PRAGMA table_info(Issues)")
        columns = {row[1]: row[2] for row in cursor.fetchall()}
        
        # Check if migration is needed
        has_priority = "Priority" in columns
        has_is_urgent = "IsUrgent" in columns
        
        if has_priority and not has_is_urgent:
            print("Database already migrated. Priority column exists and IsUrgent is removed.")
            conn.close()
            return True
        
        if not has_is_urgent:
            print("Database schema doesn't have IsUrgent column. Migration may not be needed.")
            # If Priority doesn't exist, add it with default value
            if not has_priority:
                print("Adding Priority column with default value Low...")
                cursor.execute("ALTER TABLE Issues ADD COLUMN Priority INTEGER NOT NULL DEFAULT 0")
                conn.commit()
                print("Migration completed: Added Priority column with default value.")
            conn.close()
            return True
        
        print("Starting migration from IsUrgent to Priority...")
        
        # Step 1: Add Priority column if it doesn't exist
        if not has_priority:
            print("Adding Priority column...")
            cursor.execute("ALTER TABLE Issues ADD COLUMN Priority INTEGER NOT NULL DEFAULT 0")
            conn.commit()
        
        # Step 2: Migrate data: IsUrgent=True -> Priority=2 (High), IsUrgent=False -> Priority=0 (Low)
        print("Migrating data...")
        cursor.execute("""
            UPDATE Issues 
            SET Priority = CASE 
                WHEN IsUrgent = 1 THEN 2  -- High
                WHEN IsUrgent = 0 THEN 0  -- Low
                ELSE 0
            END
        """)
        conn.commit()
        
        # Step 3: Remove the old IsUrgent column
        # SQLite doesn't support DROP COLUMN directly, so we need to recreate the table
        print("Removing IsUrgent column...")
        
        # Get all data
        cursor.execute("SELECT Code, ShortDescription, LongDescription, Priority FROM Issues")
        issues = cursor.fetchall()
        
        # Create new table without IsUrgent
        cursor.execute("""
            CREATE TABLE Issues_new (
                Code TEXT NOT NULL PRIMARY KEY,
                ShortDescription TEXT NOT NULL,
                LongDescription TEXT NOT NULL,
                Priority INTEGER NOT NULL
            )
        """)
        
        # Copy data to new table
        cursor.executemany(
            "INSERT INTO Issues_new (Code, ShortDescription, LongDescription, Priority) VALUES (?, ?, ?, ?)",
            issues
        )
        
        # Drop old table
        cursor.execute("DROP TABLE Issues")
        
        # Rename new table
        cursor.execute("ALTER TABLE Issues_new RENAME TO Issues")
        
        conn.commit()
        print(f"Successfully migrated {len(issues)} issue(s) from IsUrgent to Priority.")
        conn.close()
        return True
        
    except sqlite3.Error as e:
        print(f"Database error during migration: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error during migration: {e}")
        return False


if __name__ == "__main__":
    # Allow custom db path via command line argument
    db_path = sys.argv[1] if len(sys.argv) > 1 else "issues.db"
    
    success = migrate_database(db_path)
    sys.exit(0 if success else 1)

