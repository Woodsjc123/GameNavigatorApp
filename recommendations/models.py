from django.db import models
from django.contrib.auth.models import User 


class Platform(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class Game(models.Model):
    title = models.CharField(max_length=200)
    genres = models.ManyToManyField(Genre, related_name='games')
    release_date = models.DateField(null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    platforms = models.ManyToManyField(Platform, related_name='games')
    preview_image = models.URLField(max_length=2048, null=True, blank=True)
    description = models.TextField(null=True)

    def __str__(self):
        return self.title
    


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_genres = models.ManyToManyField('Genre')
    preferred_platforms = models.ManyToManyField('Platform')
    profile_pic = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    played_games = models.ManyToManyField(Game, related_name='players')
    
    
class PlayedGame(models.Model):
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    playtime = models.PositiveIntegerField(help_text="Playtime in hours")

    class Meta:
        unique_together = ('user_profile', 'game')


class UserGameInteraction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    hours_played = models.FloatField(default=0)