#!/bin/bash
while ! python manage.py migrate; do
echo "making migrations"
done

for file_name in "users" "ingredients" "tags" "recipe" "ingredientamount" "favorite" "follows"; do
python manage.py loaddata fixtures/$file_name.json
done

while ! python manage.py collectstatic <<<yes; do
  echo "Collect static"
done

while ! gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000; do
  echo "application started"
done

exec "$@"