from functools import wraps
import logging, redis, json
from root import database_credentials
from root.libs import localMySQLDB_connection

redis_client = redis.StrictRedis(
    host=database_credentials.redis_server,
    password=database_credentials.redis_password,
    port=6379,
    db=0
)

MAX_CHUNK_SIZE = 100 * 1024 * 1024

def _split_chunks(data, chunk_size):
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

def _store_in_chunks(key, data, expire):
    chunks = _split_chunks(data, MAX_CHUNK_SIZE)
    for i, chunk in enumerate(chunks):
        redis_client.setex(f"{key}:chunk:{i}", expire, chunk)
    redis_client.setex(f"{key}:num_chunks", expire, len(chunks))

def _get_cache_payload(key):
    # First try simple unchunked payload
    payload = redis_client.get(key)
    if payload:
        return payload.decode()

    # Fallback: Try reassembling chunked cache
    try:
        num_chunks = int(redis_client.get(f"{key}:num_chunks") or 0)
        if num_chunks == 0:
            return None
        chunks = []
        for i in range(num_chunks):
            chunk = redis_client.get(f"{key}:chunk:{i}")
            if chunk is None:
                return None  # incomplete
            chunks.append(chunk)
        return b''.join(chunks).decode()
    except Exception as e:
        logging.exception("Error reassembling cached chunks")
        return None
    
def _get_streamed_chunks(key):
    try:
        num_chunks = int(redis_client.get(f"{key}:num_chunks") or 0)
        if num_chunks == 0:
            return None

        full_data = []
        for i in range(num_chunks):
            chunk = redis_client.get(f"{key}:chunk:{i}")
            if chunk is None:
                return None  # incomplete cache
            rows = json.loads(chunk.decode())  # each chunk is a list of rows
            full_data.extend(rows)

        return full_data
    except Exception:
        logging.exception("Error reassembling streamed cached chunks")
        return None

def redis_cache(expire=120):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{args}:{kwargs}"

            # Load either normal or chunked cache
            cached_payload = _get_cache_payload(cache_key)
            if cached_payload:
                return json.loads(cached_payload)

            # Cache miss: compute and store
            result = func(*args, **kwargs)
            payload = json.dumps(result, default=str)

            if len(payload.encode()) > MAX_CHUNK_SIZE:
                _store_in_chunks(cache_key, payload.encode(), expire)
            else:
                redis_client.setex(cache_key, expire, payload)

            return result
        return wrapper
    return decorator

def redis_cache_streamed(expire=120, chunk_size=500000):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{args}:{kwargs}"

            # Try reading from Redis cache
            cached_result = _get_streamed_chunks(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Cache miss — execute the SQL query and stream chunks
            redis_client.delete(f"{cache_key}:num_chunks")
            chunk_index = 0
            total_rows = 0
            all_data = []

            db_connection = localMySQLDB_connection.LocalDBConnection().connect()
            cursor = db_connection.cursor(dictionary=True)

            try:
                query = func(*args, **kwargs)  # get SQL string
                cursor.execute(query)

                while True:
                    rows = cursor.fetchmany(chunk_size)
                    if not rows:
                        break

                    json_chunk = json.dumps(rows, default=str).encode()
                    redis_client.setex(f"{cache_key}:chunk:{chunk_index}", expire, json_chunk)
                    all_data.extend(rows)  # build final return value
                    print(f"Chunk {chunk_index}: Retrieved {len(rows)} rows (Total: {total_rows + len(rows)})")
                    total_rows += len(rows)
                    chunk_index += 1

                redis_client.setex(f"{cache_key}:num_chunks", expire, chunk_index)

            finally:
                cursor.close()
                db_connection.close()

            return all_data
        return wrapper
    return decorator