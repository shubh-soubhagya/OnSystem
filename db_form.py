import os
import sqlite3
import platform

DB_FILE = 'system_files.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT,
            file_path TEXT,
            file_extension TEXT
        )
    ''')
    conn.commit()
    conn.close()

def safe_str(s):
    try:
        return str(s)
    except UnicodeEncodeError:
        return s.encode('utf-8', 'surrogateescape').decode('utf-8', 'replace')

def index_all_files(start_dir):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    for dirpath, dirnames, filenames in os.walk(start_dir, topdown=True):
        # filter hidden/system dirs
        dirnames[:] = [d for d in dirnames if not d.startswith('$')]

        for file in filenames:
            try:
                file_path = os.path.join(dirpath, file)
                file_name = os.path.basename(file)
                file_extension = os.path.splitext(file)[1].lower()

                safe_name = safe_str(file_name)
                safe_path = safe_str(file_path)
                safe_ext = safe_str(file_extension)

                cursor.execute("""
                    INSERT INTO files (file_name, file_path, file_extension)
                    VALUES (?, ?, ?)
                """, (safe_name, safe_path, safe_ext))
            except Exception as e:
                try:
                    print(f"⚠️ Skipped: {repr(file_path)} | Reason: {e}")
                except Exception:
                    print("⚠️ Skipped an unprintable path due to encoding issues.")

    conn.commit()
    conn.close()
    print("✅ System-wide indexing complete.")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Index all system files into SQLite DB")
    parser.add_argument('--root', type=str, help='Root directory to index (default: full system)', default=None)
    args = parser.parse_args()

    if args.root:
        root_dir = args.root
    else:
        root_dir = "C:\\" if platform.system() == "Windows" else "/"

    print(f"🔍 Starting index from: {root_dir}")
    init_db()
    index_all_files(root_dir)
