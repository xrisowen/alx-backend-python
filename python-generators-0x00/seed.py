import mysql.connector
import csv
import uuid

# MySQL connection details.
# IMPORTANT: Replace with your actual database credentials.
HOST = "localhost"
USER = "newuser2"
PASSWORD = "password"
DATABASE_NAME = "ALX_prodev"
TABLE_NAME = "user_data"

seed = __import__('seed')

def connect_db():
    """
    Connects to the MySQL database server.
    
    Returns:
        A connection object if successful, None otherwise.
    """
    try:
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD
        )
        print("Successfully connected to the MySQL server.")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_database(connection):
    """
    Creates the specified database if it does not already exist.

    Args:
        connection: The MySQL server connection object.
    """
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}")
        print(f"Database '{DATABASE_NAME}' created or already exists.")
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()

def connect_to_prodev():
    """
    Connects to the ALX_prodev database in MySQL.

    Returns:
        A connection object if successful, None otherwise.
    """
    try:
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE_NAME
        )
        print(f"Successfully connected to the '{DATABASE_NAME}' database.")
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to '{DATABASE_NAME}': {err}")
        return None


def create_table(connection):
    """
    Creates the 'user_data' table with the required fields.

    Args:
        connection: The database connection object.
    """
    try:
        cursor = connection.cursor()
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(5, 2) NOT NULL
        )
        """
        cursor.execute(create_table_query)
        connection.commit()
        print(f"Table '{TABLE_NAME}' created or already exists.")
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()

def insert_data(connection, data_file="user_data.csv"):
    """
    Inserts data from a CSV file into the 'user_data' table,
    auto-generating UUIDs for each entry.

    Args:
        connection: The database connection object.
        data_file: The path to the CSV file.
    """

    try:
        cursor = connection.cursor()
        with open(data_file, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row            
            
            # The query now expects 4 values: a UUID and the three CSV columns
            insert_query = f"INSERT INTO {TABLE_NAME} (user_id, name, email, age) VALUES (%s, %s, %s, %s)"
            
            for row in reader:
                
                # Generate a new UUID for each row
                new_uuid = str(uuid.uuid4())
                
                # The data tuple now includes the new UUID at the beginning
                data_tuple = (new_uuid,) + tuple(row)
                
                try:
                    cursor.execute(insert_query, data_tuple)
                    connection.commit()
                    print(f"Inserted row for user: {row[0]}")
                except mysql.connector.Error as err:
                    print(f"Error inserting data for row {row}: {err}")

    except mysql.connector.Error as err:
        print(f"Database error during insertion: {err}")
    except FileNotFoundError:
        print(f"Error: The file '{data_file}' was not found.")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()

def stream_user_rows(connection):
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
    # 1. Connect to the MySQL server
    server_conn = seed.connect_db()
    if not server_conn:
        exit()

    # 2. Create the database
    create_database(server_conn)
    server_conn.close()

    # 3. Connect to the specific database
    db_conn = connect_to_prodev()
    if not db_conn:
        exit()

    # 4. Create the table
    create_table(db_conn)

    # 5. Insert data from the CSV file
    insert_data(db_conn)

    print("\n--- Demonstrating Data Streaming with Generator ---")
    
    # 6. Use the generator to stream data
    data_stream = stream_user_rows(db_conn)

    # The for loop iterates over the generator, fetching one row at a time
    for i, row in enumerate(data_stream):
        print(f"Streaming Row {i+1}: {row}")
        if i > 10: break
    
    # Close the database connection when finished
    db_conn.close()
    print("\nDatabase connection closed.")


