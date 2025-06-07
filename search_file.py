import sqlite3
from tabulate import tabulate
import threading

DB_PATH = r'system_files.db'

# Shared container to store search results
results = []

def search_files(input_name, results_container):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Case-insensitive LIKE search
        query = "SELECT file_name, file_path FROM files WHERE LOWER(file_name) LIKE ?"
        wildcard_name = f"%{input_name.lower()}%"
        cursor.execute(query, (wildcard_name,))
        rows = cursor.fetchall()
        results_container.extend(rows)

        conn.close()
    except Exception as e:
        print(f"❌ Error during DB search: {e}")

def main():
    input_name = input("🔍 Enter file name to search (no fuzzy): ").strip()
    if not input_name:
        print("❌ Please enter a valid file name.")
        return

    print("🔎 Searching in background thread...")

    search_thread = threading.Thread(target=search_files, args=(input_name, results))
    search_thread.start()
    search_thread.join()  # Wait for thread to complete

    if not results:
        print("❌ No matches found.")
    else:
        print(tabulate(results, headers=["File Name", "File Path"], tablefmt="fancy_grid"))

if __name__ == "__main__":
    main()

