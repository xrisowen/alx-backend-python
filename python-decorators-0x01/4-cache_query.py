import time
import sqlite3
import functools

# A global dictionary to store cached query results
query_cache = {}

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

def cache_query(func):
    """
    A decorator that caches the results of a database query to avoid
    redundant calls for the same query string.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        # The query string is the cache key.
        # We assume the query is passed as a keyword argument named 'query'.
        # For a more robust solution, you would handle both args and kwargs
        query = kwargs.get('query')
        if not query:
            # This handles cases where the query might not be in kwargs,
            # for simplicity we'll assume it's always there for this use case.
            print("No 'query' argument found in kwargs. Cannot cache.")
            #return func(conn, *args, **kwargs)
            return "Query not found."

        # Check if the query is already in the cache
        if query in query_cache:
            print(f"Cache HIT for query: '{query}'")
            return query_cache[query]
        
        print(f"Cache MISS for query: '{query}'. Executing...")
        # Execute the original function if not in cache
        result = func(conn, *args, **kwargs)
        
        # Store the result in the cache
        query_cache[query] = result
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
