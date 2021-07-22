import graphene
import os
from rx import Observable
from redisclient import asyncredis
import asyncio
from flask import abort

class SampleQuery(graphene.ObjectType):
    result = graphene.String()
    server_name = graphene.String()

    async def resolve_result(self, info):
        try:
            [channel] = await asyncio.wait_for(asyncredis.subscribe('job:1'), timeout=10)
        except asyncio.TimeoutError:
            abort(500, "Request timed out.")
        a = await channel.get()
        return a

    def resolve_server_name(self, info):
        return os.environ.get('SERVER_NAME', 'default')

class Query(graphene.ObjectType):
    sample = graphene.Field(SampleQuery)

    def resolve_sample(root, info):
        return SampleQuery()


class StatefulSecondsCounter(graphene.ObjectType):
    server_name = graphene.String()
    time = graphene.Int()

    def resolve_server_name(self, info):
        return os.environ.get('SERVER_NAME', 'default')

class Subscription(graphene.ObjectType):
    build_log = graphene.Int()

    # def resolve_build_log(root, info, app_id, job_id):
    #     return Observable.just(StatefulSecondsCounter())

    async def resolve_build_log(self, info):
        yield 0
        for i in range(10):
            yield i
            await asyncio.sleep(1.)
        yield 10

schema = graphene.Schema(query=Query,  subscription=Subscription)