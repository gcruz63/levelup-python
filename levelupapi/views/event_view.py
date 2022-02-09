"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Gamer, Game
from django.core.exceptions import ValidationError


class EventView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type"""
        event = Event.objects.get(pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

        """Returns:
            Response -- JSON serialized game type
        """

    def list(self, request):
        """Handle GET requests to get all game types"""
        events = Event.objects.all()
        # query_params is a dictionary query_params from url
        event = request.query_params.get('game', None)
        if event is not None:
            events = events.filter(game_id=event)
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle post requests to events"""
        organizer = Gamer.objects.get(user=request.auth.user)
        try:
            serializer = EventCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(organizer=organizer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request):
        """Update Event"""
        gamer = Gamer.objects.get(user=request.auth.user)
        try:
            serializer = EventCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(gamer=gamer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        """Delete game"""
        event = Event.objects.get(pk=pk)
        event.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class EventCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'description', 'date',
                  'time']


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        # __all__ gets all fields from the model you are taking it from
        fields = '__all__'
