# import aioredis
# import asyncio

# # Create Redis client bound to connections pool.
# async def pool_of_connections():
#    redis = await aioredis.create_redis_pool(
#       'redis://localhost')
#    val = await redis.get('my-key')

#    # we can also use pub/sub as underlying pool
#    #  has several free connections:
#    ch1, ch2 = await redis.subscribe('chan:1', 'asd')
#    # publish using free connection
#    await redis.publish('asd', 'Hello World')
#    a = await ch2.get()
#    print(a)

# asyncio.run(pool_of_connections())
from rx.subjects import Subject

subject_test = Subject()
subject_test.subscribe(
   lambda x: print("The value is {0}".format(x))
)
subject_test.subscribe(
   lambda x: print("The value is {0}".format(x))
)
subject_test.on_next("A")
subject_test.on_completed()
subject_test.on_next("B")
