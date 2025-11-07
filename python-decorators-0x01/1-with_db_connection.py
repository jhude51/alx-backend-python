import sqlite3 
import functools

def with_db_connection(func):
    """
    Decorator that opens a SQLite database connection before executing the function,
    passes it as the first argument, and closes it afterward.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db') # Open connection
        try:
            # Pass the connection to the wrapper
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper 

@with_db_connection 
def get_user_by_id(conn, user_id): 
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)) 
    return cursor.fetchone() 

#### Fetch user by ID with automatic connection handling 

user = get_user_by_id(user_id=1)
print(user)