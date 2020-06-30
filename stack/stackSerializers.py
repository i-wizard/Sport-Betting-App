from rest_framework import serializers

from stack.models import Event, Match, Slip, Game, Team, RafflePlayer, RaffleWinners
from users.userSerializers import UserListSerializers


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class GamesSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    home_team_selected = serializers.BooleanField(default=False)
    away_team_selected = serializers.BooleanField(default=False)
    even_selected = serializers.BooleanField(default=False)
    over_two_five_selected = serializers.BooleanField(default=False)
    under_two_five_selected = serializers.BooleanField(default=False)

    class Meta:
        model = Match
        fields = '__all__'


class MatchSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)

    class Meta:
        model = Match
        fields = '__all__'


class UserGamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slip
        fields = '__all__'


class SlipGamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'
        extra_kwargs = {
            "username": {"error_messages": {"required": "Give yourself a username"}}
        }


class IssueResponseSerializer(serializers.Serializer):
    message = serializers.CharField(error_messages={'blank': "Please enter response message"})
    title = serializers.CharField(error_messages={'blank': "Please enter response title"})


class SlipSerializer(serializers.ModelSerializer):
    user = UserListSerializers(read_only=True)

    class Meta:
        model = Slip
        fields = '__all__'


class RafflePlayerSerializer(serializers.ModelSerializer):
    user = UserListSerializers(read_only=True)

    class Meta:
        model = RafflePlayer
        fields = '__all__'


class RaffleWinnersSerializer(serializers.ModelSerializer):
    user = RafflePlayerSerializer(read_only=True)

    class Meta:
        model = RaffleWinners
        fields = '__all__'
