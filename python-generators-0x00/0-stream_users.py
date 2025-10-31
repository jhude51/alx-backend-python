import psycopg2


def stream_users():
    """
    Generator that fetches rows one by one from the user_data table.
    Uses a server-side cursor for efficient streaming.
    """
    connection = psycopg2.connect(
        dbname="ALX_prodev",
        user="postgres",
        password="S3M0V!T@",
        host="localhost",
        port="5432"
    )

    try:
        # Create a named (server-side) cursor
        with connection.cursor(name="user_stream") as cursor:
            cursor.itersize = 100  # Fetch 100 rows per batch
            cursor.execute("SELECT * FROM user_data;")

            # Stream rows using yield (1 loop only)
            for row in cursor:
                yield row

    finally:
        connection.close()
