class Game:
    SERVER: int = 1
    RETURNER: int = 2

    POINT_MAP: dict = {
        -1: '',
        0: '0',
        1: '15',
        2: '30',
        3: '40',
        4: 'AD'
    }

    def __init__(self):
        self._server_score: int = 0
        self._returner_score: int = 0
        self._score_difference: int = 0

    @property
    def server_score(self) -> int:
        return self._server_score

    @property
    def returner_score(self) -> int:
        return self._returner_score

    @property
    def score_difference(self):
        return self._score_difference

    def _add_server_point(self) -> None:
        if self._is_advantage(self.RETURNER):
            self._returner_score -= 1
        else:
            self._server_score += 1
        self._score_difference += 1

    def _add_returner_point(self) -> None:
        if self._is_advantage(self.SERVER):
            self._server_score -= 1
        else:
            self._returner_score += 1
        self._score_difference -= 1

    def _is_advantage(self, who: int) -> bool:
        if who == self.SERVER and self.server_score == 4 and self.returner_score == 3 \
                or who == self.RETURNER and self.server_score == 3 and self.returner_score == 4:
            return True
        return False

    def _check_win(self) -> int or None:
        if self.server_score >= 4 and self.score_difference > 1:
            return self.SERVER
        elif self.returner_score >= 4 and self.score_difference < -1:
            return self.RETURNER
        else:
            return None

    def _info(self) -> dict:
        return {
            'winner': 'Server' if self.server_score > self.returner_score else 'Returner',
            'total_points': self.server_score + self.returner_score,
            'server_points': self.server_score,
            'returner_points': self.returner_score
        }

    def add_point(self, winner: int) -> dict or None:
        if winner == self.SERVER:
            self._add_server_point()
        elif winner == self.RETURNER:
            self._add_returner_point()
        else:
            raise ValueError(f"Winner value {winner} not allowed.")

        if self._check_win():
            return self._info()
        return None

    def get_score(self) -> tuple[str, str]:
        if self._is_advantage(self.SERVER):
            return self.POINT_MAP[self.server_score], self.POINT_MAP[-1]
        elif self._is_advantage(self.SERVER):
            return self.POINT_MAP[-1], self.POINT_MAP[self.returner_score]
        else:
            return self.POINT_MAP[self.server_score], self.POINT_MAP[self.returner_score]


class Set:
    PLAYER1 = 1
    PLAYER2 = 2

    def __init__(self, tiebreak_to: int=7):
        self._tiebreak_to: int = tiebreak_to

        self._player1_games: int = 0
        self._player2_games: int = 0
        self._game_difference: int = 0

        self._game: Game = Game()
        self._games: list[dict] = []

    @property
    def player1_games(self) -> int:
        return self._player1_games

    @property
    def player2_games(self) -> int:
        return self._player2_games

    @property
    def game_difference(self) -> int:
        return self._game_difference

    def _add_server_game(self) -> None:
        self._player1_games += 1
        self._game_difference += 1

    def _add_returner_game(self) -> None:
        self._player1_games += 1
        self._game_difference += 1

    def _check_win(self) -> int or None:
        if self.player1_games >= 6 and self.game_difference > 2:
            return self.PLAYER1
        elif self.player2_games >= 6 and self.game_difference < -2:
            return self.PLAYER2
        else:
            return None

    def _info(self) -> dict:
        return {
            'winner': 'Server' if self.server_score > self.returner_score else 'Returner',
            'total_points': self.server_score + self.returner_score,
            'server_points': self.server_score,
            'returner_points': self.returner_score
        }

    def add_point(self, winner: int) -> dict or None:
        if winner == SERVER:
            self._add_server_point()
        elif winner == RETURNER:
            self._add_returner_point()
        else:
            raise ValueError(f"Winner value {winner} not allowed.")

        if self._check_win():
            return self._info()
        return None

    def get_score(self) -> tuple[str, str]:
        return str(self.player1_games), str(self.player2_games)


class Match:
    def __init__(
            self,
            player1_name: str,
            player2_name: str,
            best_of: int=3,
            set_tiebreak_to: int=10,
            game_tiebreak_to: int=7
    ):
        self._player1: Player = Player(player1_name)
        self._player2: Player = Player(player2_name)
        self._best_of: int = best_of
        self._set_tiebreak_to: int = set_tiebreak_to
        self._game_tiebreak_to: int = game_tiebreak_to

        self._player1_score: int = 0
        self._player2_score: int = 0

        self._set: Set = Set()
