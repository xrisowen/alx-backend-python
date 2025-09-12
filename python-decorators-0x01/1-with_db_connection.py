import sqlite3 
import functools

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
def get_user_by_id(conn, user_id):
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)) 
    return cursor.fetchone() 
#### Fetch user by ID with automatic connection handling 

user = get_user_by_id(user_id=1)
print(user)
