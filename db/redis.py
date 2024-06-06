import dotenv
import os
from redis import Redis

dotenv.load_dotenv()

redis_connection = Redis.from_url(os.getenv("REDIS_SERVICE_URI"), decode_responses=True)