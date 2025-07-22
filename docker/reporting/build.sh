set -e
docker image prune -a -f 
docker builder prune -a -f

export DOCKER_BUILDKIT=1
docker build --tag xxxxxxx/reporting:latest .

docker push xxxxxxxx/reporting:latest
