
from root.libs import redis_cache_wrapper
from root.libs import localMySQLDB_connection
import mysql.connector

def get_api_keys():

    @redis_cache_wrapper.redis_cache(3600)
    def cache_api_keys():
        try:
            db_connection = localMySQLDB_connection.LocalDBConnection().connect()

            # Check if connection is alive
            db_connection.ping(reconnect=True, attempts=3, delay=2)

            cursor = db_connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT * FROM xxxxx.api_keys 
                WHERE expiration_date IS NULL OR expiration_date >= NOW();
            """)
            records = cursor.fetchall()
            cursor.close()
            return records

        except mysql.connector.Error as err:
            # Optional: Add logging or re-raise a custom exception
            print(f"[ERROR] Failed to fetch API keys: {err}")
            return []  # or raise an exception if critical

    result = cache_api_keys()
    return result
