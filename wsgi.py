from gevent import monkey; monkey.patch_all()
from app import app
import os
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

if __name__ == '__main__':
    print("Server running")
    server = pywsgi.WSGIServer(('', int(os.environ.get('SERVER_PORT'))), app, handler_class=WebSocketHandler)
    server.serve_forever()


