from graphene import ObjectType, String, Schema, Field, Int
import os
from rx import Observable
from redisclient import syncredis
import asyncio

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
        return Observable.interval(1000).map(lambda i: BuildSubscription(args.get('job_id')))

schema = Schema(query=Query,  subscription=Subscription)