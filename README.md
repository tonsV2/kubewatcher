# Kube Watcher
Simple and highly configurable Kubernetes monitor

The idea is that you can define a filter and if there's a match it will be handled by the handlers you define.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
- [Kube Watcher](#kube-watcher)

- [Configuration](#configuration)
  - [Handlers](#handlers)
- [Install](#install)
- [Run](#run)
  - [Natively](#natively)
  - [Docker](#docker)
  - [Helm](#helm)
- [Development Setup](#development-setup)
- [Run test suite](#run-test-suite)
- [Release on PyPI](#release-on-pypi)
- [Changelog](#changelog)
  - [Version 1.4.0](#version-140)
  - [Version 1.3.0](#version-130)
  - [Version 1.2.0](#version-120)
  - [Version 1.1.0](#version-110)
  - [Version 1.0.0](#version-100)
- [Credits](#credits)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Configuration
Please see [config.yaml](config.yaml) for an example configuration

## Handlers
 - Uncomment the relevant handlers in [config.yaml](config.yaml)
 - Create an .env file. Possible use [.env.example](.env.example) as a starting point

# Install
```bash
pip install kubewatcher
```

# Run
Your default context from `~/.kube/config` will be used.

## Natively
By default, `kubewatcher` will look for a config file (config.yaml) in the current directory. Different locations, and names, can be specified using the `-f` argument.
```bash
kubewatcher
```

## Docker
```bash
docker-compose up
```

## Helm
Coming soon

# Development Setup
```bash
virtualenv venv
source venv/bin/activate
pip install --editable .
```

# Run test suite
```bash
python -m unittest -v
```

# Release on PyPI
```bash
python setup.py sdist bdist_wheel
python -m twine upload dist/*
```

# Changelog
## Version 1.5.0
 - Helm package
 - Default slack bot icon and username
 - "In cluster" API authentication
 - Command line arguments parsing via Click

## Version 1.4.0
 - Release on PyPI

## Version 1.3.0
 - Slack bot icon
 - Initial unit testing
 - Restructure code

## Version 1.2.0
 - Observe multiple resource, not just Pods

## Version 1.1.0
 - Path comparison using < and > operators
 - Support configuration environment variables

## Version 1.0.0
 - Templated messages
 - Path comparison using == and != operators
 - Slack and SMTP handlers

# Credits
Thanks to Freepik for making the icon freely available

https://www.flaticon.com/free-icon/businessman_1253770?term=binoculars&page=1&position=14
