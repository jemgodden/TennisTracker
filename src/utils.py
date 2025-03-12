import pandas as pd
from datetime import datetime, timezone
from enum import Enum


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
    ACE = 0
    FIRST_SERVE = 1
    SECOND_SERVE = 2
    DOUBLE_FAULT = 3


class ServeType(Enum):
    FLAT = 0
    KICK = 1
    SLICE = 2
    UNDERARM = 3


class ServeTarget(Enum):
    INSIDE = 0
    BODY = 1
    OUTSIDE = 2
    SHORT = 3


class NetApproachType(Enum):
    AGGRESSIVE = 0
    FORCED = 1


class RallyLength(Enum):
    RL_0_1 = 0
    RL_2_4 = 1
    RL_5_8 = 2
    RL_9_PLUS = 3


class FinalShot(Enum):
    WINNER = 0
    ERROR = 1
    UNFORCED_ERROR = 2


class FinalShotHand(Enum):
    FOREHAND = 0
    BACKHAND = 1
    OTHER = 2


class FinalShotType(Enum):
    DRIVE = 0
    VOLLEY = 1
    SMASH = 2
    DROP_SHOT = 3
    LOB = 4
    OTHER = 5


def other_player(input_player: int):
    # return Players.PLAYER_1.value if input_player == Players.PLAYER_2.value else Players.PLAYER_2.value
    return (input_player % 2) + 1


def create_backend_df() -> pd.DataFrame:
    df = pd.DataFrame(
        columns=[
            'meta_datetime',
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
        ]
    )
    return df


def add_ace(session_state: dict, serve_target: int, serve_type: int = ServeType.FLAT.value) -> None:
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
        DEFAULT_VALUE
    ]


def add_double_fault(session_state: dict) -> None:
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
        DEFAULT_VALUE
    ]


def add_point(session_state: dict) -> None:
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
        session_state['final_shot_type']
    ]
