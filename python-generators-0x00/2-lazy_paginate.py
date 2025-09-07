from seed import connect_to_prodev

def paginate_users(page_size, offset):
    """
    Fetches a single page of data from the user_data table.

    Args:
        page_size: The number of rows to fetch.
        offset: The starting row for the fetch.

    Returns:
        A list of tuples representing the rows for the requested page.
    """
    conn = None
    cursor = None
    try:
        conn = connect_to_prodev()
        if not conn:
            return []
        cursor = conn.cursor()
        # Use LIMIT and OFFSET to fetch a specific page of data
        query = f"SELECT * FROM user_data LIMIT %s OFFSET %s"
        cursor.execute(query, (page_size, offset))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error fetching paginated data: {err}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def lazy_paginate(page_size):
    """
    A generator that lazily loads pages of data from the database.

    Args:
        page_size: The number of users to fetch per page.

    Yields:
        A list of tuples representing a page of users.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            # Stop the generator when there are no more pages
            break
        yield page
        offset += page_size


if __name__ == "__main__":
    # 1. Demonstrate the new batch processing function
    # 7. Demonstrate the new lazy pagination generator
    print("\n--- Demonstrating Lazy Pagination with Generator ---")
    page_generator = lazy_paginate(page_size=2)
    
    for i, page in enumerate(page_generator):
        print(f"--- Fetched Page {i+1} ---")
        for user_row in page:
            print(user_row)
