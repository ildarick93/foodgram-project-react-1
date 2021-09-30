import os

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = ('Create fixtures from json file,'
            'createfixtures [filename] [app.model]')

    def handle(self, *args, **options):
        os.system('python3 manage.py loaddata fixtures/users.json')
        os.system('python3 manage.py loaddata fixtures/ingredients.json')
        os.system('python3 manage.py loaddata fixtures/tags.json')
        os.system('python3 manage.py loaddata fixtures/recipe.json')
        os.system('python3 manage.py loaddata fixtures/ingredientamount.json')
        os.system('python3 manage.py loaddata fixtures/favorite.json')
        os.system('python3 manage.py loaddata fixtures/follows.json')
