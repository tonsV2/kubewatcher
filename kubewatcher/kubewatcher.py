import logging
import os
from collections import defaultdict

import kubernetes as k8s
from envyaml import EnvYAML
from kubernetes.config import incluster_config, kube_config
from ruamel import yaml

from kubewatcher.filter import Filter
from kubewatcher.handlers import handle
from kubewatcher.path_extractor import extract_value
from kubewatcher.thread_launcher import ThreadLauncher


class KubeWatcher(object):
    def __init__(self, config: {}):
        self.config = config

        self.filters: [Filter] = [Filter(f) for f in self.config['filters']]
        self.filters_by_kind = defaultdict(list)
        for f in self.filters:
            self.filters_by_kind[f.kind].append(f)

    def watch(self, kube_config_file, context):
        self.__read_kube_config(kube_config_file, context)

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

        kinds = {f['kind'] for f in self.config['filters']}
        logging.info(f"Kinds observed: {list(kinds)}")

        handlers = list(self.config['handlers'].keys())
        if handlers:
            logging.info(f"Handlers: {handlers}")
        else:
            logging.warning("No handlers defined!")

        resources = {kind: resource_map[kind] for kind in kinds}

        launcher = ThreadLauncher()
        for kind, resource in resources.items():
            launcher.launch(self.__resource_watcher, [resource, self.filters_by_kind[kind], kind])
        launcher.join()

    def __resource_watcher(self, resource: classmethod, filters: {}, kind: str) -> None:
        resource_version = 0
        while True:
            watcher = k8s.watch.Watch()
            stream = watcher.stream(resource, timeout_seconds=0, resource_version=resource_version)
            for raw_event in stream:
                raw_object = raw_event['raw_object']
                self.__log_current_object(raw_object, kind)
                for filter in filters:
                    if filter.trigger(raw_object):
                        message = filter.generate_message(raw_object)
                        logging.info(f"❌ {message}")
                        handle(self.config, message, raw_object)
            resource_version = resource().metadata.resource_version

    def __log_current_object(self, raw_object: {}, kind: str):
        name = extract_value(raw_object, "metadata.name")
        if self.__has_namespace(raw_object):
            namespace = extract_value(raw_object, "metadata.namespace")
            logging.info(f"{kind}: {name} in {namespace}")
        else:
            logging.info(f"{kind}: {name}")

    @staticmethod
    def __has_namespace(raw_object: {}):
        return 'metadata' in raw_object and 'namespace' in raw_object['metadata']

    @staticmethod
    def __read_kube_config(kube_config_file: str = None, context: str = None) -> None:
        if "KUBERNETES_SERVICE_HOST" in os.environ:
            incluster_config.load_incluster_config()
        else:
            kube_config.load_kube_config(kube_config_file, context)

    def test_filters(self, verbose: bool):
        failed = False
        for f in self.filters:
            for test in f.tests:
                data = EnvYAML(test).export()
                triggered = f.trigger(data)
                if not triggered:
                    failed = True
                    print(f"❌ {yaml.dump(f)}")
                elif verbose:
                    print(f"✅ {yaml.dump(f)}")
        if not failed:
            print(f"✅ All filter tests passed!")
