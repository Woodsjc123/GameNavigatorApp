import requests
from django.core.management.base import BaseCommand
from recommendations.models import Genre
import os

# This command queries the RAWG API for all game genres and adds them to the database
class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        key = os.getenv('RAWG_API_KEY')

        url = f'https://api.rawg.io/api/genres?key={key}'

        response = requests.get(url)
        genres_data = response.json()

        for genre in genres_data['results']:
            genre_name = genre['name']

            if not Genre.objects.filter(name=genre_name).exists():
                Genre.objects.create(name=genre_name)
                self.stdout.write(self.style.SUCCESS(f'Added new genre: {genre_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Genre already exists: {genre_name}'))
