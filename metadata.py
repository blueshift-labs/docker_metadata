import os
import docker_metadata as m
import ec2_metadata as ec2

def ecs_inspect(docker_id):
    if os.environ.get('ECS_METADATA') != "true":
        return {}
    instance_metadata = ec2.ecs_instance_metadata()
    ecs_local_container_metadata, task_metadata, , task_arn = ec2.get_local_container_info(docker_id)
    ecs_metadata = {
        'Cluster': instance_metadata["Cluster"],
        'ContainerInstanceArn': instance_metadata["ContainerInstanceArn"],
        'AgentVersion': instance_metadata["Version"],
        'TaskArn': task_arn,
        'ContainerID': ecs_local_container_metadata["DockerId"],
        'Status': task_metadata["KnownStatus"]
    }
    return ecs_metadata

def port_mappings(ports_dict):
    mapping_arr = []
    for port_key, mappings in ports_dict.iteritems():
        split = port_key.split("/")
        port = split[0]
        proto = split[1]
        for mapping in mappings:
            mapped = {
                'ContainerPort': mapping["HostPort"],
                'HostPort': port,
                'BindIP': mapping["HostIp"],
                'Protocol': proto
            }
            mapping_arr.append(mapped)
    return mapping_arr


def docker_inspect(docker_id):
    meta = m.get_docker_metadata(docker_id)
    docker_long_id = meta["Id"]
    config = meta["Config"]
    net = meta["NetworkSettings"]
    host_ip = ec2.ec2_host_ip()
    docker_metadata = {
        'HostIP': host_ip,
        'Id': docker_long_id,
        'Image': config["Image"],
        'NetworkMode': meta["HostConfig"]["NetworkMode"],
        'Network': {
            'IPAddress': net["IPAddress"],
            'Gateway': net["Gateway"],
            'Ports': port_mappings(net["Ports"]),
        }
    }
    return docker_long_id, docker_metadata

