import sqlite3
import functools

#### decorator to log SQL queries

def log_queries(func):
    """
    Decorator that logs SQL queries using print() instead of logging module.
    """
    @functools.wraps(func) #copy attributes from the original function (func) to the wrapper
    def wrapper(*args, **kwargs):
        # Get the SQL query
        sql_query = kwargs.get("query") if "query" in kwargs else (args[0] if args else None)

        if isinstance(sql_query, str):
            print(f"[LOG] Executing query in {func.__name__}: {sql_query}")
        else:
            print(f"[LOG] Calling {func.__name__} (no SQL query detected)")

        # Execute the wrapped function
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