import os
import docker

client = docker.from_env(version='auto')


def get_contents(filename):
    with open(filename) as f:
        return f.read()

def get_docker_metadata(docker_id):
    docker_metadata = client.api.inspect_container(docker_id)
    return docker_metadata

def get_docker_id():
    docker_id = os.path.basename(get_contents("/proc/1/cpuset")).strip()

    if docker_id is None:
        raise Exception("Unable to find docker id")
    return docker_id
