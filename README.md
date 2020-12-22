# Kube Watcher
Simple and highly configurable Kubernetes monitor

The idea is that you can define a filter by defining a path, and an value, in the YAML of resource and if there's a match it will be handled by the handlers you define.

Currently, only kinds of type Pod is supported but in the near future I plan on adding support for other resources as well (particularly Event).

# Configuration
Please see [config.yaml](config.yaml) for an example configuration

# Launch

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
