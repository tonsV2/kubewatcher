from setuptools import setup, find_packages

description = 'Please see https://github.com/tonsV2/kubewatcher for details'

setup(
    name='kubewatcher',
    version='1.7.0',
    description=description,
    python_requires='>=3.7',
    packages=find_packages(),
    install_requires=[
        'kubernetes~=12.0.1',
        'envyaml~=1.1.201202',
        'twine~=3.3.0',
        'click~=7.1.2',
        'yamlpath~=3.4.0',
    ],
    entry_points={
        'console_scripts': ['kubewatcher=kubewatcher.cli:cli']
    },
    long_description=description,
)
