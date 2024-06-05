from db.redis import redis_connection as redis


print(redis.hgetall("be9902a8-fc70-41af-9fcd-c2675398ca87").keys())