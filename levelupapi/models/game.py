from django.db import models

class Game(models.Model):
    """Database model for tracking games"""

    title = models.CharField(max_length=155)
    maker = models.CharField(max_length=155)
    number_of_players = models.IntegerField(default=1)
    skill_level = models.CharField(max_length=50)
    game_type= models.ForeignKey('GameType', on_delete=models.CASCADE, related_name='games')
    