#!/usr/bin/env python3
"""
Database seeding script for LunchAndLearn application.
Seeds the SQLite database with initial issue data from CSV file.
"""

import sqlite3
import csv
import os
import sys


def seed_database(db_path: str = "issues.db"):
    """
    Seeds the Issues table with data from issues.csv if the table is empty.
    
    Args:
        db_path: Path to the SQLite database file
    """
    # Check if database exists
    if not os.path.exists(db_path):
        print(f"Database file '{db_path}' not found. Please ensure the database is created first.")
        return False
    
    csv_path = os.path.join(os.path.dirname(db_path), "issues.csv")
    if not os.path.exists(csv_path):
        print(f"CSV file '{csv_path}' not found.")
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
        
        # Read from CSV file
        issues = []
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                issues.append((
                    row['Code'],
                    row['ShortDescription'],
                    row['LongDescription'],
                    row['Priority']
                ))
        
        cursor.executemany(
            "INSERT INTO Issues (Code, ShortDescription, LongDescription, Priority) VALUES (?, ?, ?, ?)",
            issues
        )
        
        conn.commit()
        print(f"Successfully seeded {len(issues)} issues from CSV into the database.")
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

