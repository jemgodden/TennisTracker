import pandas as pd


if __name__ == "__main__":
    db = pd.DataFrame(
        columns=[
            'meta_datetime',
            'match_id',
            'player_name',
            'opponent_name',
            'set_id',
            'game_id',
            'point_id',
            'point_uuid',
            'point_won',
            'let_flag',
            'ace_flag',
            'double_fault_flag',
            'serve_type',
            'winner_type',
            'error_type'
        ]
    )
