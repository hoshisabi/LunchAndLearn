#!/usr/bin/env python3
"""
Database seeding script for LunchAndLearn application.
Seeds the SQLite database with initial issue data.
"""

import sqlite3
import os
import sys


def seed_database(db_path: str = "issues.db"):
    """
    Seeds the Issues table with initial data if the table is empty.
    
    Args:
        db_path: Path to the SQLite database file
    """
    # Check if database exists
    if not os.path.exists(db_path):
        print(f"Database file '{db_path}' not found. Please ensure the database is created first.")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Issues'")
        if not cursor.fetchone():
            print("Table 'Issues' does not exist. Please run the application first to create the database schema.")
            conn.close()
            return False
        
        # Check if table already has data
        cursor.execute("SELECT COUNT(*) FROM Issues")
        count = cursor.fetchone()[0]
        
        if count > 0:
            print(f"Database already contains {count} issue(s). Skipping seed.")
            conn.close()
            return True
        
        # Seed data
        issues = [
            ("ISSUE-001", "Login button not working", 
             "Users report that the login button is unresponsive on mobile devices.", 0),
            ("ISSUE-002", "Performance lag", 
             "App slows down after extended use, possibly due to memory leak.", 1),
            ("ISSUE-003", "UI misalignment", 
             "Elements are misaligned on high-resolution screens.", 0),
            ("ISSUE-004", "Security vulnerability", 
             "Potential SQL injection in search query.", 1),
            ("ISSUE-005", "Feature request: Dark mode", 
             "Users want a dark mode toggle.", 0),
        ]
        
        cursor.executemany(
            "INSERT INTO Issues (Code, ShortDescription, LongDescription, IsUrgent) VALUES (?, ?, ?, ?)",
            issues
        )
        
        conn.commit()
        print(f"Successfully seeded {len(issues)} issues into the database.")
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
    
    success = seed_database(db_path)
    sys.exit(0 if success else 1)

