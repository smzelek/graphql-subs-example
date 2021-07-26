from flask import Flask
from graphql.backend import GraphQLCoreBackend
from flask_sockets import Sockets
from flask_graphql import GraphQLView
from graphql_ws.gevent import  GeventSubscriptionServer
from flask_cors import CORS
import os
from schema import schema
from redisclient import syncredis
from graphql.execution.executors.asyncio import AsyncioExecutor
import asyncio
import lorem

class GraphQLCustomCoreBackend(GraphQLCoreBackend):
    def __init__(self, executor=None):
        super().__init__(executor)
        self.execute_params['allow_subscriptions'] = True

app = Flask(__name__)
CORS(app)
PORT = int(os.environ.get('SERVER_PORT'))

app.debug = True
app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, backend=GraphQLCustomCoreBackend(), graphiql=True))

sockets = Sockets(app)
subscription_server = GeventSubscriptionServer(schema)
app.app_protocol = lambda environ_path_info: 'graphql-ws'

@sockets.route('/subscriptions')
def echo_socket(ws):
    subscription_server.handle(ws)
    return []

@app.route('/append/<id>')
def append(id):
    key = 'job:{id}:log'.format(id=id)

    log = syncredis.get(key) or ''
    log += lorem.sentence() + "\n"

    syncredis.set(key, log)

    print("Appended to build log for job", id)

    return "OK"
