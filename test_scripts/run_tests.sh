#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd -P)"
REPO_PATH="$( dirname $DIR)"

cd $REPO_PATH

docker-compose build
docker-compose up -d database
docker-compose run --rm web python manage.py makemigrations
docker-compose run --rm web python manage.py migrate
docker-compose run --rm web python manage.py collectstatic --noinput
docker-compose run --rm web python manage.py test
