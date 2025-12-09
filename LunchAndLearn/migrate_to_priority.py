#!/usr/bin/env python3
"""
Migration script for upgrading IsUrgent boolean to Priority enum.
Reads from issues.csv and migrates data to the database with automatic backups.
"""

import sqlite3
import csv
import os
import sys
import shutil
from datetime import datetime


def create_backups(db_path: str, csv_path: str) -> tuple:
    """
    Create backups of the database and CSV file with timestamps.
    
    Args:
        db_path: Path to the database file
        csv_path: Path to the CSV file
        
    Returns:
        Tuple of (backup_db_path, backup_csv_path)
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    db_dir = os.path.dirname(db_path) if os.path.dirname(db_path) else "."
    csv_dir = os.path.dirname(csv_path) if os.path.dirname(csv_path) else "."
    
    backup_db = os.path.join(db_dir, f"issues_backup_{timestamp}.db")
    backup_csv = os.path.join(csv_dir, f"issues_backup_{timestamp}.csv")
    
    if os.path.exists(db_path):
        shutil.copy2(db_path, backup_db)
    if os.path.exists(csv_path):
        shutil.copy2(csv_path, backup_csv)
    
    return backup_db, backup_csv


def restore_from_backup(db_path: str, backup_db: str):
    """Restore database from backup."""
    if os.path.exists(backup_db):
        shutil.copy2(backup_db, db_path)


def migrate_to_priority(db_path: str = "issues.db", csv_path: str = None) -> bool:
    """
    Migrate database from IsUrgent to Priority column.
    Reads from CSV file and populates the database.
    
    Args:
        db_path: Path to the SQLite database file
        csv_path: Path to the CSV file (defaults to same directory as db)
        
    Returns:
        True if successful, False otherwise
    """
    if csv_path is None:
        csv_path = os.path.join(os.path.dirname(db_path) if os.path.dirname(db_path) else ".", "issues.csv")
    
    # Validate files exist
    if not os.path.exists(db_path):
        print(f"Error: Database file '{db_path}' not found.")
        return False
    
    if not os.path.exists(csv_path):
        print(f"Error: CSV file '{csv_path}' not found.")
        return False
    
    try:
        # Create backups
        print("Creating backups...")
        backup_db, backup_csv = create_backups(db_path, csv_path)
        print(f"  Database backup: {backup_db}")
        print(f"  CSV backup: {backup_csv}")
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if table exists and has Priority column
        cursor.execute("PRAGMA table_info(Issues)")
        columns = {row[1] for row in cursor.fetchall()}
        
        if "Priority" not in columns:
            print("Error: Priority column not found. Ensure database schema is updated first.")
            restore_from_backup(db_path, backup_db)
            conn.close()
            return False
        
        # Clear existing data
        cursor.execute("SELECT COUNT(*) FROM Issues")
        existing_count = cursor.fetchone()[0]
        
        if existing_count > 0:
            print(f"Clearing {existing_count} existing issue(s)...")
            cursor.execute("DELETE FROM Issues")
        
        # Read and insert from CSV
        print(f"Reading from CSV: {csv_path}")
        issues = []
        priority_counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
        
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                priority = row.get('Priority', 'MEDIUM').upper()
                if priority not in priority_counts:
                    priority = 'MEDIUM'
                priority_counts[priority] += 1
                
                issues.append((
                    row['Code'],
                    row['ShortDescription'],
                    row['LongDescription'],
                    priority
                ))
        
        # Insert all issues
        cursor.executemany(
            "INSERT INTO Issues (Code, ShortDescription, LongDescription, Priority) VALUES (?, ?, ?, ?)",
            issues
        )
        
        conn.commit()
        conn.close()
        
        # Report statistics
        print(f"\nMigration successful!")
        print(f"Total issues migrated: {len(issues)}")
        print(f"  HIGH priority: {priority_counts['HIGH']}")
        print(f"  MEDIUM priority: {priority_counts['MEDIUM']}")
        print(f"  LOW priority: {priority_counts['LOW']}")
        print(f"\nTo rollback, restore from: {backup_db}")
        
        return True
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        if 'backup_db' in locals() and os.path.exists(backup_db):
            print(f"Restoring from backup: {backup_db}")
            restore_from_backup(db_path, backup_db)
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        if 'backup_db' in locals() and os.path.exists(backup_db):
            print(f"Restoring from backup: {backup_db}")
            restore_from_backup(db_path, backup_db)
        return False


def rollback(backup_db: str, db_path: str):
    """
    Rollback to a backup.
    
    Args:
        backup_db: Path to the backup database file
        db_path: Path to restore to
    """
    if not os.path.exists(backup_db):
        print(f"Backup file not found: {backup_db}")
        return False
    
    try:
        restore_from_backup(db_path, backup_db)
        print(f"Restored from backup: {backup_db}")
        return True
    except Exception as e:
        print(f"Rollback failed: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--rollback":
        if len(sys.argv) < 3:
            print("Usage: python migrate_to_priority.py --rollback <backup_db_path>")
            sys.exit(1)
        success = rollback(sys.argv[2], "issues.db")
    else:
        db_path = sys.argv[1] if len(sys.argv) > 1 else "issues.db"
        csv_path = sys.argv[2] if len(sys.argv) > 2 else None
        success = migrate_to_priority(db_path, csv_path)
    
    sys.exit(0 if success else 1)

