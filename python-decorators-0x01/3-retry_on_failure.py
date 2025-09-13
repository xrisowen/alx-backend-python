import sqlite3 
import functools
import time

def retry_on_failure(retries=3, delay=1):
    """
    A decorator that retries a function a specified number of times
    if it raises an exception.

    Args:
        retries (int): The number of times to retry the function.
        delay (int): The delay in seconds between retries.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {i + 1} failed: {e}")
                    if i < retries - 1:
                        print(f"Retrying in {delay} second(s)...")
                        time.sleep(delay)
                    else:
                        print("All retry attempts failed.")
                        raise # Re-raise the last exception
        return wrapper
    return decorator

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
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)

