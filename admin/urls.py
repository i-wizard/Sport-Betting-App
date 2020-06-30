from django.urls import path
from django.utils.decorators import decorator_from_middleware

from trivia.views import AdminTrivia, cancel_question, AdminTriviaResult
from .middleware import AdminCheckMiddleware
from .views import (dashboard, TeamsView, delete_team_view, EventsView, delete_event_view, games_view,
                    games_creation_view, game_matches_view, redirect_after_match_update, ImagesView, add_slider_image,
                    remove_slider_image, UsersView, delete_slider_image, game_edit_view, GamesSetting, user_games_view,
                    user_bet_slip, change_user_status, support_view, SupportResponse, SendMessage, game_delete_view,
                    CreditUserAccount, QualifiedPlayers)

admin_auth_decorator = decorator_from_middleware(AdminCheckMiddleware)
app_name = 'myadmin'

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('teams', admin_auth_decorator(TeamsView.as_view()), name='teams'),
    path('teams/delete/<int:pk>', admin_auth_decorator(delete_team_view), name='delete_team'),
    path('events', admin_auth_decorator(EventsView.as_view()), name='events'),
    path('events/delete/<int:pk>', admin_auth_decorator(delete_event_view), name='delete_event'),
    path('games', admin_auth_decorator(games_view), name='games'),
    path('games/setting', admin_auth_decorator(GamesSetting.as_view()), name='games_setting'),
    path('trivia', admin_auth_decorator(AdminTrivia.as_view()), name='trivia'),
    path('trivia/result/<int:pk>', admin_auth_decorator(AdminTriviaResult.as_view()), name='trivia_result'),
    path('trivia/cancel/<int:pk>', admin_auth_decorator(cancel_question), name='trivia_cancel'),
    path('games/create', admin_auth_decorator(games_creation_view), name='games_create'),
    path('games/matches/<int:pk>', admin_auth_decorator(game_matches_view), name='game_matches'),
    path('games/edit/<int:pk>', admin_auth_decorator(game_edit_view), name='edit_game'),
    path('games/delete/<int:pk>', admin_auth_decorator(game_delete_view), name='delete_game'),
    path('games/matches/update/success/<int:pk>', admin_auth_decorator(redirect_after_match_update)),
    path('images', admin_auth_decorator(ImagesView.as_view()), name='images'),
    path('images/add/<int:pk>', admin_auth_decorator(add_slider_image), name='add_slider'),
    path('images/remove/<int:pk>', admin_auth_decorator(remove_slider_image), name='remove_slider'),
    path('images/delete/<int:pk>', admin_auth_decorator(delete_slider_image), name='delete_image'),
    path('users', admin_auth_decorator(UsersView.as_view()), name='users'),
    path('user/<int:pk>/games', admin_auth_decorator(user_games_view), name='user_games'),
    path('slip/<int:pk>', admin_auth_decorator(user_bet_slip), name='bet_slip'),
    path('status/change/<int:pk>', admin_auth_decorator(change_user_status), name='status_change'),
    path('support', admin_auth_decorator(support_view), name='support'),
    path('support/respond', admin_auth_decorator(SupportResponse.as_view()), name='support_response'),
    path('messages', admin_auth_decorator(SendMessage.as_view()), name='message'),
    path('users/credit-account', admin_auth_decorator(CreditUserAccount.as_view()), name='credit_user_account'),
    path('qualified-players', admin_auth_decorator(QualifiedPlayers.as_view()), name='qualified_players'),
]
