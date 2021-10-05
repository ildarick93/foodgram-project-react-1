#!/bin/bash

for file_name in "users" "ingredients" "tags" "recipe" "ingredientamount" "favorite" "follows"; do
python manage.py loaddata fixtures/$file_name.json
done