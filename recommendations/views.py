from django.shortcuts import render
from .models import UserGameInteraction, Game
from django.contrib.auth.decorators import login_required

@login_required
def game_recommendations(request):
    user = request.user
    recommendations = Game.objects.exclude(usergameinteraction__user=user).order_by('-total_hours_played')[:10] 
