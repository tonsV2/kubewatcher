from enum import Enum


class Operator(Enum):
    EQUAL = "=="
    NOT_EQUAL = "!="
    LESS_THAN = "<"
    GRATER_THAN = ">"


def evaluate_path(obj, path_str: str) -> bool:
    operator = __get_operator(path_str)
    left, right = path_str.split(operator.value)
    values = extract_values(obj, left)
    cmp = False
    for value in values:
        cmp = __compare(value.strip(), operator, right.strip())
        if cmp:
            return True
    return cmp


def __compare(left: str, operator: Operator, right: str) -> bool:
    if operator == Operator.EQUAL:
        return left == right

    if operator == Operator.NOT_EQUAL:
        return left != right

    if operator == Operator.LESS_THAN:
        return int(left) < int(right)

    if operator == Operator.GRATER_THAN:
        return int(left) > int(right)


def __get_operator(path_str):
    operators = ["==", "!=", "<", ">"]
    for operator in operators:
        if path_str.find(operator) != -1:
            return Operator(operator)


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
    if not split_path:
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
