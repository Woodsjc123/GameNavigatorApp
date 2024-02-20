from django.db import models
from django.contrib.auth.models import User 

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_genres = models.ManyToManyField('Genre')
    preferred_platforms = models.ManyToManyField('Platform')

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
    release_date = models.DateField()
    rating = models.FloatField()
    platforms = models.ManyToManyField(Platform, related_name='games')
    total_hours_played = models.FloatField(default=0)

    def __str__(self):
        return self.title

    
class UserGameRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    rating = models.IntegerField()

    class Meta:
        unique_together = ('user', 'game')

    def __str__(self):
        return f"{self.user.username} - {self.game.title} - Rating: {self.rating}"


class UserGameInteraction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    hours_played = models.FloatField(default=0)