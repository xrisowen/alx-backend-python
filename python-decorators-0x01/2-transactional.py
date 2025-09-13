import sqlite3 
import functools

def transactional(func):
    """
    A decorator that manages a database transaction.
    It commits changes on success and rolls back on failure.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            # Call the decorated function with the connection
            result = func(conn, *args, **kwargs)
            # Commit the transaction if no errors occurred
            conn.commit()
            print("Transaction committed successfully.")
            return result
        except Exception as e:
            # Rollback the transaction on any error
            conn.rollback()
            print(f"Transaction rolled back due to error: {e}")
            raise  # Re-raise the exception to propagate the error
    return wrapper

def with_db_connection(func):
    """
    A decorator that handles database connection management for a function.
    It opens a connection, passes it to the function, and ensures it's closed.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        try:
            # Establish the database connection
            conn = sqlite3.connect('users_test.db')
            
            # Pass the connection object as the first argument to the function
            result = func(conn, *args, **kwargs)
            return result
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            # Ensure the connection is always closed
            if conn:
                conn.close()
    return wrapper

@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 

#### Update user's email with automatic transaction handling
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
