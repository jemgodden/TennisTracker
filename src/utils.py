import pandas as pd
from datetime import datetime, timezone
from enum import Enum, auto


"""
This file contains a number of utility functions used across both the tennis scoring backend, and throughout the application frontend.
"""


DEFAULT_VALUE = None


class MatchSections(Enum):
    POINTS = 'points'
    GAMES = 'games'
    SETS = 'sets'


class Players(Enum):
    NONE = 0
    PLAYER_1 = 1
    PLAYER_2 = 2


class Side(Enum):
    DEUCE = 0
    AD = 1


class Serve(Enum):
    ACE = auto()
    FIRST_SERVE = auto()
    SECOND_SERVE = auto()
    DOUBLE_FAULT = auto()


class ServeType(Enum):
    FLAT = auto()
    KICK = auto()
    SLICE = auto()
    UNDERARM = auto()


class ServeTarget(Enum):
    INSIDE = auto()
    BODY = auto()
    OUTSIDE = auto()
    SHORT = auto()


class NetApproachType(Enum):
    AGGRESSIVE = auto()
    DEFENSIVE = auto()


class RallyLength(Enum):
    RL_0_2 = auto()
    RL_3_5 = auto()
    RL_6_8 = auto()
    RL_9_PLUS = auto()


class FinalShot(Enum):
    WINNER = auto()
    ERROR = auto()
    UNFORCED_ERROR = auto()


class FinalShotHand(Enum):
    FOREHAND = auto()
    BACKHAND = auto()
    OTHER = auto()


class FinalShotType(Enum):
    DRIVE = auto()
    SLICE = auto()
    SMASH = auto()
    VOLLEY = auto()
    DROP_SHOT = auto()
    LOB = auto()
    OTHER = auto()


def format_enum_name(enum_name: str, rally_length: bool=False) -> str:
    """
    Formats the enum name to make it more human-readable.

    :param enum_name: string value for enum name.
    :param rally_length: boolean flag to indicate if enum is RallyLength, which requires different formatting.
    :return: formatted string value for enum name.
    """
    if rally_length:
        return enum_name[3:].replace("_PLUS", "+").replace("_", "-")
    return " ".join([word[0]+word[1:].lower() for word in enum_name.split("_")])


def other_player(input_player: int):
    """
    Returns the integer value for the other player to the given input player.

    :param input_player: integer value for current player.
    :return: integer value for other player.
    """
    # return Players.PLAYER_1.value if input_player == Players.PLAYER_2.value else Players.PLAYER_2.value
    return (input_player % 2) + 1


def create_backend_df() -> pd.DataFrame:
    df = pd.DataFrame(
        columns=[
            'point_datetime',
            'point_uuid',
            'set_id',
            'game_id',
            'point_id',
            'match_point',
            'set_point',
            'break_point',
            'server',
            'side',
            'winner',
            'ace_flag',
            'double_fault_flag',
            'serve',
            'serve_type',
            'serve_target',
            'net_approach',
            'first_net_approacher',
            'net_approach_type',
            'rally_length',
            'final_shot',
            'final_shot_hand',
            'final_shot_type',
            # 'final_shot_spin',
            # 'final_shot_target'
            'meta_match_datetime',
            'meta_player1_name',
            'meta_player2_name',
        ]
    )
    return df


def add_ace(session_state: dict, serve_target: int, serve_type: int = ServeType.FLAT.value) -> None:
    """
    Quickly add an ace to the backend data.

    :param session_state: streamlit session state dictionary.
    :param serve_target: ServeTarget enum value.
    :param serve_type: ServeType enum value, defaulted to FLAT.
    """
    df = session_state['match_data']
    match = session_state['match']

    df.loc[len(df)] = [
        datetime.now(timezone.utc),
        match.point_uuid,
        match.set_number,
        match.game_number,
        match.point_number,
        match.match_point(),
        match.set_point(),
        match.break_point(),
        match.current_server,
        match.side,
        match.current_server,
        True,
        False,
        Serve.ACE.value,
        serve_type,
        serve_target,
        False,
        DEFAULT_VALUE,
        DEFAULT_VALUE,
        RallyLength.RL_0_1.value,
        FinalShot.WINNER.value,
        DEFAULT_VALUE,
        DEFAULT_VALUE,
        session_state['match_datetime'],
        session_state['player1_name'],
        session_state['player2_name'],
    ]


