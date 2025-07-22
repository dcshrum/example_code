
Run reporting container
/usr/bin/docker run  -it --rm --network host --mount source=warehouse_temp_files,target=/warehouse_temp_files --mount source=donny,target=/reports --mount source=SSL,target=/SSL --mount source=logs,target=/logs --mount type=bind,source=/home/xxxx/reporting/,target=/reporting --entrypoint=/bin/bash xxxxxx/reporting:latest

Run web container
/usr/bin/docker run --rm -it --network host --mount source=certs,target=/certs --mount source=warehouse_temp_files,target=/warehouse_temp_files --mount source=SSL,target=/SSL --mount source=logs,target=/logs --mount type=bind,source=/home/xxxx/reporting/,target=/reporting --entrypoint=/bin/bash xxxxxx/web:latest

Run Redis 
/usr/bin/docker run -d --rm --name=redis  --mount source=SSL,target=/usr/local/etc/redis -p 6379:6379 redis redis-server /usr/local/etc/redis/redis.conf

Run Mysql
docker run --rm --name=local-mysql -p 3306:3306 --mount source=warehouse_temp_files,target=/warehouse_temp_files --mount source=mysql,target=/var/lib/mysql -e MYSQL_ROOT_PASSWORD=xxxxx -d mysql:latest --secure-file-priv=/warehouse_temp_files --local-infile=ON

#### Some mysql notes 
-ssl-mode=REQUIRED <<<  This setting does not work with Docker!
2023-06-26T15:09:40.658054Z 0 [ERROR] [MY-000067] [Server] unknown variable 'ssl-mode=REQUIRED'.
no text editor in the mysql container -- ugh 
have to use - this would force a specific CA certificate
sed -i 's/\[mysqld\]/\[mysqld\]\nrequire_secure_transport=ON/' /etc/my.cnf
sed -i 's/\[client\]/\[client\]\nssl-key=\/mysql\/client-key.pem/' /etc/my.cnf
sed -i 's/\[client\]/\[client\]\nssl-cert=\/mysql\/client-cert.pem/' /etc/my.cnf
sed -i 's/\[client\]/\[client\]\nssl-mode=VERIFY_CA/' /etc/my.cnf

You ALSO have to force it per user with - ALTER USER 'root'@'%' REQUIRE X509;

--Problems with powerBI, it has limited integration with mysql.  Will just force ANY SSL which includes TLS


########## windows syntax example
docker run -it --rm --network host --mount source=warehouse_temp_files,target=/warehouse_temp_files -v //c/Users/xxxxx/reporting:/reporting --entrypoint=/bin/bash xxxxx/reporting:latest

#####################################
To copy files to a volume on Windows - 
Go to the docker network share - 
\\wsl.localhost\docker-desktop-data\version-pack-data\community\docker\volumes\

