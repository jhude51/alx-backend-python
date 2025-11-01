#!/usr/bin/python3
"""
Lazily loads paginated user data from the database using a generator.
Each page is fetched only when needed, starting at offset 0.
"""
import psycopg2
from psycopg2.extras import RealDictCursor
seed = __import__('seed')


def paginate_users(page_size, offset):
    """
    Fetches a single page of users from the user_data table.
    Uses LIMIT and OFFSET for pagination.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return [dict(row) for row in rows]


def lazy_paginate(page_size):
    """
    Generator function that lazily fetches paginated user data from the database.
    Only fetches the next page when needed.
    """
    offset = 0
    while True: 
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size 