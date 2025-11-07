import sqlite3

class DatabaseConnection:
    """Context manager to handle opening and closing a database connection"""

    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        print(f"Connecting to database: {self.db_name}")
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()
            print("Database connection closed.")
        # Returning False allows exceptions (if any) to propagate
        return False
    
### Attempt to perform a query

with DatabaseConnection("users.db") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print(results)

