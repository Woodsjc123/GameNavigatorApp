import csv
import time
import requests
from django.core.management.base import BaseCommand
from recommendations.models import Game, Platform, Genre
import os


# This command queries the RAWG API for all the game titles in the csv file, and populates the database with the results
class Command(BaseCommand):

    def handle(self, *args, **options):
        key = os.getenv('RAWG_API_KEY')
        csv_path = options['csv_file']
        games_count = options['number']
        start = options['start']    


        with open(csv_path, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            
            for i, row in enumerate(csv_reader):
                if i < start:
                    continue
                if i >= start + games_count:
                    break
                
                game_title = row['Title']                

                response = requests.get(f'https://api.rawg.io/api/games?key={key}&search={game_title}')
                time.sleep(5)   # Wait 5 seconds between each request
                
                if response.status_code == 200:
                    data = response.json()
                    results = data.get('results')
                    if results:
                        game_data = results[0] 
                

                        game, created = Game.objects.update_or_create(
                            title=game_title,
                            defaults={
                                'description': game_data.get('description', ''),
                                'release_date': game_data.get('released', None),
                                'preview_image': game_data.get('background_image', ''),
                                'rating': game_data.get('rating', 0),
                            }
                        )
                        

                        for platform in game_data.get('platforms', []):
                            platform_name = platform.get('platform', {}).get('name', '')
                            if platform_name:
                                plat, _ = Platform.objects.get_or_create(name=platform_name)
                                game.platforms.add(plat)
                        

                        for genre in game_data.get('genres', []):
                            genre_name = genre.get('name', '')
                            if genre_name:
                                gen, _ = Genre.objects.get_or_create(name=genre_name)
                                game.genres.add(gen)
                        
                        action = 'Added' if created else 'Updated'
                        self.stdout.write(self.style.SUCCESS(f'{action} {game_title}'))
                else:
                    self.stdout.write(self.style.ERROR(f'Failed to import data for {game_title}'))
