import os
from dotenv import load_dotenv
import subprocess

from helper_scripts.constants import IMAGE_NAME, IMAGE_TAG

ENV_FILE = "secrets.env"

if os.path.exists(ENV_FILE):
    load_dotenv(dotenv_path=ENV_FILE)

# Parameters
docker_hub_username = os.getenv("DOCKER_HUB_USERNAME", "")
docker_hub_token = os.getenv("DOCKER_HUB_TOKEN", "")
image_name = IMAGE_NAME
image_tag = IMAGE_TAG

try:
    # Get the absolute path of the current script file
    script_directory = os.path.dirname(os.path.abspath(__file__))
    os.chdir(os.path.join(script_directory, ".."))

    # Login to Docker Hub
    docker_login_command = f"docker login -u {docker_hub_username} --password-stdin"
    docker_login_process = subprocess.Popen(docker_login_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE, shell=True)
    docker_login_output, docker_login_error = docker_login_process.communicate(input=docker_hub_token.encode())
    print(docker_login_output.decode())
    print(docker_login_error.decode())

    # Build the Docker image
    build_command = f"docker build --no-cache -t {image_name}:{image_tag} ."
    result_build = subprocess.check_output(build_command, text=True, shell=True)
    print(result_build)

    # Tag the Docker image
    tag_command = f"docker tag {image_name}:{image_tag} {docker_hub_username}/{image_name}:{image_tag}"
    result_tag = subprocess.check_output(tag_command, text=True, shell=True)
    print(result_tag)

    # Push the Docker image to Docker Hub
    push_command = f"docker push {docker_hub_username}/{image_name}:{image_tag}"
    result_push = subprocess.check_output(push_command, text=True, shell=True)
    print(result_push)

    # Logout from Docker Hub
    logout_command = "docker logout"
    result_logout = subprocess.check_output(logout_command, text=True, shell=True)
    print(result_logout)
except Exception as e:
    print(f"Exception: {str(e)}")