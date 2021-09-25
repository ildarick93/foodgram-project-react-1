from django.core.management.base import BaseCommand, CommandError
import json
import os
class Command(BaseCommand):
    help = ('Create fixtures from json file,'
            'createfixtures [filename] [app.model]')

    def handle(self, *args, **options):
        os.system('python3 manage.py loaddata fixtures/users.json')
        os.system('python3 manage.py loaddata fixtures/ingredients.json')
        os.system('python3 manage.py loaddata fixtures/tags.json')