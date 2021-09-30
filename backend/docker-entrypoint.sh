#!/bin/bash

echo "making migrations"

while ! python manage.py migrate; do
  echo "creating tables in data base"
done

while ! python manage.py loadall; do
  echo "Collect static"
done

while ! python manage.py collectstatic <<<yes; do
  echo "Collect static"
done

exec "$@"