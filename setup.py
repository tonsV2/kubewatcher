import os

from setuptools import setup


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name='kubewatcher',
    version='1.2.0',
    description='See https://github.com/tonsV2/kubewatcher',
    python_requires='>=3.8',
    py_modules=['kubewatcher'],
    packages=['config', 'handlers', 'path_extractor', 'thread_launcher'],
    install_requires=[
        'kubernetes~=12.0.1',
        'ruamel.yaml~=0.16.12',
        'envyaml~=1.1.201202'
    ],
    entry_points={
        'console_scripts': ['kubewatcher=kubewatcher.kubewatcher:cli']
    },
    long_description=read('README.md'),
)
