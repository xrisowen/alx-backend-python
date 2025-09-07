from seed import connect_to_prodev

def stream_users_in_batches(batch_size):
    conn = None
    cursor = None
    try:
        conn = connect_to_prodev()
        if not conn:
            return
        cursor = conn.cursor(buffered=True)
        cursor.execute(f"SELECT * FROM user_data")
        
        while True:
            # fetchmany() fetches a chunk of rows at a time
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch
    except mysql.connector.Error as err:
        print(f"Error streaming batches: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def batch_processing(batch_size):
    """
    Processes each batch to filter users over the age of 25.

    Args:
        batch_size: The size of each batch to process.
    """
    print(f"\n--- Processing Users in Batches (Age > 25) ---")
    
    # Outer loop to iterate over each batch from the generator
    for batch in stream_users_in_batches(batch_size):
        print(f"Processing a new batch of {len(batch)} users...")
        
        # Inner loop to process each user in the current batch
        for user_row in batch:
            user_id, name, email, age = user_row
            if age > 25:
                print(user_row)

if __name__ == "__main__":
    # 1. Demonstrate the new batch processing function
    batch_processing(batch_size=50)
