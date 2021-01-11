import logging

import click

from kubewatcher.kubewatcher import KubeWatcher
from kubewatcher.parse_config_files import parse_config_files

log_format = '%(asctime)s %(levelname)s:%(message)s'
logging.basicConfig(level=logging.INFO, format=log_format)


@click.group()
def cli():
    pass


@cli.command()
@click.option('--config-file', '-f', "config_files", multiple=True, default=["config.yaml"])
@click.option('--kube-config-file', '-k', default=None)
@click.option('--context', '-c', default=None)
def watch(config_files: [], kube_config_file: str, context: str) -> None:
    config = parse_config_files(config_files)
    KubeWatcher(config).watch(kube_config_file, context)


@cli.command()
@click.option('--config-file', '-f', "config_files", multiple=True, default=["config.yaml"])
@click.option('--verbose', '-v', default=None, is_flag=True)
def test_filters(config_files: [], verbose: bool) -> None:
    config = parse_config_files(config_files)
    KubeWatcher(config).test_filters(verbose)
