import asyncio
import aiosqlite
import sqlite3

async def async_fetch_users():
    """
    Asynchronously fetches all users from the database.
    """
    print("Starting to fetch all users...")
    async with aiosqlite.connect('users_test.db') as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            return users

async def async_fetch_older_users():
    """
    Asynchronously fetches users older than 40 from the database.
    """
    print("Starting to fetch users older than 40...")
    async with aiosqlite.connect('users_test.db') as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            older_users = await cursor.fetchall()
            return older_users

async def fetch_concurrently():
    """
    Runs both asynchronous fetch functions concurrently using asyncio.gather.
    """
    try:
        # Create a temporary table for testing since we are not using the setup_db.py file here.
        conn = sqlite3.connect('users_test.db')
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                age INT
            );
        """)
        c.execute("INSERT OR REPLACE INTO users (id, name, age) VALUES (1, 'Alice Smith', 30);")
        c.execute("INSERT OR REPLACE INTO users (id, name, age) VALUES (2, 'Bob Johnson', 24);")
        c.execute("INSERT OR REPLACE INTO users (id, name, age) VALUES (3, 'Charlie Brown', 45);")
        c.execute("INSERT OR REPLACE INTO users (id, name, age) VALUES (4, 'Diana Prince', 52);")
        conn.commit()
        conn.close()

        # Run both queries concurrently and wait for them to complete
        all_users_task = async_fetch_users()
        older_users_task = async_fetch_older_users()
        
        all_users, older_users = await asyncio.gather(all_users_task, older_users_task)
        
        print("\n--- All Users ---")
        print(all_users)
        
        print("\n--- Users Older Than 40 ---")
        print(older_users)

    except sqlite3.Error as e:
        print(f"Database error during setup: {e}")

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
