#!/usr/bin/env python3
"""
Database migration script to convert IsUrgent boolean to Priority enum.
Converts IsUrgent=1 to Priority='HIGH' and IsUrgent=0 to Priority='MEDIUM'.
"""

import sqlite3
import os
import sys
from datetime import datetime


def migrate_database(db_path: str = "issues.db", backup: bool = True):
    """
    Migrates the Issues table from IsUrgent (boolean) to Priority (enum).
    
    Args:
        db_path: Path to the SQLite database file
        backup: Whether to create a backup before migration
    
    Returns:
        bool: True if migration successful, False otherwise
    """
    # Check if database exists
    if not os.path.exists(db_path):
        print(f"Database file '{db_path}' not found.")
        return False
    
    try:
        # Create backup if requested
        if backup:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"{db_path}.backup.{timestamp}"
            import shutil
            shutil.copy2(db_path, backup_path)
            print(f"Backup created: {backup_path}")
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Issues'")
        if not cursor.fetchone():
            print("Table 'Issues' does not exist.")
            conn.close()
            return False
        
        # Check if Priority column already exists (migration already done)
        cursor.execute("PRAGMA table_info(Issues)")
        columns = {row[1] for row in cursor.fetchall()}
        
        if 'Priority' in columns and 'IsUrgent' not in columns:
            print("✓ Migration already complete. Priority column exists.")
            conn.close()
            return True
        
        if 'Priority' in columns and 'IsUrgent' in columns:
            print("✓ Migration in progress (both columns exist). Removing IsUrgent column...")
            cursor.execute("ALTER TABLE Issues DROP COLUMN IsUrgent")
            conn.commit()
            print("✓ Migration complete. IsUrgent column removed.")
            conn.close()
            return True
        
        if 'IsUrgent' not in columns:
            print("✗ Error: Neither Priority nor IsUrgent column found.")
            conn.close()
            return False
        
        # Begin migration
        print("Starting migration from IsUrgent (boolean) to Priority (enum)...")
        
        # Add Priority column (temporarily allow NULL)
        cursor.execute("ALTER TABLE Issues ADD COLUMN Priority TEXT")
        
        # Convert IsUrgent to Priority
        # IsUrgent=1 (true) → HIGH
        # IsUrgent=0 (false) → MEDIUM
        cursor.execute("""
            UPDATE Issues 
            SET Priority = CASE 
                WHEN IsUrgent = 1 THEN 'HIGH'
                WHEN IsUrgent = 0 THEN 'MEDIUM'
                ELSE 'MEDIUM'
            END
        """)
        
        # Verify conversion
        cursor.execute("SELECT COUNT(*) FROM Issues WHERE Priority IS NULL")
        null_count = cursor.fetchone()[0]
        
        if null_count > 0:
            print(f"✗ Error: {null_count} rows have NULL Priority after conversion.")
            conn.rollback()
            conn.close()
            return False
        
        # Get counts for reporting
        cursor.execute("SELECT Priority, COUNT(*) FROM Issues GROUP BY Priority")
        priority_counts = cursor.fetchall()
        
        # Drop the IsUrgent column
        cursor.execute("ALTER TABLE Issues DROP COLUMN IsUrgent")
        
        conn.commit()
        
        # Report results
        print("✓ Migration successful!")
        print(f"  Rows converted:")
        for priority, count in priority_counts:
            print(f"    - {priority}: {count}")
        
        conn.close()
        return True
        
    except sqlite3.Error as e:
        print(f"✗ Database error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False


def rollback_migration(db_path: str = "issues.db"):
    """
    Rollback migration by restoring from the most recent backup.
    
    Args:
        db_path: Path to the SQLite database file
    
    Returns:
        bool: True if rollback successful, False otherwise
    """
    # Find the most recent backup
    import glob
    backup_pattern = f"{db_path}.backup.*"
    backups = sorted(glob.glob(backup_pattern), reverse=True)
    
    if not backups:
        print(f"No backup files found matching pattern: {backup_pattern}")
        return False
    
    latest_backup = backups[0]
    print(f"Rolling back to: {latest_backup}")
    
    try:
        import shutil
        shutil.copy2(latest_backup, db_path)
        print("✓ Rollback complete.")
        return True
    except Exception as e:
        print(f"✗ Rollback failed: {e}")
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Migrate Issues database from IsUrgent (boolean) to Priority (enum)"
    )
    parser.add_argument(
        "--db",
        default="issues.db",
        help="Path to the SQLite database file (default: issues.db)"
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Skip creating a backup before migration"
    )
    parser.add_argument(
        "--rollback",
        action="store_true",
        help="Rollback to the most recent backup"
    )
    
    args = parser.parse_args()
    
    if args.rollback:
        success = rollback_migration(args.db)
    else:
        success = migrate_database(args.db, backup=not args.no_backup)
    
    sys.exit(0 if success else 1)
