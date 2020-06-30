from random import randint
from django.db.models import F

from stack.models import Game, Slip


class StockHelper:
    _MATCH_OUTCOME = ''
    _RESULT_BOOL = [True, False]

    def play_smart_users(self, match):
        both_team_score = int(match.home_team_score) + int(match.away_team_score)

        if int(match.home_team_score) == int(match.away_team_score):
            self._MATCH_OUTCOME = 'draw'
        elif int(match.away_team_score) > int(match.home_team_score):
            self._MATCH_OUTCOME = 'away'
        elif int(match.home_team_score) > int(match.away_team_score):
            self._MATCH_OUTCOME = 'home'

        special_games = Game.objects.filter(is_smart=True, match=match.pk)

        if special_games.count():
            for special_game in special_games:
                if special_game.points < 4:
                    self._check_smart_user(special_game, match.pk, both_team_score)

    def _check_smart_user(self, game, match_id, both_team_score):
        both_team_score = int(both_team_score)
        normal_games = Game.objects.filter(is_smart=False, match=match_id).order_by('-points')
        game_score = game.points
        should_increase = False
        lose_main_selection = False
        lose_point_selection = False
        check_slip = False

        normal_slips = Slip.objects.filter(today=game.slip.today.pk, is_special=False)
        smart_slip = Slip.objects.get(pk=game.slip.pk)

        for slip in normal_slips:
            if slip.score > smart_slip.score:
                check_slip = True
                break

        if check_slip:
            for normal_game in normal_games:
                if int(normal_game.points) > int(game_score):
                    should_increase = True
                    if int(normal_game.points) == 3 and not game.win:
                        lose_main_selection = True
                    elif int(normal_game.points) > 3 and not game.win:
                        lose_point_selection = True
                        lose_main_selection = True
                    else:
                        lose_point_selection = True
                    break

            if should_increase:
                game_record = Game.objects.get(pk=game.pk)
                game_win = game_record.win
                score = 0

                if lose_point_selection:
                    if game.under_two_five:
                        if both_team_score >= 3:
                            game_record.under_two_five = False
                            game_record.over_two_five = True
                            score += 1
                    elif game.over_two_five:
                        if both_team_score < 3:
                            game_record.under_two_five = True
                            game_record.over_two_five = False
                            score += 1

                if lose_main_selection:
                    if self._MATCH_OUTCOME == 'draw':
                        if not game_record.both_even:
                            game_record.both_even = True
                            selection = self._RESULT_BOOL[randint(0, 1)]
                            game_record.home_team_win = selection
                            game_record.away_team_win = not selection
                            score += 3
                            game_win = True
                    elif self._MATCH_OUTCOME == 'home':
                        if not game_record.home_team_win:
                            selection = self._RESULT_BOOL[randint(0, 1)]
                            game_record.both_even = not selection
                            game_record.home_team_win = True
                            game_record.away_team_win = selection
                            score += 3
                            game_win = True
                    elif self._MATCH_OUTCOME == 'away':
                        if not game_record.away_team_win:
                            selection = self._RESULT_BOOL[randint(0, 1)]
                            game_record.both_even = not selection
                            game_record.home_team_win = selection
                            game_record.away_team_win = True
                            score += 3
                            game_win = True

                game_record.win = game_win
                game_record.points = F('points') + score
                game_record.save()

                # game = Game.objects.get(pk=game_record.pk)

                game_slip = Slip.objects.get(pk=game_record.slip.pk)
                game_slip.score = F('score') + score
                game_slip.save(update_fields=('score',))

                # if game.points < 4:
                #     self._check_smart_user(game, match_id, both_team_score)
