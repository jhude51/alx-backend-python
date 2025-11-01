#!/usr/bin/python3
"""
Computes the average age of users using a memory-efficient generator.
The generator streams one user age at a time from the database.
"""

import psycopg2
from psycopg2.extras import RealDictCursor
seed = __import__('seed')


def stream_user_ages():
    """
    Generator that streams user ages one by one from the database.
    Uses yield to avoid loading all rows into memory.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT age FROM user_data;")

    for row in cursor:
        yield float(row['age'])  # yield one age at a time

    connection.close()


def compute_average_age():
    """
    Consumes the stream_user_ages generator to calculate
    the average age of all users using at most two loops.
    """
    total_age = 0
    count = 0

    # Loop 1: consume the generator stream
    for age in stream_user_ages():
        total_age += age
        count += 1

    # Compute and print result
    average_age = total_age / count if count > 0 else 0
    print(f"Average age of users: {average_age:.2f}")

    return average_age