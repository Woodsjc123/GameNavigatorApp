from django.urls import path
from .views import SPAView, GameListAPIView
from .views import LoginAPIView
from .views import UserRegistrationAPIView

urlpatterns = [
    path('api/games/', GameListAPIView.as_view(), name='game-list'),
    path('', SPAView.as_view()),
    path('api/login/', LoginAPIView.as_view(), name='api_login'),
    path('api/register/', UserRegistrationAPIView.as_view(), name='api_register'),
]
