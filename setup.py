from setuptools import setup, find_packages

description = 'Please see https://github.com/tonsV2/kubewatcher for details'

setup(
    name='kubewatcher',
    version='1.6.0',
    description=description,
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
    long_description=description,
)
