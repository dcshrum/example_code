set -x
docker image prune -a -f 
docker builder prune -a -f

export DOCKER_BUILDKIT=1
docker build --tag xxxxxx/web:latest .

docker push xxxxxxx/web:latest

