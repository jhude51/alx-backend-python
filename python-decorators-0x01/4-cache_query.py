import time
import sqlite3 
import functools


query_cache = {}

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

def cache_query(func):
    """
        Decorator that caches query results to avoid redundant DB calls
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query") if "query" in kwargs else (args[1] if len(args) > 1 else None)

        if query in query_cache:
            print(f"[CACHE HIT] Returning cached results for query: {query}")
            return query_cache[query]
        else:
            print(f"[CACHE MISS] Executing and caching query: {query}")
            result = func(*args, **kwargs)
            query_cache[query] = result
            return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")