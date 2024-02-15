from django.core.management.base import BaseCommand
import requests
from recommendations.models import Game, Genre, Platform

class Command(BaseCommand):
    help = 'Imports the first 100 games from the RAWG API into the database'

    def handle(self, *args, **options):
        games_fetched = 0
        page = 1
        total_games_to_fetch = 100
        while games_fetched < total_games_to_fetch:
            api_url = 'https://api.rawg.io/api/games'
            params = {
                'key': '4915b9306c824a47a1b6765e400fb02c',
                'page': page,
                'page_size': 20,
            }

            response = requests.get(api_url, params=params)
            if response.status_code == 200:
                games_data = response.json()['results']
                for game_data in games_data:
                    if games_fetched >= total_games_to_fetch:
                        break 

                    game, created = Game.objects.get_or_create(
                        id=game_data['id'],
                        defaults={
                            'title': game_data['name'],
                            'release_date': game_data['released'],
                            'rating': game_data.get('rating', 0),
                        }
                    )

                    if created:
                        for genre_data in game_data['genres']:
                            genre, _ = Genre.objects.get_or_create(id=genre_data['id'], defaults={'name': genre_data['name']})
                            game.genres.add(genre)

                        for platform_data in game_data['platforms']:
                            platform, _ = Platform.objects.get_or_create(id=platform_data['platform']['id'], defaults={'name': platform_data['platform']['name']})
                            game.platforms.add(platform)

                    games_fetched += 1

                page += 1
                self.stdout.write(self.style.SUCCESS(f'Fetched {games_fetched} games so far...'))
            else:
                self.stdout.write(self.style.ERROR('Failed to fetch data from RAWG API.'))
                break 

        self.stdout.write(self.style.SUCCESS('Finished importing games.'))
