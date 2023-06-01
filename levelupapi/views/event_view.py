"""View module for handling requests about Events"""
# from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers, status
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.db.models import Count
from levelupapi.models import Event, Game, Gamer

class EventView(ViewSet):
    """Level up events view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single event

        Returns:
            Response -- JSON serialized event
        """
        try:
            event = Event.objects.annotate(attendees_count=Count('attendees')).get(pk=pk)
            serializer = EventSerializer(event)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Event.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all events

        Returns:
            Response -- JSON serialized list of events
        """
        events = []
        gamer = Gamer.objects.get(user=request.auth.user)
        game_id = request.query_params.get('game')
        if game_id:
            events = Event.objects.filter(game=game_id)
        else:
            # events = Event.objects.all()
            events = Event.objects.annotate(
                attendees_count=Count('attendees'),
                joined=Count('attendees',filter=Q(attendees=gamer)
                ))

        # Event.objects.filter(
        #     Q(organizer=gamer) &
        #     Q(game__gamer=gamer)
        # )
        # # Set the `joined` property on every event
        # for event in events:
        #     # Check to see if the gamer is in the attendees list on the event
        #     event.joined = gamer in event.attendees.all()

        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized event instance
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        game = Game.objects.get(pk=request.data["game"])

        serializer = CreateEventSerializer(data=request.data)
        if serializer.is_valid():
            event = serializer.save()
            event_serializer = EventSerializer(event)
            serializer.save(organizer=gamer, game=game)
            return Response(event_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # serializer = CreateEventSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save(organizer=gamer, game=game)
        # return Response(serializer.data, status=status.HTTP_201_CREATED)

        # event = Event.objects.create(
        #     description=request.data["description"],
        #     date=request.data["date"],
        #     time=request.data["time"],
        #     game=game,
        #     organizer=gamer
        # )

        # serializer = EventSerializer(event)
        # return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """

        event = Event.objects.get(pk=pk)
        event.description = request.data["description"]
        event.date = request.data["date"]
        event.time = request.data["time"]

        game = Game.objects.get(pk=request.data["game"])
        event.game = game

        gamer = Gamer.objects.get(pk=request.data["organizer"])
        event.organizer = gamer
        event.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """To Delete an event"""
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=True)
    def signup(self, request, pk):
        """Post request for a user to sign up for an event"""

        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendees.add(gamer)
        return Response({'message': 'Gamer added'}, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True)
    def leave(self, request, pk):
        """Delete request for a user to leave an event"""

        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendees.remove(gamer)
        return Response({'message': 'Successfully left event'}, status=status.HTTP_204_NO_CONTENT)


class CreateEventSerializer(serializers.ModelSerializer):
    """JSON serializer for creating new Event"""
    class Meta:
        model = Event
        fields = ('id', 'description', 'date', 'time', 'game', 'organizer',)

class EventSerializer(serializers.ModelSerializer):
    attendees_count = serializers.IntegerField(default=None)
    """JSON serializer for Events"""
    class Meta:
        model = Event
        fields = ('id', 'description', 'date', 'time', 'game', 'attendees', 'organizer', 'joined', 'attendees_count')
        depth = 2
