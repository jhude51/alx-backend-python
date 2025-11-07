import sqlite3
import functools
from datetime import datetime

#### decorator to log SQL queries

def log_queries(func):
    """
    Decorator that logs SQL queries using print() instead of logging module.
    """
    @functools.wraps(func) #copy attributes from the original function (func) to the wrapper
    def wrapper(*args, **kwargs):
        # Get the SQL query
        sql_query = kwargs.get("query") if "query" in kwargs else (args[0] if args else None)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(sql_query, str):
            print(f"[{timestamp}] Executing query in {func.__name__}: {sql_query}")
        else:
            print(f"[{timestamp}] Calling {func.__name__} (no SQL query detected)")

        return func(*args, **kwargs)

    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")