FROM python:3.7
ENV PYTHONUNBUFFERED 1
ENV SETUPTOOLS_USE_DISTUTILS stdlib
RUN apt-get update && apt-get install -y nano && rm -rf /var/lib/apt/lists/*
RUN mkdir /code
WORKDIR /code
RUN pip install pipenv
ADD Pipfile /code/
ADD Pipfile.lock /code/
RUN pipenv install --system
ADD src/ /code/
ENTRYPOINT sh container_init.sh && sh -c "exec gunicorn backend.wsgi:application --access-logfile - --bind 0.0.0.0:8000 --workers 4"
