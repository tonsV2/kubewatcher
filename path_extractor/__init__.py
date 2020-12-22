def extract_values(data, path) -> []:
    split_path = path.split(".")
    result = []
    yaml_rec(data, split_path, result)
    return result


def extract_value(data, path) -> str:
    split_path = path.split(".")
    result = []
    yaml_rec(data, split_path, result)
    # TODO: assert len(result) == 1 || raise exception
    return result[0]


def yaml_rec(data, split_path, result):
    path_part = split_path.pop(0).strip()
    # if len(split_path) == 0 and path_part.endswith("]"):
    #     find = path_part.find("[")
    #     index = path_part[find + 1:-1]
    #     path_part_without_index = path_part[0:find]
    #     if index == "*":
    #         result.append(data[path_part_without_index])
    #     else:
    #         result.append(data[path_part_without_index][int(index)])
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
