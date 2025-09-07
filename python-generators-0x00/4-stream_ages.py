from seed import connect_to_prodev

def stream_user_ages():
    """
    A generator function that streams user ages from the database.

    Yields:
        A single age (Decimal) from each row.
    """
    conn = None
    cursor = None
    try:
        conn = connect_to_prodev()
        if not conn:
            return
        
        cursor = conn.cursor(buffered=True)
        query = f"SELECT age FROM user_data"
        cursor.execute(query)
        
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            # Yields the age from the single-element tuple
            yield row[0]
    except mysql.connector.Error as err:
        print(f"Error streaming ages: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def calculate_average_age():
    """
    Calculates the average age of all users using the generator.
    """
    total_age = 0
    user_count = 0
    
    # This is the first and only loop for the calculation
    for age in stream_user_ages():
        total_age += age
        user_count += 1
        
    if user_count > 0:
        average_age = total_age / user_count
        print(f"Average age of users: {average_age:.2f}")
    else:
        print("No users found to calculate average age.")


