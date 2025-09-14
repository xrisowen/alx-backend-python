import sqlite3

class DatabaseConnection:
    """
    A class-based context manager for handling database connections.
    """
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        """
        Connects to the database and returns the connection object.
        """
        try:
            self.conn = sqlite3.connect(self.db_name)
            print(f"Successfully connected to the database '{self.db_name}'")
            return self.conn
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            raise  # Re-raise the exception to stop execution

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Closes the database connection, regardless of whether an
        exception occurred.
        """
        if self.conn:
            self.conn.close()
            print(f"Connection to '{self.db_name}' closed.")

# --- Usage Example ---
if __name__ == "__main__":
    db_file = 'users_test.db'
    
    # Use the custom context manager with a 'with' statement.
    with DatabaseConnection(db_file) as conn:
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users")
                users = cursor.fetchall()
                print("Query results:")
                print(users)
            except sqlite3.Error as e:
                print(f"Query error: {e}")
