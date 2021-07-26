import redis
import asyncio
import aioredis
asyncredis = asyncio.run(aioredis.create_redis_pool('redis://localhost'))
syncredis = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
