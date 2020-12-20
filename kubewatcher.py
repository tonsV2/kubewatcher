import kubernetes as k8s
from kubernetes import config


def cli():
    config.load_kube_config()

    core_api = k8s.client.CoreV1Api()
    watcher = k8s.watch.Watch()
    stream = watcher.stream(core_api.list_pod_for_all_namespaces, timeout_seconds=0)
    for raw_event in stream:
#        yaml_path = "status.phase == Failed"
        yaml_path = "status.containerStatuses[*].state.terminated.exitCode != 0"
#        yaml_path = "status.containerStatuses[0].state.terminated.exitCode != 0"
        print("===========================================================================================")
        metadata = raw_event['raw_object']['metadata']
# TODO: If debug
        print(f"Inspecting {metadata['name']} in {metadata['namespace']}")
        if alert(raw_event['raw_object'], yaml_path):
            # TODO: Extract some data/time information as well
            print("ALARM!!!")
            print(f"{metadata['name']} in {metadata['namespace']} terminated with nonzero exit code")


def alert(yaml, yaml_path_str: str) -> bool:
    if yaml_path_str.find("==") != -1:
        path, value = yaml_path_str.split("==")
        values = yaml_path(yaml, path)
        return len(values) > 0 and value.strip() in values

    if yaml_path_str.find("!="):
        path, value = yaml_path_str.split("!=")
        values = yaml_path(yaml, path)
        return len(values) > 0 and not value.strip() in values


def yaml_path(data, path):
    split_path = path.split(".")
    result = []
    yaml_rec(data, split_path, result)
    return result


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
