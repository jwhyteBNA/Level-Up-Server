"""View module for handling requests about game types"""
# from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Gamer


class GamerView(ViewSet):
    """Level up gamer view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single gamer

        Returns:
            Response -- JSON serialized gamer
        """
        gamer = Gamer.objects.get(pk=pk)
        serializer = GamerSerializer(gamer)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def list(self, request):
        """Handle GET requests to get all gamers

        Returns:
            Response -- JSON serialized list of gamers
        """
        gamers = Gamer.objects.all()
        serializer = GamerSerializer(gamers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GamerSerializer(serializers.ModelSerializer):
    """JSON serializer for Gamers"""
    class Meta:
        model = Gamer
        fields = ('id', 'user', 'bio' )
        depth = 1
