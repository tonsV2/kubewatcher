import ruamel.yaml as yaml


def read_config():
    yaml_file = "config.yaml"
    with open(yaml_file) as stream:
        try:
            yaml_data = yaml.safe_load(stream)
            return yaml_data
        except yaml.YAMLError as exc:
            print(exc)


config = read_config()
