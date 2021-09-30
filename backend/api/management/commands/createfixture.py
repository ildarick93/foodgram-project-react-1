import json
import os

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = ('Create fixtures from json file,'
            'createfixtures [filename] [app.model]')

    def add_arguments(self, parser):
        parser.add_argument('file_path', nargs='+', type=str)

    def handle(self, *args, **options):
        file_path = options['file_path'][0]
        model = options['file_path'][1]
        abspath = os.getcwd() + file_path
        filename = os.path.basename(abspath).split('.')[0]
        with open(abspath, "r") as read_file:
            data = json.load(read_file)
        len_data = len(data)
        fixture = [None] * len_data
        pk_counter = 0
        for ingredient in data:
            fixture[pk_counter] = {}
            fixture[pk_counter]['pk'] = pk_counter + 1
            fixture[pk_counter]['model'] = model
            fixture[pk_counter]['fields'] = ingredient
            pk_counter += 1
        with open(f'./fixtures/{filename}.json', 'w') as fixture_file:
            json.dump(fixture, fixture_file, indent=2, ensure_ascii=False)
        self.stdout.write(self.style.SUCCESS(
            f'Successfully saved at fixtures/{fixture_file}.json'))
