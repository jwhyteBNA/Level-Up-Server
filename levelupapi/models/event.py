from django.db import models


class Event(models.Model):
    """Database model for tracking events"""

    description = models.CharField(max_length=155)
    date = models.DateField()
    time = models.TimeField()
    organizer = models.ForeignKey('Gamer', on_delete=models.CASCADE, related_name= 'events')
    attendees= models.ManyToManyField('Gamer')
    game=models.ForeignKey('Game', on_delete=models.CASCADE, related_name= 'events')

    @property
    def joined(self):
        """Create joined column from validation logic"""
        return self.__joined

    @joined.setter
    def joined(self, value):
        self.__joined = value
