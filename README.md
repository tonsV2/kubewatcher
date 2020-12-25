# Kube Watcher
Simple and highly configurable Kubernetes monitor

The idea is that you can define a filter and if there's a match it will be handled by the handlers you define.

# Configuration
Please see [config.yaml](config.yaml) for an example configuration

## Handlers
 - Uncomment the relevant handlers in [config.yaml](config.yaml)
 - Create an .env file. Possible use [.env.example](.env.example) as a starting point

# Launch
Your default context from `~/.kube/config` will be used.

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

# Changelog
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
