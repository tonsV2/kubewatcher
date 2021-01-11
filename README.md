# Kube Watcher
[![Python packaging](https://github.com/tonsV2/kubewatcher/workflows/Python%20packaging/badge.svg)](https://github.com/tonsV2/kubewatcher/actions?query=workflow%3A%22Python+packaging%22)
[![Docker image creation](https://github.com/tonsV2/kubewatcher/workflows/Docker%20image%20creation/badge.svg)](https://github.com/tonsV2/kubewatcher/actions?query=workflow%3A%22Docker+image+creation%22)

Simple and highly configurable Kubernetes monitor

The idea is that you define a filter and if there's a match you'll get a message via Slack, Telegram or mail.

Out of the box you'll get notified about nodes with disk, memory or PID pressure. Deployments configured with nonexistent Docker images, failing Jobs and any events of type warning.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
- [Kube Watcher](#kube-watcher)

- [Install](#install)
- [Configuration](#configuration)
  - [Handlers](#handlers)
- [Run](#run)
  - [Natively](#natively)
  - [Docker](#docker)
  - [Helm](#helm)
    - [Install](#install-1)
    - [Package](#package)
    - [Push](#push)
- [Development Setup](#development-setup)
- [Run test suite](#run-test-suite)
- [Release on PyPI](#release-on-pypi)
- [Changelog](#changelog)
  - [Version 1.7.1](#version-171)
  - [Version 1.7.0](#version-170)
  - [Version 1.6.0](#version-160)
  - [Version 1.5.0](#version-150)
  - [Version 1.4.0](#version-140)
  - [Version 1.3.0](#version-130)
  - [Version 1.2.0](#version-120)
  - [Version 1.1.0](#version-110)
  - [Version 1.0.0](#version-100)
- [Credits](#credits)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Install
```bash
pip install kubewatcher
```

# Configuration
Please see [config.yaml](config.yaml) for an example configuration

## Handlers
Currently Slack, Telegram and mail handlers are supported. Let me know if your favorite protocol is missing, and I'll see what I can do.

 - Uncomment the relevant handlers in [config.yaml](config.yaml)
 - Create an .env file. Possible use [.env.example](.env.example) as a starting point

# Run
By default `~/.kube/config` and your current context will be used, but config file location and context can be specified using command line arguments. Please see `kubewatcher --help` for details.

## Natively
By default, `kubewatcher` will look for a config file (config.yaml) in the current directory. Different locations, and names, can be specified using the `-f` argument.
```bash
kubewatcher watch
```

## Docker
```bash
docker-compose up
```

## Helm
### Install
Please see [values.yaml](helm/values.yaml) for an example configuration

```bash
helm upgrade --install kubewatcher --namespace kubewatcher tons/kubewatcher --values values.yaml
```

### Package
```bash
helm package --sign --key 'helm' --keyring ~/.gnupg/pubring.gpg helm/
```

### Push
```bash
curl --user "$CHARTMUSEUM_AUTH_USER:$CHARTMUSEUM_AUTH_PASS" \
            -F "chart=@kubewatcher-1.2.0.tgz" \
            -F "prov=@kubewatcher-1.2.0.tgz.prov" \
            https://helm-charts.fitfit.dk/api/charts
```

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
## Version 1.7.1
 - Make filters optional so configuration can be separated into several files
 - Make tests optional since they might not be included when the application is deployed on Kubernetes or similar

## Version 1.7.0
 - Complete rewrite of the main application structure. The original functional approach is scrapped in favor of a more OO architecture
 - Add testing of filters from the command line
 - Add filters for various node related issues
 - Use yamlpath rather than custom implementation

## Version 1.6.0
 - Telegram handler
 - Initial CI
 - Log rather than print
 - Rewrite main application loop, now loops forever

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
