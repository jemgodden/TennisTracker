from abc import ABC, abstractmethod
import streamlit as st

from src.player import Player
from src.utils import Players, MatchSections, other_player


class Game(ABC):
    def __init__(self, server: int):
        self._server: int = server
        self._player1_points: int = 0
        self._player2_points: int = 0
        self._score_difference: int = 0

    @property
    def server(self) -> int:
        return self._server

    @property
    def player1_points(self) -> int:
        return self._player1_points

    @property
    def player2_points(self) -> int:
        return self._player2_points

    @property
    def score_difference(self):
        return self._score_difference

    @property
    def side(self):
        return (self.player1_points + self.player2_points) % 2

    def _add_player1_point(self) -> None:
        if self._is_advantage(Players.PLAYER_2.value):
            self._player2_points -= 1
        else:
            self._player1_points += 1
        self._score_difference += 1

    def _add_player2_point(self) -> None:
        if self._is_advantage(Players.PLAYER_1.value):
            self._player1_points -= 1
        else:
            self._player2_points += 1
        self._score_difference -= 1

    @abstractmethod
    def _is_advantage(self, who: int) -> bool:
        pass

    @abstractmethod
    def game_point(self) -> int:
        pass

    @abstractmethod
    def break_point(self) -> int:
        pass

    @abstractmethod
    def _check_win(self) -> int:
        pass

    def add_point(self, winner: int) -> dict or None:
        if winner == Players.PLAYER_1.value:
            self._add_player1_point()
        elif winner == Players.PLAYER_2.value:
            self._add_player2_point()
        else:
            st.write("Hello")
            raise ValueError(f"Winner value {winner} is invalid.")

        return self._check_win()

    @abstractmethod
    def get_score(self) -> dict[str, tuple[str, str]]:
        pass


class RegularGame(Game):
    WINNING_NUM_POINTS = 4
    POINT_MAP: dict = {
        -1: '',
        0: '0',
        1: '15',
        2: '30',
        3: '40',
        4: 'AD'
    }

    def __init__(self, server: int):
        super().__init__(server)

    def _is_advantage(self, who: int) -> bool:
        return (who == Players.PLAYER_1.value and self.player1_points == self.WINNING_NUM_POINTS and self.player2_points == self.WINNING_NUM_POINTS-1) \
            or (who == Players.PLAYER_2.value and self.player1_points == self.WINNING_NUM_POINTS-1 and self.player2_points == self.WINNING_NUM_POINTS)

    def game_point(self) -> int:
        if self._is_advantage(Players.PLAYER_1.value) \
                or (self.player1_points >= 3 and self.player1_points > self.player2_points):
            return Players.PLAYER_1.value
        elif self._is_advantage(Players.PLAYER_2.value) \
                or (self.player2_points >= 3 and self.player2_points > self.player1_points):
            return Players.PLAYER_2.value
        else:
            return Players.NONE.value

    def break_point(self) -> int:
        if self.server == Players.PLAYER_2.value and self.game_point() == Players.PLAYER_1.value:
            return Players.PLAYER_1.value
        elif self.server == Players.PLAYER_1.value and self.game_point() == Players.PLAYER_2.value:
            return Players.PLAYER_2.value
        else:
            return Players.NONE.value

    def _check_win(self) -> int:
        if self.player1_points >= self.WINNING_NUM_POINTS and self.score_difference > 1:
            return Players.PLAYER_1.value
        elif self.player2_points >= self.WINNING_NUM_POINTS and self.score_difference < -1:
            return Players.PLAYER_2.value
        return Players.NONE.value

    def get_score(self) -> dict[str, tuple[str, str]]:
        if self._is_advantage(Players.PLAYER_1.value):
            return {MatchSections.POINTS.value: (self.POINT_MAP[self.player1_points], self.POINT_MAP[-1])}
        elif self._is_advantage(Players.PLAYER_2.value):
            return {MatchSections.POINTS.value: (self.POINT_MAP[-1], self.POINT_MAP[self.player2_points])}
        else:
            return {MatchSections.POINTS.value: (self.POINT_MAP[self.player1_points], self.POINT_MAP[self.player2_points])}


class TiebreakGame(Game):
    def __init__(self, server: int, tiebreak_to: int=7):
        super().__init__(server)
        self._tiebreak_to: int = tiebreak_to

    def _is_advantage(self, who: int) -> bool:
        pass

    def game_point(self) -> int:
        return (self.player1_points >= self._tiebreak_to - 1 and self.player1_points > self.player2_points) \
            or (self.player2_points >= self._tiebreak_to - 1 and self.player2_points > self.player1_points)

    def break_point(self) -> int:
        return Players.NONE.value

    def _check_win(self) -> int:
        switch_servers = (self.player1_points + self.player2_points) % 2 == 1
        if switch_servers:
            self._server = other_player(self.server)

        if self.player1_points >= self._tiebreak_to and self.score_difference > 1:
            return Players.PLAYER_1.value
        elif self.player2_points >= self._tiebreak_to and self.score_difference < -1:
            return Players.PLAYER_2.value
        return Players.NONE.value

    def get_score(self) -> dict[str, tuple[str, str]]:
        return {MatchSections.POINTS.value: (str(self.player1_points), str(self.player2_points))}


