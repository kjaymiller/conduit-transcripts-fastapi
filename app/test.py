from db.redis import redis_connection as redis

print(redis.scan())
redis.flushall()