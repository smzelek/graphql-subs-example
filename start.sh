# export SERVER_NAME=instance1 SERVER_PORT=5000 && python3 wsgi.py
# export SERVER_NAME=instance2 SERVER_PORT=5001 && python3 wsgi.py
# npm start

service nginx stop
cp ./nginx.conf /usr/share/nginx
nginx -c nginx.conf
service redis-server start
# lsof -i tcp:5000 | awk 'NR!=1 {print $2}' | xargs kill