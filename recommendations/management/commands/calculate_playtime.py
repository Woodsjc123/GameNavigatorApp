from django.core.management.base import BaseCommand
from recommendations.models import Game, UserGameInteraction, models

class Command(BaseCommand):
    help = 'Calculates and updates total hours played for each game'

    def handle(self, *args, **options):
        for game in Game.objects.all():
            total_hours = UserGameInteraction.objects.filter(game=game).aggregate(total_hours=models.Sum('hours_played'))['total_hours']
            game.total_hours_played = total_hours or 0
            game.save()
            self.stdout.write(self.style.SUCCESS(f'Updated {game.title} with total hours played.'))
