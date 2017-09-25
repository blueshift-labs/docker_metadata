import os
import requests
import datetime
import time

def ec2_host_ip():
    host_ip = requests.get('http://169.254.169.254/latest/meta-data/local-ipv4').content
    return host_ip

def get_ecs_introspection_url(resource):
    # 172.17.0.1 is the docker network bridge ip
    return 'http://172.17.0.1:51678/v1/' + resource

def contains_key(d, key):
    return key in d and d[key] is not None


def ecs_instance_metadata():
    # http://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-agent-introspection.html
    instance_metadata = requests.get(get_ecs_introspection_url('metadata')).json()
    return instance_metadata

def get_local_container_info(docker_id):
    # http://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-agent-introspection.html
    ecs_local_task = requests.get(get_ecs_introspection_url('tasks') + '?dockerid=' + docker_id).json()

    task_arn = ecs_local_task['Arn']

    if task_arn is None:
        raise Exception("Unable to find task arn for container %s in ecs introspection api" % docker_id)

    ecs_local_container = None

    if contains_key(ecs_local_task, 'Containers'):
        for c in ecs_local_task['Containers']:
            if c['DockerId'] == docker_id:
                ecs_local_container = c

    if ecs_local_container is None:
        raise Exception("Unable to find container %s in ecs introspection api" % docker_id)

    return ecs_local_container, ecs_local_task, task_arn

