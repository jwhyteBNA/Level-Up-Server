"""View module for handling requests about game types"""
# from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.core.exceptions import ValidationError
from django.db.models import Q, Count
from levelupapi.models import Game, Gamer, GameType


class GameView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game
        """

        try:
            gamer = Gamer.objects.get(user=request.auth.user)
            game = Game.objects.annotate(
                event_count=Count('events'), user_event_count=Count('events', filter=Q(events__organizer=gamer))
            ).get(pk=pk)
            serializer = GameSerializer(game)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all games

        Returns:
            Response -- JSON serialized list of games
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        # games = Game.objects.all()
        games = Game.objects.annotate(
            event_count=Count('events'),            user_event_count=Count('events', filter=Q(events__organizer=gamer)
        ))

        game_type = request.query_params.get('type', None)
        if game_type is not None:
            games = games.filter(game_type_id=game_type)

        search = request.query_params.get('search', None)
        if search is not None:
            Game.object.filter(
                Q(title__startswith=search) |
                Q(maker__startswith=search)
            )

        serializer = GameSerializer(games, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """
        serializer = CreateGameSerializer(data=request.data)
        if serializer.is_valid():
            game=serializer.save()
            game_serializer=GameSerializer(game)
            return Response(game_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Old Create Method without validation
        # gamer = Gamer.objects.get(user=request.auth.user)
        # game_type = GameType.objects.get(pk=request.data["game_type"])

        # game = Game.objects.create(
        #     title=request.data["title"],
        #     maker=request.data["maker"],
        #     number_of_players=request.data["number_of_players"],
        #     skill_level=request.data["skill_level"],
        #     game_type=game_type
        # )
        # serializer = GameSerializer(game)
        # return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """

        game = Game.objects.get(pk=pk)
        game.title = request.data["title"]
        game.maker = request.data["maker"]
        game.number_of_players = request.data["number_of_players"]
        game.skill_level = request.data["skill_level"]

        game_type = GameType.objects.get(pk=request.data["game_type"])
        game.game_type = game_type

        creator = Gamer.objects.get(pk=request.data["creator"])
        game.creator = creator
        game.save()

        serializer = GameSerializer(game)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """To Delete a game"""
        game = Game.objects.get(pk=pk)
        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class CreateGameSerializer(serializers.ModelSerializer):
    """JSON serializer for creating new Game"""
    class Meta:
        model = Game
        fields = ['id', 'title', 'maker',
                  'number_of_players', 'skill_level', 'game_type', 'creator']


class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for Games"""
    event_count = serializers.IntegerField(default=None)
    user_event_count = serializers.IntegerField(default=None)

    class Meta:
        model = Game
        fields = ('id', 'title', 'maker', 'number_of_players', 'skill_level',
                  'game_type', 'creator', 'event_count', 'user_event_count')
