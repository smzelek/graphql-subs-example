import graphene
import os
from rx import Observable
import random


class SampleQuery(graphene.ObjectType):
    result = graphene.Int()
    server_name = graphene.String()

    def resolve_result(self, info):
        return random.randint(1,101)

    def resolve_server_name(self, info):
        return os.environ.get('SERVER_NAME', 'default')

class Query(graphene.ObjectType):
    sample = graphene.Field(SampleQuery)

    def resolve_sample(root, info):
        return SampleQuery()


class StatefulSecondsCounter(graphene.ObjectType):
    time = graphene.Int()
    server_name = graphene.String()

    def __init__(self, time):
        self.time = time
    
    def resolve_time(self, info):
        return self.time

    def resolve_server_name(self, info):
        return os.environ.get('SERVER_NAME', 'default')

class Subscription(graphene.ObjectType):
    count_seconds = graphene.Field(StatefulSecondsCounter, start_from=graphene.Int(), up_to=graphene.Int())

    def resolve_count_seconds(root, info, start_from=0, up_to=5):
        return Observable.interval(1000)\
            .take_while(lambda i: int(i) + start_from <= up_to)\
            .map(lambda i: StatefulSecondsCounter(i + start_from))

schema = graphene.Schema(query=Query,  subscription=Subscription)