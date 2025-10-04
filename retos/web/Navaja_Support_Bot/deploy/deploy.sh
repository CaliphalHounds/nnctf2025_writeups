#!/bin/bash
PUBLIC_PORT=5002
PRIVATE_PORT=5002

# Check running as root
if [[ $(/usr/bin/id -u) -ne 0 ]]; then
    echo "Not running as root"
    exit 1
fi

# Need a name for the container
if [ $# -eq 1 ]
  then
        BUILD_NAME=$1
else
        echo "Usage:"
        echo $0 "BUILD_NAME"
        exit 2
fi

# Check if container is running or exited then stop and rm
if [ "$( docker container inspect -f '{{.State.Status}}' $BUILD_NAME )" == "running" ] ||
   [ "$( docker container inspect -f '{{.State.Status}}' $BUILD_NAME )" == "exited"  ]
then
        docker stop $BUILD_NAME
        docker rm -f $BUILD_NAME >/dev/null 2>&1 || true
fi

# build and start container
docker build -t  $BUILD_NAME .
docker rm -f $BUILD_NAME >/dev/null 2>&1 || true
docker run --name  $BUILD_NAME -itd  --restart unless-stopped -p $PUBLIC_PORT:$PRIVATE_PORT $BUILD_NAME 
echo "Sleeping for 3 seconds ... "
sleep 3
# Check service connection
test_command=$( nc -zv localhost $PUBLIC_PORT )
if [ $? -eq 0 ]; then
        echo "PORT $PUBLIC_PORT is open! Test successfully completed."
else
        echo "Test has been failed"
fi
