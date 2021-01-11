from envyaml import EnvYAML


def parse_config_files(config_files: []) -> {}:
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
