import psycopg2

def stream_users_in_batches(batch_size):
    """
    Generator that fetches users from the user_data table in batches.
    Uses server-side cursor for efficient streaming.
    """
    connection = psycopg2.connect(
        dbname="ALX_prodev",
        user="postgres",
        password="S3M0V!T@",
        host="localhost",
        port="5432"
    )

    try:
        with connection.cursor(name="user_batch_stream") as cursor:
            cursor.execute("SELECT user_id, name, email, age FROM user_data;")

            while True:
                batch = cursor.fetchmany(batch_size)
                if not batch:
                    break
                yield batch  

    finally:
        connection.close()

def batch_processing(batch_size):
    """
    Processes each batch from the stream_users_in_batches generator.
    Filters users over the age of 25 and yields them one by one.
    """
    for batch in stream_users_in_batches(batch_size): 
        for user in batch:
            user_id, name, email, age = user
            if age > 25: 
                print(user)