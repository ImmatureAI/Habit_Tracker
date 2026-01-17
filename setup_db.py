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
            habit_id INTEGER AUTOINCREMENT,
            PRIMARY KEY (id, habit),
            FOREIGN KEY (id) REFERENCES users(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS habit_log(
            user_id INTEGER NOT NULL,
            habit_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (habit_id) REFERENCES habits(habit_id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            PRIMARY KEY (user_id, habit_id, date)
        )
    ''')

    conn.commit()
    conn.close()
    print("Database Updated: Ready to track history.")



if __name__ == "__main__":
    initdb()