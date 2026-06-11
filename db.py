import sqlite3
def get_connect():#this func is to get the conncetion to db
    con=sqlite3.connect("Data_Visualizer.db")
    con.row_factory=sqlite3.Row   
    return con

def create_database():#to create a database table 
    con=get_connect()
    c=con.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users(
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              username TEXT UNIQUE NOT NULL,
              password TEXT NOT NULL)
    """)

    c.execute("""
    INSERT OR IGNORE INTO users(username, password)
    VALUES(?, ?)
    """, ("akshaya", "1234"))

    c.execute("""CREATE TABLE IF NOT EXISTS chart_history(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            chart_type TEXT,
            x_column TEXT,
            y_column TEXT,
            chart_file TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id))
    """)
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    for row in c.fetchall():
        print(row["name"])
    con.commit()
    con.close()


if __name__ == "__main__":
    create_database()

