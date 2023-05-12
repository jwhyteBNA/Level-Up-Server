from django.db import models


class Event(models.Model):
    """Database model for tracking events"""

    description = models.CharField(max_length=155)
    date = models.DateField(auto_now=False, auto_now_add=False)
    time = models.TimeField()
    organizer = models.ForeignKey('Gamer', on_delete=models.CASCADE,
                                related_name= 'organized_events')
    attendees= models.ManyToManyField('Gamer', related_name='events_attended')
    game=models.ForeignKey('Game', on_delete=models.CASCADE, related_name= 'events')

    @property
    def joined(self):
        """Create joined column from validation logic"""
        return self.__joined

    @joined.setter
    def joined(self, value):
        self.__joined = value
