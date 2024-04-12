from rest_framework import serializers
from .models import Game, UserProfile

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    played_games = GameSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'