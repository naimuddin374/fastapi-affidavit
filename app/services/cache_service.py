import os
import json
from typing import Any, Optional, Dict
from app.utils.json_encoder import serialize_data
from redis import Redis, exceptions as redis_exceptions
from dotenv import load_dotenv
# Note: TypeError is the correct exception for JSON dumping failures

# IMPORTANT: I've updated your environment variable usage here
# and moved the Redis client initialization outside of __init__
# to follow standard FastAPI pattern, connecting once.

# Environment variables from your system
# Default to 'redis' (Docker service name)
load_dotenv()
REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
REDIS_PORT = os.environ.get("REDIS_PORT", 6379)
# Ensure TTL is an integer
REDIS_TTL = int(os.environ.get('REDIS_TTL', 300))

# --- Initialize Redis Client Once (Recommended FastAPI Pattern) ---
# Create the connection object outside the class instance
try:
    REDIS_CLIENT = Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=0,
        decode_responses=True  # Decodes bytes to strings automatically
    )
    # Ping to check connection immediately (optional, but good practice)
    REDIS_CLIENT.ping()
    print("INFO: Redis Client initialized successfully.")

except Exception as e:
    print(f"FATAL ERROR: Could not initialize Redis Client: {e}")
    # You might want to exit the application or use a fallback mechanism here
    REDIS_CLIENT = None  # Set to None if initialization fails


class CacheService:
    """
    A service wrapper for basic key-value caching operations using Redis.
    It automatically handles JSON serialization/deserialization for Python objects.
    """

    def __init__(self):
        """Initializes the service using the pre-configured global client."""
        if REDIS_CLIENT is None:
            raise RuntimeError(
                "CacheService cannot be initialized: REDIS_CLIENT is not configured.")

        # Use the pre-initialized client
        self._client: Redis = REDIS_CLIENT
        self.DEFAULT_TTL = REDIS_TTL  # Default expiration time

    # --- Utility: Connection Check ---
    def ping_redis(self) -> bool:
        """Checks if the Redis client is connected and healthy."""
        try:
            if self._client.ping():
                print("INFO: Successfully connected to Redis cache server!")
                return True
            else:
                print("ERROR: Redis ping failed.")
                return False
        except redis_exceptions.ConnectionError as e:
            print(f"FATAL ERROR: Could not connect to Redis: {e}")
            return False

    # --- Method 1: SET ---
    def set_value(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """
        1. Sets a key-value pair in Redis with an optional TTL.
           Uses the custom 'default' serializer for generic data handling.
        """
        try:
            ttl_to_use = ttl if ttl is not None else self.DEFAULT_TTL

            # --- THE GENERIC FIX IS HERE ---
            # Pass your helper function to the 'default' argument.
            # If json.dumps encounters a complex object, it will call serialize_data().
            serialized_value = json.dumps(value, default=serialize_data)

            # Store the key in Redis
            self._client.set(key, serialized_value, ex=ttl_to_use)
            print(
                f"CACHE: SET successful for key '{key}' with TTL {ttl_to_use}s.")
            return True

        except TypeError as e:
            # This will only be raised if serialize_data couldn't handle the object
            print(
                f"ERROR: Could not SET key '{key}'. Value is not JSON serializable. {e}")
            return False
        except redis_exceptions.ConnectionError as e:
            print(
                f"ERROR: Could not SET key '{key}'. Redis Connection Error. {e}")
            return False

    # --- Method 2: GET ---
    def get_value(self, key: str) -> Optional[Any]:
        """
        Retrieves and deserializes a value using a key.
        Returns None if the key is not found or has expired.
        """
        try:
            cached_data = self._client.get(key)

            if cached_data is None:
                print(f"CACHE: GET miss for key '{key}'.")
                return None

            # Deserialize the JSON string back into a Python object
            deserialized_value = json.loads(cached_data)
            print(f"CACHE: GET hit for key '{key}'.")
            return deserialized_value

        # FIX 2: Catch JSONDecodeError for deserialization failures
        except json.JSONDecodeError as e:
            print(
                f"ERROR: Could not GET or deserialize key '{key}'. Malformed JSON stored. {e}")
            return None
        except redis_exceptions.ConnectionError as e:
            print(
                f"ERROR: Could not GET key '{key}'. Redis Connection Error. {e}")
            return None

    # --- Method 3: REMOVE ---
    def remove_value(self, key: str) -> bool:
        """
        Removes (invalidates) a key from the cache.
        """
        try:
            # The delete command returns the number of keys removed (0 or 1)
            deleted_count = self._client.delete(key)
            if deleted_count > 0:
                print(f"CACHE: REMOVED key '{key}'.")
            else:
                print(f"CACHE: REMOVE attempted on non-existent key '{key}'.")
            return deleted_count > 0
        except redis_exceptions.ConnectionError as e:
            print(
                f"ERROR: Could not REMOVE key '{key}'. Redis Connection Error. {e}")
            return False
