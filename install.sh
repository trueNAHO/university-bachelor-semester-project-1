#!/usr/bin/env sh

# Install script to run the application inside a temporary docker container.

# Make sure the `docker` command is available.
if ! command -v docker >/dev/null; then
    printf '[ERROR] %s: docker: command not found\n' "$0" >&2
    exit 1
fi

docker_image="university_of_luxembourg_bsp1_encrypt_in_the_middle"
readonly docker_image

# Build and run the docker image.
docker build -t "$docker_image" . && docker run -it --rm "$docker_image"

# Remove the docker image.
docker rmi "$docker_image"
