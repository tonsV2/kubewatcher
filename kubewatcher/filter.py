from kubewatcher.path_extractor import extract_value, evaluate_path


class Filter(object):
    def __init__(self, filter: {}):
        self.kind: str = filter['kind']
        self.api_version: str = filter['apiVersion'] if 'apiVersion' in filter else None
        self.namespaces: {} = filter['namespaces'] if 'namespaces' in filter else None
        self.conditions: [] = filter['conditions']
        self.message_data: {} = filter['message']
        self.tests: [] = filter['tests']

    def generate_message(self, raw_object: {}) -> str:
        attributes = {attribute: extract_value(raw_object, path) for attribute, path in self.message_data['attributes'].items()}
        message = self.message_data['template'].format(**attributes)
        return message

    def trigger(self, raw_object: {}) -> bool:
        if self.__api_version_does_not_match(raw_object['apiVersion']):
            return False

        if self.__has_namespace(raw_object):
            namespace = raw_object['metadata']['namespace']
            if self.namespaces:
                if self.__namespace_ignored(namespace) or self.__namespace_not_included(namespace):
                    return False

        conditions = [evaluate_path(raw_object, condition) for condition in self.conditions]
        return all(conditions)

    def __api_version_does_not_match(self, api_version: str) -> bool:
        return self.api_version and self.api_version != api_version

    @staticmethod
    def __has_namespace(raw_object: {}):
        return 'metadata' in raw_object and 'namespace' in raw_object['metadata']

    def __namespace_ignored(self, namespace: str) -> bool:
        return 'ignore' in self.namespaces and namespace in self.namespaces['ignore']

    def __namespace_not_included(self, namespace: str) -> bool:
        return 'include' in self.namespaces and namespace not in self.namespaces['include']
