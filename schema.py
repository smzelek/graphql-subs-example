from graphene import ObjectType, String, Schema, Field
import os
from rx import Observable
from redisclient import asyncredis
import asyncio
from flask import abort
from datetime import datetime

class SampleQuery(ObjectType):
    result = String()
    server_name = String()

    async def resolve_result(self, info):
        try:
            [channel] = await asyncio.wait_for(asyncredis.subscribe('job:1'), timeout=5)
            a = await asyncio.wait_for(channel.get(), timeout=5)
            return a
        except asyncio.TimeoutError:
            abort(500, "Request timed out.")

    def resolve_server_name(self, info):
        return os.environ.get('SERVER_NAME', 'default')

class Query(ObjectType):
    sample = Field(SampleQuery)

    def resolve_sample(root, info):
        return SampleQuery()

# class StatefulSecondsCounter(graphene.ObjectType):
#     server_name = graphene.String()
#     time = graphene.Int()

#     def resolve_server_name(self, info):
#         return os.environ.get('SERVER_NAME', 'default')

# def from_aiter(iter):
#     def on_subscribe(observer):
#         async def _aio_sub():
#             async for i in iter:
#                 observer.on_next(i)

#         asyncio.ensure_future(_aio_sub())

#     return Observable.create(on_subscribe)

# async def async_build_log():
#     # return Observable.interval(1000)\
#     #                  .take_while(lambda i: i <= 5)
#     yield 0
#     for i in range(10):
#         yield i
#         await asyncio.sleep(1.)
#     yield 10

# class Subscription(graphene.ObjectType):
#     build_log = graphene.Int()

#     # def resolve_build_log(root, info, app_id, job_id):
#     #     return Observable.just(StatefulSecondsCounter())

#     def resolve_build_log(self, info):
#         return Observable.just(1)
class Subscription(ObjectType):
    time_of_day = String()

    async def subscribe_time_of_day(root, info):
        while True:
            yield datetime.now().isoformat()
            await asyncio.sleep(1)

schema = Schema(query=Query,  subscription=Subscription)