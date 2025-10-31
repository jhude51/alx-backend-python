from seed import *

if __name__ == "__main__":
    conn = connect_db()
    create_database(conn)
    conn.close()
    prodev_conn = connect_to_prodev()
    if prodev_conn:
        print("🎉 Connection test successful!")
    create_table(prodev_conn)
    insert_data(prodev_conn, "user_data.csv")
    prodev_conn.close()
    print("🎉 Data seeding complete!")