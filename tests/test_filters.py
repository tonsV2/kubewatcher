from unittest import TestCase

from envyaml import EnvYAML

from kubewatcher.kubewatcher import read_configs
from kubewatcher.kubewatcher import trigger


class Test(TestCase):
    def test_filters(self):
        config_file = "./config.yaml"
        config = read_configs([config_file])

        for f in config['filters']:
            if 'tests' in f:
                for test in f['tests']:
                    data = EnvYAML(test).export()
                    triggered = trigger(f, data)
                    if not triggered:
                        print(f)
                    self.assertTrue(triggered)

    def test_ensure_all_filters_are_tested(self):
        config_file = "./config.yaml"
        config = read_configs([config_file])

        for f in config['filters']:
            missing_tests = 'tests' not in f
            if missing_tests:
                print(f)
            self.assertFalse(missing_tests)
