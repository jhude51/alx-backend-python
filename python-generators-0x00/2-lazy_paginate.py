import psycopg2

def paginate_users(page_size, offset):
    """
    Fetches a single page of users from the database based on page size and offset.
    Returns a list of tuples.
    """
    connection = psycopg2.connect(
        dbname="ALX_prodev",
        user="postgres",
        password="S3M0V!T@",
        host="localhost",
        port="5432"
    )

    try:
        with connection.cursor() as cursor:
            query = """
            SELECT user_id, name, email, age
            FROM user_data
            ORDER BY created_at ASC
            LIMIT %s OFFSET %s;
            """
            cursor.execute(query, (page_size, offset))
            result = cursor.fetchall()
            return result
    finally:
        connection.close()


def lazy_paginate(page_size):
    """
    Generator that lazily fetches paginated user data from the database.
    Uses only one loop and fetches the next page only when needed.
    """
    offset = 0
    while True:  
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page  
        offset += page_size 