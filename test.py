import aioredis
import asyncio

# Create Redis client bound to connections pool.
async def pool_of_connections():
   redis = await aioredis.create_redis_pool(
      'redis://localhost')
   val = await redis.get('my-key')

   # we can also use pub/sub as underlying pool
   #  has several free connections:
   ch1, ch2 = await redis.subscribe('chan:1', 'asd')
   # publish using free connection
   await redis.publish('asd', 'Hello World')
   a = await ch2.get()
   print(a)

asyncio.run(pool_of_connections())