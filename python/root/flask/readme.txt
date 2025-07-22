

Run redis for caching - 
docker run -d --restart unless-stopped --name=redis  --mount source=SSL,target=/usr/local/etc/redis -p 6379:6379 redis redis-server /usr/local/etc/redis/redis.conf


### Note the folder is now passed in as an environment variable ###
-e application=log_viewer for example.  The value cooresponds to the folder name.  
see docker/flask/start.sh for how it is used. 


### Run in test:
/usr/bin/docker run --rm -it --network host --mount source=certs,target=/certs --mount source=warehouse_temp_files,target=/warehouse_temp_files --mount source=SSL,target=/SSL --mount source=logs,target=/logs --mount type=bind,source=/home/YOU/reporting/,target=/reporting --entrypoint=/bin/bash xxxxxxx/web:latest
docker run -d --rm --name=redis  --mount source=SSL,target=/usr/local/etc/redis -p 6379:6379 redis redis-server /usr/local/etc/redis/redis.conf

### Run in production example for API server:
/usr/bin/docker run -e application=data_lake --restart unless-stopped --detach --name web_api --network host --mount source=certs,target=/certs --mount source=warehouse_temp_files,target=/warehouse_temp_files --mount source=SSL,target=/SSL --mount source=logs,target=/logs xxxxxxx/web:latest

### Restart web api and redis in production
docker stop redis && docker rm redis && docker run --detach --restart unless-stopped --name=redis --mount source=SSL,target=/usr/local/etc/redis -p 6379:6379 redis redis-server /usr/local/etc/redis/redis.conf 
docker stop web_api && docker rm web_api && /usr/bin/docker run -e application=data_lake --restart unless-stopped  --detach --name web_api --network host --mount source=certs,target=/certs --mount source=warehouse_temp_files,target=/warehouse_temp_files --mount source=SSL,target=/SSL --mount source=logs,target=/logs xxxxx/web:latest && docker logs --follow web_api