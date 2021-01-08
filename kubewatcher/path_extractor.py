from yamlpath import Processor
from yamlpath.exceptions import YAMLPathException
from yamlpath.wrappers import ConsolePrinter


def evaluate_path(obj: {}, path_str: str) -> bool:
    values = extract_values(obj, path_str)
    return len(values) > 0


def extract_value(data: {}, path: str) -> str:
    values = extract_values(data, path)
    if len(values) > 1:
        raise MultipleValuesException(f"Expected single value, got: {values}")
    return values[0]


def extract_values(data: {}, path: str) -> []:
    class Args:
        debug = True
        verbose = False
        quiet = True

    args = Args()
    log = ConsolePrinter(args)

    try:
        processor = Processor(log, data)
        nodes = processor.get_nodes(path)
        return [n.node for n in nodes]
    except YAMLPathException as ex:
        print(ex)


class MultipleValuesException(Exception):
    pass
