from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import View
from rest_framework.views import APIView
import os
from .models import Game, UserGameInteraction, UserProfile
from .serializers import GameSerializer, UserProfileSerializer
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.models import User
from django.contrib.auth import logout

from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated

from .recommendation_engine import get_playtime, load_data, get_recommendations
import pandas as pd



games_df = pd.read_csv('..\\recommendations\\csv\\final_merged_data.csv')
playtime_df = pd.read_csv('..\\recommendations\\csv\\clean.csv')
partition, community_pagerank_scores = load_data()



class SPAView(View):
    def get(self, request, *args, **kwargs):
        with open(os.path.join(settings.REACT_APP_DIR, 'build', 'index.html'), 'r') as file:
            return HttpResponse(file.read(), content_type='text/html')


class GameListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)
    
    
class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({"detail": "Successul authentication"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Incorrect parameters"}, status=status.HTTP_401_UNAUTHORIZED)


class UserRegistrationAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email') 

        if not username or not password:
            return Response({"error": "Username and password needed"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)


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

        user_playtime = get_playtime(user.id, playtime_df)


        recommendations = get_recommendations(
            user_playtime, community_pagerank_scores, partition, games_df, top_n=5
        )

        recommended_games = Game.objects.filter(title__in=recommendations)
        serializer = GameSerializer(recommended_games, many=True)

        return Response(serializer.data)


class UpdateHours(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        game_hours = request.data.get('hours', {})

        for game_id, hours in game_hours.items():
            try:
                hours = float(hours)
            except ValueError:
                return Response({"error": f"Invalid hours value for game ID {game_id}"}, status=status.HTTP_400_BAD_REQUEST)
            

            game = get_object_or_404(Game, pk=game_id)

            UserGameInteraction.objects.update_or_create(
                user=user, 
                game=game, 
                defaults={'hours_played': hours}
            )

        return Response({"status": "success"}, status=status.HTTP_200_OK)
    

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login/')