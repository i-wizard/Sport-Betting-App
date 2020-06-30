from django.urls import path
from .views import (EventsApiView, CreationDataAPi, CreateGameApi, GamesView, PlayTodayGames, TodayMatches,
                    UserGamesView, SlipGamesView, GameMatches, BetSlips, WinnersChart, EditMatches, RaffleWinnersView, RafflePlayers)

urlpatterns = [
    path('events', EventsApiView.as_view(), name='events'),
    path('games/creation/data', CreationDataAPi.as_view(), name='events_only'),
    path('create-game', CreateGameApi.as_view(), name='create_game'),
    path('games/<int:date>', GamesView.as_view()),
    path('play-game', PlayTodayGames.as_view()),
    path('admin/today-matches', TodayMatches.as_view()),
    path('user-games', UserGamesView.as_view()),
    path('slip-games/<str:token>', SlipGamesView.as_view()),
    path('game/<int:pk>/matches', GameMatches.as_view()),
    path('edit-game/<int:pk>', EditMatches.as_view()),
    path('slips', BetSlips.as_view()),
    path('winners', WinnersChart.as_view()),
    path('raffle-winners', RaffleWinnersView.as_view()),
    path('get-raffle-players', RafflePlayers.as_view()),
    path('get-raffle-winners', RaffleWinnersView.as_view()),
]
