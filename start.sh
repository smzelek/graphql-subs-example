service nginx stop
cp ./nginx.conf /usr/share/nginx
nginx -c nginx.conf
service redis-server start
# export SERVER_PORT=5000 SERVER_NAME=instance1 && uwsgi --ini uwsgi.ini
# lsof -i tcp:5000 | awk 'NR!=1 {print $2}' | xargs kill
# export SERVER_PORT=5000 SERVER_NAME=instance1 && python3 wsgi.py