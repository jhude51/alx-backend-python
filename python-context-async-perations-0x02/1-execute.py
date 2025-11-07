import sqlite3

class ExecuteQuery:
    """Context manager to handle database connection and query execution"""

    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params or ()
        self.conn = None
        self.cursor = None

    def __enter__(self):
        print(f"Connecting to database: {self.db_name}")
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

        print(f"Executing query: {self.query}")
        self.cursor.execute(self.query, self.params)
        results = self.cursor.fetchall()
        return results  # Returned directly to the 'with' block

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()
            print("Database connection closed.")
        return False  # Propagate exceptions if they occur
    

query = "SELECT * FROM users WHERE age > ?"
params = (25,)

with ExecuteQuery("users.db", query, params) as results:
    print("Query Results:")
    for row in results:
        print(row)