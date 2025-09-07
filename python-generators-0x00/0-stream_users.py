import mysql.connector
from seed import connect_to_prodev

TABLE_NAME = "user_data"

def stream_users(connection):
    """
    A generator function that streams rows from the 'user_data' table
    one by one, to conserve memory.

    Args:
        connection: The database connection object.

    Yields:
        A tuple representing a single row from the database.
    """
    cursor = None
    try:
        # Use buffered=True for fetching rows one at a time for large datasets
        cursor = connection.cursor(buffered=True)
        query = f"SELECT * FROM {TABLE_NAME}"
        cursor.execute(query)
        
        while True:
            row = cursor.fetchone()
            if row is None:
                # No more rows to fetch, stop the generator
                break
            yield row
    except mysql.connector.Error as err:
        print(f"Error streaming data: {err}")
    finally:
        if cursor:
            cursor.close()


if __name__ == "__main__":
    # 1. Connect to the specific database
    db_conn = connect_to_prodev()
    if not db_conn:
        exit()

    print("\n--- Demonstrating Data Streaming with Generator ---")
    
    # 6. Use the generator to stream data
    data_stream = stream_users(db_conn)

    # The for loop iterates over the generator, fetching one row at a time
    for i, row in enumerate(data_stream):
        print(f"Streaming Row {i+1}: {row}")
        if i > 5: break
    
    # Close the database connection when finished
    db_conn.close()
    print("\nDatabase connection closed.")


