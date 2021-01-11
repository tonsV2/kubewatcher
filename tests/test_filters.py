from unittest import TestCase

from ruamel import yaml

from kubewatcher.cli import parse_config_files
from kubewatcher.kubewatcher import KubeWatcher


class Test(TestCase):
    def test_filters(self):
        config_file = "./config.yaml"
        config = parse_config_files([config_file])

        filters = KubeWatcher(config).filters

        for f in filters:
            for test in f.tests:
                with open(test, 'r') as stream:
                    data = yaml.safe_load(stream)
                    triggered = f.trigger(data)
                    if not triggered:
                        print(yaml.dump(f))
                    self.assertTrue(triggered)

    def test_ensure_all_filters_are_tested(self):
        config_file = "./config.yaml"
        config = parse_config_files([config_file])

        filters = KubeWatcher(config).filters

        for f in filters:
            missing_tests = not f.tests
            if missing_tests:
                print(yaml.dump(f))
            self.assertFalse(missing_tests)
