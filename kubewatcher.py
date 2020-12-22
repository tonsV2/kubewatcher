import kubernetes as k8s
from kubernetes.config import kube_config

from config import config
from handlers import handle
from path_extractor import extract_value, extract_values


def cli():
    pod_filters = [filter for filter in config['filters'] if filter['kind'] == 'Pod']

    kube_config.load_kube_config()

    core_api = k8s.client.CoreV1Api()
    watcher = k8s.watch.Watch()
    stream = watcher.stream(core_api.list_pod_for_all_namespaces, timeout_seconds=0)
    for raw_event in stream:
        raw_object = raw_event['raw_object']
        name = extract_value(raw_object, "metadata.name")
        namespace = extract_value(raw_object, "metadata.namespace")
        print(f"Inspecting: {name} in {namespace}")
        for pod_filter in pod_filters:
            if trigger(pod_filter, raw_object):
                message = generate_message(pod_filter['message'], raw_object)
                print(message)
                handle(message, raw_object)


def generate_message(message_data, raw_object):
    attributes = {attribute: extract_value(raw_object, path) for attribute, path in message_data['attributes'].items()}
    message = message_data['template'].format(**attributes)
    return message


def trigger(pod_filter, raw_object):
    api_version_does_not_match = 'apiVersion' in pod_filter and pod_filter['apiVersion'] != raw_object['apiVersion']
    if api_version_does_not_match:
        return False

    namespace = raw_object['metadata']['namespace']
    if 'namespaces' in pod_filter:
        namespaces = pod_filter['namespaces']
        namespace_ignored = 'ignore' in namespaces and namespace in namespaces['ignore']
        namespace_not_included = 'include' in namespaces and namespace not in namespaces['include']
        if namespace_ignored or namespace_not_included:
            return False

    should_trigger = False
    for t in pod_filter['trigger']:
        should_trigger = alert(raw_object, t)
    return should_trigger


def alert(yaml, yaml_path_str: str) -> bool:
    if yaml_path_str.find("==") != -1:
        path, value = yaml_path_str.split("==")
        values = extract_values(yaml, path)
        return len(values) > 0 and value.strip() in values

    if yaml_path_str.find("!="):
        path, value = yaml_path_str.split("!=")
        values = extract_values(yaml, path)
        return len(values) > 0 and not value.strip() in values


if __name__ == "__main__":
    cli()