class Set(ABC):
    def __init__(self, server: int, num_games: int=6, tiebreak_to: int=7):
        self._server: int = server

        self._num_games: int = num_games
        self._tiebreak_to: int = tiebreak_to

        self._player1_games: int = 0
        self._player2_games: int = 0

        self._game = None

    @property
    def server(self) -> int:
        return self._server

    @property
    def player1_games(self) -> int:
        return self._player1_games

    @property
    def player2_games(self) -> int:
        return self._player2_games

    @property
    def game(self) -> Game:
        return self._game

    @property
    def game_difference(self) -> int:
        return abs(self.player1_games - self.player2_games)

    @abstractmethod
    def set_point(self) -> int:
        pass

    def _add_player1_game(self) -> None:
        self._player1_games += 1

    def _add_player2_game(self) -> None:
        self._player2_games += 1

    @abstractmethod
    def _check_win(self) -> int:
        pass

    def add_game(self, winner: int) -> int:
        if winner == Players.PLAYER_1.value:
            self._add_player1_game()
        elif winner == Players.PLAYER_2.value:
            self._add_player2_game()
        else:
            raise ValueError(f"Winner value {winner} not allowed.")

        self._server = other_player(self.server)
        return self._check_win()

    @abstractmethod
    def new_game(self) -> None:
        pass

    def add_point(self, winner: int) -> tuple[None or int, int, bool]:
        game_winner = self._game.add_point(winner)
        if game_winner:
            set_winner = self.add_game(game_winner)
            if set_winner == Players.NONE.value:
                self.new_game()
            return set_winner, self.server, True
        return None, self.server, False

    @abstractmethod
    def get_score(self) -> dict[str, tuple[str, str]]:
        pass


class RegularSet(Set):
    def __init__(self, server: int, num_games: int=6, tiebreak_to: int=7):
        super().__init__(server, num_games, tiebreak_to)
        self._game = RegularGame(
            server=self.server
        )

    def set_point(self) -> int:
        if self.game.game_point() == Players.PLAYER_1.value \
                and (self.player1_games >= self._num_games - 1 and self.player1_games > self.player2_games):
            return Players.PLAYER_1.value
        elif self.game.game_point() == Players.PLAYER_2.value \
                and (self.player2_games >= self._num_games - 1 and self.player2_games > self.player1_games):
            return Players.PLAYER_2.value
        else:
            return Players.NONE.value

    def _check_win(self) -> int:
        if (self.player1_games == self._num_games and self.game_difference > 1) or (self.player1_games == self._num_games + 1):
            return Players.PLAYER_1.value
        elif (self.player2_games == self._num_games and self.game_difference < -1) or (self.player2_games == self._num_games + 1):
            return Players.PLAYER_2.value
        return Players.NONE.value

    def new_game(self) -> None:
        if self.player1_games == self._num_games and self.player2_games == self._num_games:
            self._game = TiebreakGame(
                server=self.server,
                tiebreak_to=self._tiebreak_to
            )
        else:
            self._game = RegularGame(
                server=self.server
            )

    def get_score(self) -> dict[str, tuple[str, str]]:
        scores = self._game.get_score()
        return {
            **scores,
            MatchSections.GAMES.value: (str(self.player1_games), str(self.player2_games))
        }


class TiebreakSet(Set):
    def __init__(self, server: int, num_games: int=1, tiebreak_to: int=10):
        super().__init__(server, num_games, tiebreak_to)
        self._game: Game = TiebreakGame(
            server=self.server,
            tiebreak_to=self._tiebreak_to
        )

    def set_point(self) -> int:
        return self.game.game_point()

    def _check_win(self) -> int:
        if self.player1_games >= self._num_games and self.game_difference >= 1:
            return Players.PLAYER_1.value
        elif self.player2_games >= self._num_games and self.game_difference < -1:
            return Players.PLAYER_2.value
        return Players.NONE.value

    def new_game(self) -> None:
        pass

    def get_score(self) -> dict[str, tuple[str, str]]:
        scores = self._game.get_score()
        return {
            **scores,
            MatchSections.GAMES.value: ('0', '0')
        }


