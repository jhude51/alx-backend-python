import csv
import uuid
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


DB_HOST = "localhost"
DB_PORT = 5432
DB_USER = "postgres"
DB_PASSWORD = "S3M0V!T@"
DB_NAME = "ALX_prodev"

def connect_db():
    """Connect to PostgreSQL server."""
    conn = psycopg2.connect(
        dbname="postgres",  # default database
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    print("✅ Connected to PostgreSQL server.")
    return conn

def create_database(connection):
    """
    Create ALX_prodev database if it doesn't exist.
    Accepts an active PostgreSQL connection (server-level).
    """
    with connection.cursor() as cursor:
        # Check if the database exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (DB_NAME,))
        exists = cursor.fetchone()

        if not exists:
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME)))
            print(f"✅ Database '{DB_NAME}' created successfully.")
        else:
            print(f"ℹ️ Database '{DB_NAME}' already exists.")

def connect_to_prodev():
    """Connect to the ALX_prodev database."""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT, 
        )
        print(f"✅ Connected to '{DB_NAME}' database.")
        return conn
    except psycopg2.Error as e:
        print(f"❌ Failed to connect to '{DB_NAME}' database: {e}")
        return None
    
def create_table(connection):
    """
    Creates the user_data table in the ALX_prodev database if it doesn't exist.
    """
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id UUID PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        age DECIMAL NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(create_table_query)
            connection.commit()
        print("✅ Table 'user_data' created or already exists.")
    except Exception as e:
        print(f"❌ Error creating table: {e}")

def stream_csv(file_path):
    """
    Streams data from the CSV file one row at a time using a generator.
    More memory-efficient than loading all data at once.
    """
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            yield row  # <-- Generator implementation
    print(f"📄 Loaded {len(row)} rows from {file_path}.")
    return row

def insert_data(connection, data):
    """
    Inserts data into the user_data table.
    Skips rows that already exist (idempotent insert using ON CONFLICT).
    """
    insert_query = """
    INSERT INTO user_data (user_id, name, email, age)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (email) DO NOTHING;
    """
    inserted = 0

    with connection.cursor() as cursor:
        for row in stream_csv(data):
            user_id = str(uuid.uuid4())
            name = row["name"].strip()
            email = row["email"].strip().lower()
            age = float(row["age"])

            cursor.execute(insert_query, (user_id, name, email, age))
            inserted += cursor.rowcount  # rowcount = 1 if inserted, 0 if skipped

        connection.commit()

    print(f"✅ Inserted {inserted} new rows into user_data.")