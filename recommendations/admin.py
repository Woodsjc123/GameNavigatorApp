from django.contrib import admin
from .models import UserProfile, Platform, Genre, Game, PlayedGame

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Platform)
admin.site.register(Genre)
admin.site.register(Game)
admin.site.register(PlayedGame)