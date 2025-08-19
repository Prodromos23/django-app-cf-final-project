import sqlite3
import os
from datetime import datetime

# Define the source and backup file paths
source_db = 'db.sqlite3'
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
backup_db = f'backups/db_backup_{timestamp}.sqlite3'

# Perform the backup
try:
    with sqlite3.connect(source_db) as source_conn:
        with sqlite3.connect(backup_db) as backup_conn:
            source_conn.backup(backup_conn)
    print(f"Backup successful: {backup_db}")
except Exception as e:
    print(f"Backup failed: {e}")
