from django.core.management.base import BaseCommand
import pandas as pd
from recommendations.models import Game, UserProfile, UserGameInteraction

class Command(BaseCommand):
    help = 'Load data from CSV into the database'

    def handle(self, *args, **options):
        df = pd.read_csv('C:\\Users\\John\\Desktop\\Notebooks\\clean.csv')
        for _, row in df.iterrows():
            user_profile, _ = UserProfile.objects.get_or_create(user_id=row['userID'])
            game, _ = Game.objects.get_or_create(title=row['title'])
            UserGameInteraction.objects.create(
                user_profile=user_profile,
                game=game,
                hours_played=row['hours']
            )
        self.stdout.write(self.style.SUCCESS('Data loaded successfully'))
