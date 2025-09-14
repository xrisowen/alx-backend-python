import sqlite3

class ExecuteQuery:
    """
    A context manager to execute a specific SQL query and return its results.
    This class handles the database connection lifecycle internally.
    """
    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params if params is not None else ()
        self.conn = None
        self.result = None

    def __enter__(self):
        """
        Connects to the database, executes the query, and stores the result.
        """
        try:
            self.conn = sqlite3.connect(self.db_name)
            print(f"Successfully connected to the database '{self.db_name}'")
            cursor = self.conn.cursor()
            cursor.execute(self.query, self.params)
            self.result = cursor.fetchall()
            return self
        except sqlite3.Error as e:
            print(f"Query execution error: {e}")
            self.result = None
            # Do not re-raise, as the __exit__ method needs to close the connection
            return self

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
    print("Executing query...")
    query_string = "SELECT * FROM users WHERE age > ?"
    query_params = (25,)
    
    with ExecuteQuery(db_name=db_file, query=query_string, params=query_params) as query_exec:
        print("Query results:")
        print(query_exec.result)
