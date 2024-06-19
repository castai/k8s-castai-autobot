#!/bin/bash

# Load environment variables from secrets.env
ENV_FILE="secrets.env"
if [ -f "$ENV_FILE" ]; then
  source "$ENV_FILE"
fi

# Parameters
docker_hub_username="$DOCKER_HUB_USERNAME"
docker_hub_token="$DOCKER_HUB_TOKEN"
image_name="your_image_name"  # Replace with your actual image name
image_tag="your_image_tag"    # Replace with your actual image tag

try {
  # Get the absolute path of the current script file
  script_directory="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
  cd "$script_directory/.."

  # Login to Docker Hub
  echo "$docker_hub_token" | docker login -u "$docker_hub_username" --password-stdin

  # Build the Docker image
  docker build --no-cache -t "${image_name}:${image_tag}" .

  # Tag the Docker image
  docker tag "${image_name}:${image_tag}" "${docker_hub_username}/${image_name}:${image_tag}"

  # Push the Docker image to Docker Hub
  docker push "${docker_hub_username}/${image_name}:${image_tag}"

  # Logout from Docker Hub
  docker logout
} catch {
  echo "Exception: $?"
}
