#openeats Project

**openeats** is a continuation from [qgriffith/OpenEats](https://github.com/qgriffith/OpenEats).

## Changes
* Updated to Django 1.10
* Docker-compose to deploy project

## Dev deploy
Install and create basic data:
```
docker-compose up -d database && \
docker-compose run --rm web python manage.py makemigrations && \
docker-compose run --rm web python manage.py migrate && \
docker-compose run --rm web python manage.py collectstatic --noinput && \
docker-compose run --rm web python manage.py createsuperuser
```

Deploy environment:
```
docker-compose up -d
```


## Prod deploy
Configure editing `docker-compose.prod.yml` environment variables.

Install and create basic data:
```
docker-compose -f docker-compose.prod.yml up -d database && \
docker-compose -f docker-compose.prod.yml run --rm web python manage.py makemigrations && \
docker-compose -f docker-compose.prod.yml run --rm web python manage.py migrate && \
docker-compose -f docker-compose.prod.yml run --rm web python manage.py collectstatic --noinput && \
docker-compose -f docker-compose.prod.yml run --rm web python manage.py createsuperuser
```

Deploy environment:
```
docker-compose -f docker-compose.prod.yml up -d
```
