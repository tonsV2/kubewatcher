from envyaml import EnvYAML


def read_config():
    yaml_file = "config.yaml"
    return EnvYAML(yaml_file)


config = read_config()
