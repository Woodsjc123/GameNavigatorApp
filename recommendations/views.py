import os
from .models import Game, PlayedGame, UserProfile
from .serializers import GameSerializer, UserProfileSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.conf import settings
from django.shortcuts import get_object_or_404

from django.db.models import Q

from .recommendation_engine import load_data, get_recommendations
import pandas as pd



playtime_df = pd.read_csv('.\\recommendations\\csv\\final_merged_data.csv')
games_df = pd.read_csv('.\\recommendations\\csv\\clean.csv')
partition, community_pagerank_scores = load_data()


def clean_title(title):
    title = str(title).lower().strip()

    for char in [":", ";", "'", ".", ",", "-", "_", "(", ")", "&", "/"]:
        title = title.replace(char, "")
    return title



class SPAView(View):
    def get(self, request, *args, **kwargs):
        with open(os.path.join(settings.REACT_APP_DIR, 'build', 'index.html'), 'r') as file:
            return HttpResponse(file.read(), content_type='text/html')


class GameListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return JsonResponse(serializer.data, safe=False)
    
class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({"detail": "Success."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)


class UserRegistrationAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email') 

        if not username or not password:
            return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)


        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()

        login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        return Response({"success": "Successful registration"}, status=status.HTTP_201_CREATED)
    

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_profile = get_object_or_404(UserProfile, user=request.user)
        serializer = UserProfileSerializer(user_profile, context={'request': request})
        return Response(serializer.data)

        


class ProfilePicUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        user_profile = get_object_or_404(UserProfile, user=request.user)
        file_serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        

class AddGameView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, game_id):
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        game = get_object_or_404(Game, pk=game_id)
        user_profile.played_games.add(game)
        return Response({"success": f"Game '{game.title}' added to your played list."})
    


class RecommendGames(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user

        userprofile = get_object_or_404(UserProfile, user=user)

        played_games = PlayedGame.objects.filter(user_profile=userprofile)
        playtime = {played_game.game.title: played_game.playtime for played_game in played_games}


        recommendations = get_recommendations(
            playtime, community_pagerank_scores, partition, games_df, top_n=10
        )

        clean_recommendations = [clean_title(title) for title in recommendations]

        print(clean_recommendations)

        played_titles = [clean_title(game.game) for game in played_games]

        query = Q(title__in=clean_recommendations) & ~Q(title__in=played_titles)
        recommended_games = Game.objects.filter(query)

        serializer = GameSerializer(recommended_games, many=True)

        return Response(serializer.data)


class UpdateHours(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user

        userprofile = get_object_or_404(UserProfile, user=user)
        
        game_hours = request.data.get('hours', {})

        for game_id, hours in game_hours.items():
            try:
                hours = float(hours)
            except ValueError:
                return Response({"error": f"Invalid hours value for game ID {game_id}"}, status=status.HTTP_400_BAD_REQUEST)
            

            game = get_object_or_404(Game, pk=game_id)

            PlayedGame.objects.update_or_create(
                user_profile=userprofile, 
                game=game, 
                defaults={'playtime': hours}
            )

        return Response({"status": "success"}, status=status.HTTP_200_OK)
    

def logout_view(request):
    logout(request)
    