def add_double_fault(session_state: dict) -> None:
    """
    Quickly add a double fault to the backend data.

    :param session_state: streamlit session state dictionary.
    """
    df = session_state['match_data']
    match = session_state['match']

    df.loc[len(df)] = [
        datetime.now(timezone.utc),
        match.point_uuid,
        match.set_number,
        match.game_number,
        match.point_number,
        match.match_point(),
        match.set_point(),
        match.break_point(),
        match.current_server,
        match.side,
        Players.PLAYER_2.value if match.current_server == Players.PLAYER_1.value else Players.PLAYER_1.value,
        False,
        True,
        Serve.DOUBLE_FAULT.value,
        DEFAULT_VALUE,
        DEFAULT_VALUE,
        False,
        DEFAULT_VALUE,
        DEFAULT_VALUE,
        RallyLength.RL_0_1.value,
        DEFAULT_VALUE,
        DEFAULT_VALUE,
        DEFAULT_VALUE,
        session_state['match_datetime'],
        session_state['player1_name'],
        session_state['player2_name'],
    ]


def add_point(session_state: dict) -> None:
    """
    Add a point to the backend data using information the streamlit session state dictionary.

    :param session_state: streamlit session state dictionary.
    """
    if session_state['winner'] is None:
        raise ValueError("No winner was selected for the point so it was not added to the data.")

    df = session_state['match_data']
    match = session_state['match']

    df.loc[len(df)] = [
        datetime.now(timezone.utc),
        match.point_uuid,
        match.set_number,
        match.game_number,
        match.point_number,
        match.match_point(),
        match.set_point(),
        match.break_point(),
        match.current_server,
        match.side,
        session_state['winner'],
        True if session_state['serve'] == Serve.ACE.value else False,
        True if session_state['serve'] == Serve.DOUBLE_FAULT.value else False,
        session_state['serve'],
        session_state['serve_type'],
        session_state['serve_target'],
        session_state['net_approach'],
        session_state['first_net_approacher'],
        session_state['net_approach_type'],
        session_state['rally_length'],
        session_state['final_shot'],
        session_state['final_shot_hand'],
        session_state['final_shot_type'],
        session_state['match_datetime'],
        session_state['player1_name'],
        session_state['player2_name'],
    ]


def add_player_data(player: int, match_data: pd.DataFrame) -> dict[str, pd.DataFrame]:
    data = {
        'all_points': match_data,
        'points_won': match_data[(match_data.winner == player)],
        'points_lost': match_data[(match_data.winner == other_player(player))],
        'break_points': match_data[(match_data.break_point == player)],
        'set_points': match_data[(match_data.set_point == player)],
        'match_points': match_data[(match_data.match_point == player)],
        'serves': match_data[(match_data.server == player)],
        'returns': match_data[(match_data.server == other_player(player))],
        'net_approach_points': match_data[(match_data.net_approach == True) & (match_data.first_net_approacher == player)],
    }

    data['break_points_won'] = data['break_points'][(data['break_points'].winner == player)]
    data['set_points_won'] = data['set_points'][(data['set_points'].winner == player)]
    data['match_points_won'] = data['match_points'][(data['match_points'].winner == player)]

    data['aces'] = data['serves'][(data['serves'].serve == Serve.ACE.value)]
    data['first_serves'] = data['serves'][(data['serves'].serve.isin([Serve.ACE.value, Serve.FIRST_SERVE.value]))]
    data['second_serves'] = data['serves'][(data['serves'].serve == Serve.SECOND_SERVE.value)]
    data['double_faults'] = data['serves'][(data['serves'].serve == Serve.DOUBLE_FAULT.value)]

    data['serve_points_won'] = data['serves'][(data['serves'].winner == player)]
    data['first_serve_points_won'] = data['serve_points_won'][(data['serve_points_won'].serve.isin([Serve.ACE.value, Serve.FIRST_SERVE.value]))]
    data['second_serve_points_won'] = data['serve_points_won'][(data['serve_points_won'].serve == Serve.SECOND_SERVE.value)]

    data['winners'] = data['points_won'][(data['points_won'].final_shot == FinalShot.WINNER.value)]
    data['errors'] = data['points_lost'][(data['points_lost'].final_shot == FinalShot.ERROR.value)]
    data['unforced_errors'] = data['points_lost'][(data['points_lost'].final_shot == FinalShot.UNFORCED_ERROR.value)]

    data['final_shot'] = pd.concat([data['winners'], data['errors'], data['unforced_errors']])

    data['net_approach_points_won'] = data['net_approach_points'][(data['net_approach_points'].winner == player)]

    return data
