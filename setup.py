import os

from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='kubewatcher',
    version='1.0.0',
    description='See https://github.com/tonsV2/kubewatcher',
    python_requires='>=3.8',
    py_modules=['kubewatcher'],
    install_requires=[
        'kubernetes==12.0.1',
        'ruamel.yaml==0.16.12',
        'yamlpath==3.4.0'
    ],
    entry_points='''
        [console_scripts]
        kubewatcher=kubewatcher:cli
    ''',
    long_description=read('README.md'),
)
