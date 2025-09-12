import sqlite3
import functools
import time
import json
from datetime import datetime

def log_queries(func):
    """
    A decorator that logs the SQL query before executing it.

    Using functools.wraps when creating a decorator is crucial because it preserves the
    original function's metadata, such as its name, docstring, and argument list.

    For example, without functools.wraps, if you were to check the name of fetch_all_users,
    it would incorrectly return "wrapper". With functools.wraps, it correctly returns "fetch_all_users".
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Log the request details in JSON format
        start_time = time.time()
        request_log = {
            "type": "REQUEST",
            "timestamp": datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
            "method_called": func.__name__,
            "request_body": {
                "args": args,
                "kwargs": kwargs
            }
        }
        print(json.dumps(request_log, indent=2))
        
        # Call the original function to get the response
        results = func(*args, **kwargs)
        
        # Log the response details in JSON format
        end_time = time.time()
        response_log = {
            "type": "RESPONSE",
            "timestamp": datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
            "execution_time_ms": (end_time - start_time) * 1000,
            "response_body": results
        }
        print(json.dumps(response_log, indent=2))
        
        return results
    return wrapper

@log_queries
def fetch_all_users(query):
    """
    Fetches all users from a SQLite database.
    This is for demonstration and does not use a robust connection handler.
    """
    try:
        conn = sqlite3.connect('users_test.db')
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return results
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return []

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
