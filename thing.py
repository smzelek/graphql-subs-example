# import asyncio
# from datetime import datetime
# from graphene import ObjectType, String, Schema, Field

# # Every schema requires a query.
# class Query(ObjectType):
#     hello = String()

#     def resolve_hello(root, info):
#         return "Hello, world!"

# class Subscription(ObjectType):
#     time_of_day = String()

#     async def subscribe_time_of_day(root, info):
#         while True:
#             yield datetime.now().isoformat()
#             await asyncio.sleep(1)

# schema = Schema(query=Query)

# async def main(schema):
#     subscription = 'query { hello }'
#     result = await schema.subscribe(subscription)
#     async for item in result:
#         print(item.data['hello'])

# asyncio.run(main(schema))