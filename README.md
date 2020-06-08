# SNAP-BackEnd

Georgia SNANPWorks Project Back end code

## Starting dev environment

Use this command to start db

```
docker-compose -f docker-compose/docker-compose.dev.yml up -d
```

## Per-object permisssions

https://www.youtube.com/watch?v=90T5D4KUjWI

Use Django Guardian? https://github.com/django-guardian/django-guardian

or

Django Rules

## Logging

Application logging should be handled with `django.app` or `django.app.[XYZ]` loggers:

```
import logging
logging.getLogger('django.app').error('app error')
logging.getLogger('django.app[XYZ]').error('app error')
```

Set LOGLEVEL environment variable to control app-level logger verbosity.

## Testing API

Goto `http://localhost:8000/swagger/`, Authorize by entering `Token [ACCESS_TOKEN]` in the authorize box.

To obtain new access token use the command: `./manage.py drf_create_token [USERNAME]`

## Jupyter notebook

Use `./manage.py shell_plus --notebook` to start a Jupyter notebook.

In order to connectYour script must start with:

```
import os
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
```

then you can work with models like so:

```
list(Client.objects.all())
```

# Deployment

Currently new version can be deployed via `pipenv run deploy`

## Production server dependencies
