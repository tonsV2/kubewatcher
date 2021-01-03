import os
from unittest import TestCase
from unittest.mock import patch

from kubewatcher.kubewatcher import read_kube_config


class Test(TestCase):
    @patch("kubernetes.config.incluster_config.load_incluster_config")
    def test_read_kube_config__load_incluster_config(self, load_incluster_config):
        os.environ['KUBERNETES_SERVICE_HOST'] = "some value"

        read_kube_config()

        load_incluster_config.assert_called()
        del os.environ['KUBERNETES_SERVICE_HOST']

    @patch("kubernetes.config.kube_config.load_kube_config")
    def test_read_kube_config__load_kube_config2(self, load_kube_config):
        read_kube_config()

        load_kube_config.assert_called()
