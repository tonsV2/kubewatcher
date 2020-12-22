from pprint import pprint

import kubernetes as k8s
import ruamel.yaml as yaml
from kubernetes import kube_config

from config import config
from handlers import handle


def cli():
    pod_filters = [filter for filter in config['filters'] if filter['kind'] == 'Pod']

    kube_config.load_kube_config()

    core_api = k8s.client.CoreV1Api()
    watcher = k8s.watch.Watch()
    stream = watcher.stream(core_api.list_pod_for_all_namespaces, timeout_seconds=0)
    for raw_event in stream:
        raw_object = raw_event['raw_object']
        name = yaml_path_extract_value(raw_object, "metadata.name")
        namespace = yaml_path_extract_value(raw_object, "metadata.namespace")
        print(f"Inspecting: {name} in {namespace}")
        for pod_filter in pod_filters:
            if trigger(pod_filter, raw_object):
                attributes = extract_message_attributes(pod_filter['message']['attributes'], raw_object)
                message = pod_filter['message']['template'].format(**attributes)
                print(message)


def extract_message_attributes(attributes, raw_object):
    return {attribute: yaml_path_extract_value(raw_object, path) for attribute, path in attributes.items()}


def trigger(filter, raw_object):
    if 'apiVersion' in filter and filter['apiVersion'] != raw_object['apiVersion']:
        return False

    namespace = raw_object['metadata']['namespace']
    if 'namespaces' in filter and ('ignore' in filter['namespaces'] and namespace in filter['namespaces']['ignore']
            or 'include' in filter['namespaces'] and namespace not in filter['namespaces']['include']):
        return False

    should_trigger = False
    for t in filter['triggers']:
        should_trigger = alert(raw_object, t)
    return should_trigger


def alert(yaml, yaml_path_str: str) -> bool:
    if yaml_path_str.find("==") != -1:
        path, value = yaml_path_str.split("==")
        values = yaml_path(yaml, path)
        return len(values) > 0 and value.strip() in values

    if yaml_path_str.find("!="):
        path, value = yaml_path_str.split("!=")
        values = yaml_path(yaml, path)
        return len(values) > 0 and not value.strip() in values


def yaml_path(data, path) -> []:
    split_path = path.split(".")
    result = []
    yaml_rec(data, split_path, result)
    return result


def yaml_path_extract_value(data, path) -> str:
    split_path = path.split(".")
    result = []
    yaml_rec(data, split_path, result)
    return result[0]


def yaml_rec(data, split_path, result):
    path_part = split_path.pop(0).strip()
#    if len(split_path) == 0 and path_part.endswith("]"):
#        find = path_part.find("[")
#        index = path_part[find + 1:-1]
#        path_part_without_index = path_part[0:find]
#        if index == "*":
#            result.append(data[path_part_without_index])
#        else:
#            result.append(data[path_part_without_index][int(index)])
    if len(split_path) == 0:
        result.append(str(data[path_part]))
    else:
        if path_part.endswith("]"):
            find = path_part.find("[")
            index = path_part[find + 1:-1]
            path_part_without_index = path_part[0:find]
            if index == "*":
                if path_part_without_index in data:
                    for d in data[path_part_without_index]:
                        yaml_rec(d, split_path.copy(), result)
            else:
                return yaml_rec(data[path_part_without_index][int(index)], split_path, result)
        else:
            if path_part in data:
                return yaml_rec(data[path_part], split_path, result)


if __name__ == "__main__":
    cli()
