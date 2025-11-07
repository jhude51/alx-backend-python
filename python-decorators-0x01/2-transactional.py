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

def transactional(func):
    """
    Decorator that wraps a function inside a database transaction.
    Commits if successful, rolls back if an exception occurs.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()  # Commit transaction if no errors
            return result
        except Exception as e:
            conn.rollback()  # Rollback on error
            print(f"[ERROR] Transaction rolled back due to: {e}")
            raise
        return wrapper

@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 
#### Update user's email with automatic transaction handling 

update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')   