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
    Creates the database and table if they don't exist.
    
    Args:
        db_path: Path to the SQLite database file
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if table exists, create if it doesn't
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Issues'")
        if not cursor.fetchone():
            print(f"Table 'Issues' does not exist. Creating database schema...")
            # Create the Issues table matching Entity Framework schema
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Issues (
                    Code TEXT NOT NULL PRIMARY KEY,
                    ShortDescription TEXT NOT NULL,
                    LongDescription TEXT NOT NULL,
                    IsUrgent INTEGER NOT NULL
                )
            """)
            conn.commit()
            print("Database schema created successfully.")
        
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

