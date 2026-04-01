import sqlite3
import os

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'instance', 'database.db')

if not os.path.exists(db_path):
    print(f"Database not found at {db_path}. Skipping migration.")
    exit(0)

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if column already exists
    cursor.execute("PRAGMA table_info(user_progress)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'roadmap_json' not in columns:
        print("Adding column 'roadmap_json' to table 'user_progress'...")
        cursor.execute("ALTER TABLE user_progress ADD COLUMN roadmap_json TEXT")
        conn.commit()
        print("Column added successfully.")
    else:
        print("Column 'roadmap_json' already exists. No changes needed.")
    
    conn.close()
except Exception as e:
    print(f"Error during migration: {str(e)}")
