import time
import sqlite3 
import functools

#### paste your with_db_decorator here

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

def retry_on_failure():
    """
        Decorator that retries a function if it fails due to a transient error
    """
    def decorator(func):
        @functools.wrap(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except sqlite3.OperationalError as e:
                    attempt += 1
                    print(f"Attempt {attempt} failed: {e}")
                    if attempt < retries:
                        print(f"Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        print("Max retries reached. Operation failed.")
                        raise
        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)