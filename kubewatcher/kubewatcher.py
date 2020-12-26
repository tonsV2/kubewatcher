import os

import click
import kubernetes as k8s
from envyaml import EnvYAML
from kubernetes.config import kube_config, incluster_config

from kubewatcher.handlers import handle
from kubewatcher.path_extractor import extract_value, evaluate_path
from kubewatcher.thread_launcher import ThreadLauncher


@click.command()
@click.option('--config-file', '-f', "config_files", multiple=True, default=["config.yaml"])
def cli(config_files):
    config = read_configs(config_files)

    read_kube_config()

    core_api = k8s.client.CoreV1Api()
    batch_v1_api = k8s.client.BatchV1Api()
    batch_v1_beta_api = k8s.client.BatchV1beta1Api()

    resource_map = {
        "Event": core_api.list_event_for_all_namespaces,
        "Pod": core_api.list_pod_for_all_namespaces,
        "Service": core_api.list_service_for_all_namespaces,
        "Node": core_api.list_node,
        "Job": batch_v1_api.list_job_for_all_namespaces,
        "CronJob": batch_v1_beta_api.list_cron_job_for_all_namespaces
    }

    kinds = {filter['kind'] for filter in config['filters']}
    print(f"Kinds observed: {list(kinds)}")
    print(f"Handlers: {list(config['handlers'].keys())}")

    resources = {kind: resource_map[kind] for kind in kinds}

    launcher = ThreadLauncher()
    for kind, resource in resources.items():
        filters = [filter for filter in config['filters'] if filter['kind'] == kind]
        launcher.launch(resource_watcher, [config, resource, filters, kind])
    launcher.join()


def resource_watcher(config, resource, pod_filters, kind):
    watcher = k8s.watch.Watch()
    stream = watcher.stream(resource, timeout_seconds=0)
    for raw_event in stream:
        raw_object = raw_event['raw_object']
        name = extract_value(raw_object, "metadata.name")
        namespace = extract_value(raw_object, "metadata.namespace")
        print(f"{kind}: {name} in {namespace}")
        for pod_filter in pod_filters:
            if trigger(pod_filter, raw_object):
                message = generate_message(pod_filter['message'], raw_object)
                print(f"❌ {message}")
                handle(config, message, raw_object)


def generate_message(message_data, raw_object):
    attributes = {attribute: extract_value(raw_object, path) for attribute, path in message_data['attributes'].items()}
    message = message_data['template'].format(**attributes)
    return message


def trigger(pod_filter, raw_object):
    if api_version_does_not_match(pod_filter, raw_object):
        return False

    namespace = raw_object['metadata']['namespace']
    if 'namespaces' in pod_filter:
        namespaces = pod_filter['namespaces']
        if namespace_ignored(namespace, namespaces) or namespace_not_included(namespace, namespaces):
            return False

    conditions = [evaluate_path(raw_object, condition) for condition in pod_filter['conditions']]
    return all(conditions)


def api_version_does_not_match(pod_filter, raw_object):
    return 'apiVersion' in pod_filter and pod_filter['apiVersion'] != raw_object['apiVersion']


def namespace_ignored(namespace, namespaces):
    return 'ignore' in namespaces and namespace in namespaces['ignore']


def namespace_not_included(namespace, namespaces):
    return 'include' in namespaces and namespace not in namespaces['include']


def read_configs(config_files: []) -> {}:
    """
    Each file in config_files will be read and added to the config object.
    Filters will be appended but handlers will be merged since they are uniq by name.

    :param config_files: []
    :return: An object containing the combined configuration
    """
    config = {
        "filters": [],
        "handlers": {}
    }

    for config_file in config_files:
        yaml = EnvYAML(config_file)
        config["filters"] += yaml["filters"]
        if 'handlers' in yaml:
            config["handlers"] = {**config["handlers"], **yaml["handlers"]}

    return config


def read_kube_config():
    if "KUBERNETES_SERVICE_HOST" in os.environ:
        incluster_config.load_incluster_config()
    else:
        kube_config.load_kube_config()
