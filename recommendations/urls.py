from django.urls import path
from .views import SPAView, GameListAPIView
from .views import LoginAPIView
from .views import UserRegistrationAPIView
from .views import UserProfileView
from .views import ProfilePicUpdateView
from .views import logout_view

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from django.contrib.auth import views as auth_views
from .views import AddGameView, RecommendGames, UpdateHours


urlpatterns = [
    path('api/games/', GameListAPIView.as_view(), name='game-list'),
    path('', SPAView.as_view()),
    path('api/login/', LoginAPIView.as_view(), name='api_login'),
    path('api/register/', UserRegistrationAPIView.as_view(), name='api_register'),
    path('api/profile/', UserProfileView.as_view(), name='user-profile'),
    path('api/profilepic/', ProfilePicUpdateView.as_view(), name='profile-pic'),
    path('api/logout/', logout_view, name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('api/add_game/<int:game_id>/', AddGameView.as_view(), name='add_game'),
    path('api/recommend/', RecommendGames.as_view(), name='recommend'),
    path('api/updatehours/', UpdateHours.as_view(), name='recommend')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
