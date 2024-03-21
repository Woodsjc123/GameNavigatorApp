from rest_framework import serializers
from .models import Game

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'title', 'genres', 'release_date', 'rating', 'platforms', 'total_hours_played']
        depth = 1
