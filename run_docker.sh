#!/usr/bin/env bash

#bash: take a image label variable
export imagetag="rate_dog_flask"
# remove image. prune dangling imagesBuild image
docker rmi -f $imagetag:latest
docker system prune -f
docker build --tag $imagetag .

# List docker images
docker image ls

# Run flask app
docker run -p 127.0.0.1:8080:8080 $imagetag
