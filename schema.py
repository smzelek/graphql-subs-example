from graphene import ObjectType, String, Schema, Field
import os
from rx import Observable
from redisclient import syncredis, asyncredis
import asyncio

loop = asyncio.new_event_loop()
class BuildQuery(ObjectType):
    job_id = String()
    build_log = String()
    server_name = String()

    def resolve_build_log(self, info, **args):
        key = 'job:{id}:log'.format(id=self.job_id)
        return syncredis.get(key)

    def resolve_server_name(self, info):
        return os.environ.get('SERVER_NAME', 'default')

class Query(ObjectType):
    build = Field(BuildQuery, job_id=String())

    def resolve_build(root, info, **args):
        return BuildQuery(args.get('job_id'))
class BuildSubscription(ObjectType):
    job_id = String()
    build_log = String()
    server_name = String()

    def resolve_build_log(self, info, **args):
        key = 'job:{id}:log'.format(id=self.job_id)
        return syncredis.get(key)

    def resolve_server_name(self, info):
        return os.environ.get('SERVER_NAME', 'default')

class Subscription(ObjectType):
    build = Field(BuildSubscription, job_id=String())

    def resolve_build(self, info, **args):
        id = args.get('job_id')

        def async_log_events():
            def on_subscribe(observer):
                observer.on_next(BuildSubscription(id))
                async def subscribe_to_channel(): 
                    key = 'job:{id}:log'.format(id=id)
                    [ch] = await asyncredis.subscribe(key)
                    async for message in ch.iter():
                        observer.on_next(BuildSubscription(id)) 
                
                loop.run_until_complete(subscribe_to_channel())

            return Observable.create(on_subscribe)

        return async_log_events()

schema = Schema(query=Query,  subscription=Subscription)