class Match:
    def __init__(
            self,
            player1_name: str='Player 1',
            player2_name: str='Player 2',
            server: int=1,
            match_best_of: int=3,
            set_num_games: int=6,
            set_tiebreak_to: int=10,
            final_set_tiebreak: bool=False,
            game_tiebreak_to: int=7
    ):
        self._player1: Player = Player(player1_name)
        self._player2: Player = Player(player2_name)

        if server not in [Players.PLAYER_1.value, Players.PLAYER_2.value]:
            raise ValueError(f"Server value {server} is invalid.")
        self._server: int = server

        self._winning_num_sets = (match_best_of // 2) + 1
        self._set_num_games: int = set_num_games
        self._set_tiebreak_to: int = set_tiebreak_to
        self._final_set_tiebreak: bool = final_set_tiebreak
        self._game_tiebreak_to: int = game_tiebreak_to

        self._player1_sets: int = 0
        self._player2_sets: int = 0

        self._set_number: int = 1
        self._game_number: int = 1
        self._point_number: int = 1

        if match_best_of == 1 and final_set_tiebreak:
            self._set: Set = TiebreakSet(
                server=self.server,
                num_games=set_num_games,
                tiebreak_to=game_tiebreak_to
            )
        else:
            self._set: Set = RegularSet(
                server=self.server,
                num_games=set_num_games,
                tiebreak_to=game_tiebreak_to
            )

    @property
    def player1_name(self) -> str:
        return self._player1.name

    @property
    def player2_name(self) -> str:
        return self._player2.name

    @property
    def player1_sets(self) -> int:
        return self._player1_sets

    @property
    def player2_sets(self) -> int:
        return self._player2_sets

    @property
    def set(self) -> Set:
        return self._set

    @property
    def set_number(self) -> int:
        return self._set_number

    @property
    def game_number(self) -> int:
        return self._game_number

    @property
    def point_number(self) -> int:
        return self._point_number

    @property
    def server(self) -> int:
        return self._server

    @property
    def current_server(self) -> int:
        return self.set.game.server

    @property
    def side(self) -> int:
        return self._set.game.side

    @property
    def point_uuid(self) -> str:
        return f"{self.set_number}-{self.game_number}-{self.point_number}-{self.current_server}-{self.side}"

    def break_point(self) -> int:
        return self.set.game.break_point()

    def set_point(self) -> int:
        return self.set.set_point()

    def match_point(self) -> int:
        if self.set.game.game_point() == Players.PLAYER_1.value \
            and self.set_point() == Players.PLAYER_1.value \
                and self.player1_sets >= self._winning_num_sets - 1:
            return Players.PLAYER_1.value
        elif self.set.game.game_point() == Players.PLAYER_2.value \
            and self.set_point() == Players.PLAYER_2.value \
                and self.player2_sets >= self._winning_num_sets - 1:
            return Players.PLAYER_2.value
        else:
            return Players.NONE.value

    def _add_player1_set(self) -> None:
        self._player1_sets += 1

    def _add_player2_set(self) -> None:
        self._player2_sets += 1

    def _check_win(self) -> int:
        if self.player1_sets == self._winning_num_sets:
            return Players.PLAYER_1.value
        elif self.player2_sets == self._winning_num_sets:
            return Players.PLAYER_2.value
        return Players.NONE.value

    def add_set(self, winner: int) -> int:
        if winner == Players.PLAYER_1.value:
            self._add_player1_set()
        elif winner == Players.PLAYER_2.value:
            self._add_player2_set()
        else:
            raise ValueError(f"Winner value {winner} not allowed.")

        return self._check_win()

    def new_set(self) -> None:
        if self._final_set_tiebreak and self.player1_sets == self._winning_num_sets - 1 \
                and self.player2_sets == self._winning_num_sets - 1:
            self._set = TiebreakSet(
                server=self.server,
                tiebreak_to=self._set_tiebreak_to
            )
        else:
            self._set = RegularSet(
                server=self.server,
                num_games=self._set_num_games,
                tiebreak_to=self._game_tiebreak_to
            )

    def add_point(self, winner: int) -> None or int:
        if winner not in [Players.PLAYER_1.value, Players.PLAYER_2.value]:
            raise ValueError(f"Winner value {winner} is invalid.")

        set_winner, next_server, game_end = self.set.add_point(winner)
        self._point_number += 1
        self._server = next_server

        if game_end:
            self._game_number += 1
        if set_winner:
            match_winner = self.add_set(set_winner)
            if match_winner == Players.NONE.value:
                self._set_number += 1
                self.new_set()
            return match_winner
        return None

    def get_score(self) -> dict[str, tuple[str, str]]:
        scores = self._set.get_score()
        return {
            **scores,
            MatchSections.SETS.value: (str(self.player1_sets), str(self.player2_sets))
        }
