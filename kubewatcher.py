import kubernetes as k8s
from kubernetes.config import kube_config

from config import config
from handlers import handle
from path_extractor import extract_value, evaluate_path
from thread_launcher import ThreadLauncher


def cli():
    kube_config.load_kube_config()

    core_api = k8s.client.CoreV1Api()
    batch_v1_api = k8s.client.BatchV1Api()
    batch_v1_beta_api = k8s.client.BatchV1beta1Api()

    resource_map = {
        "Event": core_api.list_event_for_all_namespaces,
        "Pod": core_api.list_pod_for_all_namespaces,
        "Service": core_api.list_service_for_all_namespaces,
        "Job": batch_v1_api.list_job_for_all_namespaces,
        "CronJob": batch_v1_beta_api.list_cron_job_for_all_namespaces
    }

    kinds = {filter['kind'] for filter in config['filters']}
    print(f"Kinds observed: {kinds}")
    resources = {kind: resource_map[kind] for kind in kinds}

    launcher = ThreadLauncher()
    for kind, resource in resources.items():
        filters = [filter for filter in config['filters'] if filter['kind'] == kind]
        launcher.launch(resource_watcher, [resource, filters, kind])
    launcher.join()


def resource_watcher(resource, pod_filters, kind):
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

    conditions = [evaluate_path(raw_object, t) for t in pod_filter['conditions']]
    return all(conditions)


if __name__ == "__main__":
    cli()
