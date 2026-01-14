import sqlite3

def initdb():
    conn = sqlite3.connect('tracker.db')
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS habits(
            id INTEGER NOT NULL,
            habit TEXT NOT NULL,
            date TEXT DEFAULT CURRENT_DATE,
            PRIMARY KEY (id, habit),
            FOREIGN KEY (id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()
    print("Database Updated: Ready to track history.")



if __name__ == "__main__":
    initdb()