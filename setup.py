import os

from setuptools import setup, find_packages


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name='kubewatcher',
    version='1.5.0',
    description='See https://github.com/tonsV2/kubewatcher',
    python_requires='>=3.8',
    packages=find_packages(),
    install_requires=[
        'kubernetes~=12.0.1',
        'ruamel.yaml~=0.16.12',
        'envyaml~=1.1.201202',
        'twine~=3.3.0',
        'click~=7.1.2',
    ],
    entry_points={
        'console_scripts': ['kubewatcher=kubewatcher.kubewatcher:cli']
    },
    long_description=read('README.md'),
)
