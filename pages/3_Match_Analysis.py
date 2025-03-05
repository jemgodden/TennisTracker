import pandas as pd
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import matplotlib.pyplot as plt
import numpy as np

from src.utils import *


np.seterr(divide='ignore', invalid='ignore')


if __name__ == "__main__":

    st.set_page_config(
        page_title="Analysis",
        # initial_sidebar_state="collapsed",
    )

    st.title("Analysis")

    with st.container():
        st.header(f"Match: {st.session_state['player1_name']} vs {st.session_state['player2_name']}")
        st.subheader(f"Played: {st.session_state['match_datetime'].strftime('%d/%m/%Y %H:%M:%S')}")

    with st.container():
        st.write("######")
        if st.toggle("Show Data"):
            st.dataframe(st.session_state['match_data'])
        st.caption("Only intended for developer use.")

    if st.session_state['match_data'].empty:
        st.warning("There is no match data to analyse.")
        st.stop()

    with st.container():
        st.header("Set Filter")

        set_filter = st.pills(
            "Select All Sets To Show Data For",
            options=st.session_state['match_data'].set_id.unique(),
            selection_mode="multi",
            default=st.session_state['match_data'].set_id.unique(),
            key='set_filter',
        )
        match_data = st.session_state['match_data'][st.session_state['match_data']['set_id'].isin(set_filter)]

    with st.container():
        st.header("Overview")

        left_title, middle_title, right_title = st.columns(3)
        left_title.markdown(f"<h3 style='text-align: center;'>{st.session_state['player1_name']}</h3>", unsafe_allow_html=True)
        middle_title.markdown(f"<h3 style='text-align: center;'>VS</h3>", unsafe_allow_html=True)
        right_title.markdown(f"<h3 style='text-align: center;'>{st.session_state['player2_name']}</h3>", unsafe_allow_html=True)
        st.divider()

        left_body, middle_body, right_body = st.columns(3)

        def add_player_data(player: int) -> dict[str, pd.DataFrame]:
            data = {
                'points_won': match_data[(match_data.winner == player)],
                'points_lost': match_data[(match_data.winner == other_player(player))],
                'match_points': match_data[(match_data.match_point == player)],
                'set_points': match_data[(match_data.set_point == player)],
                'break_points': match_data[(match_data.break_point == player)],
                'serves': match_data[(match_data.server == player)],
                'returns': match_data[(match_data.server == other_player(player))],
                'net_approach_points': match_data[(match_data.net_approach == True)],
            }

            data['aces'] = data['serves'][(match_data.serve == Serve.ACE.value)]
            data['first_serves'] = data['serves'][(match_data.serve.isin([Serve.ACE.value, Serve.FIRST_SERVE.value]))]
            data['double_faults'] = data['serves'][(match_data.serve == Serve.DOUBLE_FAULT.value)]

            data['serve_points_won'] = data['points_won'][(match_data.serve == player)]
            data['first_serve_points_won'] = data['serve_points_won'][(match_data.serve.isin([Serve.ACE.value, Serve.FIRST_SERVE.value]))]
            data['second_serve_points_won'] = data['serve_points_won'][(match_data.serve == Serve.DOUBLE_FAULT.value)]

            data['winners'] = data['points_won'][(match_data.serve == FinalShot.WINNER.value)]
            data['errors'] = data['points_lost'][(match_data.serve == FinalShot.ERROR.value)]
            data['unforced_errors'] = data['points_lost'][(match_data.serve == FinalShot.UNFORCED_ERROR.value)]

            data['final_shot'] = pd.concat([data['winners'], data['errors'], data['unforced_errors']])

            data['net_approach_points_won'] = data['points_won'][(match_data.net_approach == True)]

            return data

        player_data = {
            Players.PLAYER_1.value: add_player_data(Players.PLAYER_1.value),
            Players.PLAYER_2.value: add_player_data(Players.PLAYER_2.value)
        }

        def add_stat(title: str, player1_val: int or float, player2_val: int or float, end_str: str=""):
            left_body.markdown(f"<h6 style='text-align: center;'>{player1_val}{end_str}</h6>", unsafe_allow_html=True)
            middle_body.markdown(f"<h6 style='text-align: center;'>{title}</h6>", unsafe_allow_html=True)
            right_body.markdown(f"<h6 style='text-align: center;'>{player2_val}{end_str}</h6>", unsafe_allow_html=True)

        add_stat(
            "Points Won",
            player_data[Players.PLAYER_1.value]['points_won'].shape[0],
            player_data[Players.PLAYER_2.value]['points_won'].shape[0]
        )

        add_stat(
            "Aces",
            player_data[Players.PLAYER_1.value]['aces'].shape[0],
            player_data[Players.PLAYER_2.value]['aces'].shape[0]
        )

        add_stat(
            "Double Faults",
            player_data[Players.PLAYER_1.value]['double_faults'].shape[0],
            player_data[Players.PLAYER_2.value]['double_faults'].shape[0]
        )

        add_stat(
            "First Serve %",
            ((player_data[Players.PLAYER_1.value]['first_serves'].shape[0] / player_data[Players.PLAYER_1.value]['serves'].shape[0]) * 100) if player_data[Players.PLAYER_1.value]['serves'].shape[0] > 0 else 0,
            ((player_data[Players.PLAYER_2.value]['first_serves'].shape[0] / player_data[Players.PLAYER_2.value]['serves'].shape[0]) * 100) if player_data[Players.PLAYER_2.value]['serves'].shape[0] > 0 else 0,
            "%"
        )

        add_stat(
            "First Serve Win %",
            ((player_data[Players.PLAYER_1.value]['first_serve_points_won'].shape[0] / player_data[Players.PLAYER_1.value]['serves'].shape[0]) * 100) if player_data[Players.PLAYER_1.value]['serves'].shape[0] > 0 else 0,
            ((player_data[Players.PLAYER_2.value]['first_serve_points_won'].shape[0] / player_data[Players.PLAYER_2.value]['serves'].shape[0]) * 100) if player_data[Players.PLAYER_2.value]['serves'].shape[0] > 0 else 0,
            "%"
        )

        add_stat(
            "Second Serve Win %",
            ((player_data[Players.PLAYER_1.value]['second_serve_points_won'].shape[0] / player_data[Players.PLAYER_1.value]['serves'].shape[0]) * 100) if player_data[Players.PLAYER_1.value]['serves'].shape[0] > 0 else 0,
            ((player_data[Players.PLAYER_2.value]['second_serve_points_won'].shape[0] / player_data[Players.PLAYER_2.value]['serves'].shape[0]) * 100) if player_data[Players.PLAYER_2.value]['serves'].shape[0] > 0 else 0,
            "%"
        )

        # Should add stuff about returning here.

        add_stat(
            "Winners",
            player_data[Players.PLAYER_1.value]['winners'].shape[0],
            player_data[Players.PLAYER_2.value]['winners'].shape[0]
        )

        add_stat(
            "Errors",
            player_data[Players.PLAYER_1.value]['errors'].shape[0],
            player_data[Players.PLAYER_2.value]['errors'].shape[0]
        )

        add_stat(
            "Unforced Errors",
            player_data[Players.PLAYER_1.value]['unforced_errors'].shape[0],
            player_data[Players.PLAYER_2.value]['unforced_errors'].shape[0]
        )

        add_stat(
            "Net Approach Win %",
            ((player_data[Players.PLAYER_1.value]['net_approach_points_won'].shape[0] / player_data[Players.PLAYER_1.value]['net_approach_points'].shape[0]) * 100) if player_data[Players.PLAYER_1.value]['net_approach_points'].shape[0] > 0 else 0,
            ((player_data[Players.PLAYER_2.value]['net_approach_points_won'].shape[0] / player_data[Players.PLAYER_2.value]['net_approach_points'].shape[0]) * 100) if player_data[Players.PLAYER_2.value]['net_approach_points'].shape[0] > 0 else 0,
            "%"
        )

    # with st.container():
    #     st.header("Serve")
    #
    #     try:
    #         fig, (ax1, ax2) = plt.subplots(1, 2)
    #
    #         p1_serve_data = player_data[Players.PLAYER_1.value]['serves']
    #         p1_serve_type_data = []
    #         p1_serve_type_labels = []
    #         for serve_type in ServeType:
    #             count = p1_serve_data[p1_serve_data.serve_type == serve_type.value].shape[0]
    #             if count > 0:
    #                 p1_serve_type_data.append(count)
    #                 p1_serve_type_labels.append(serve_type.name)
    #
    #         ax1.pie(
    #             p1_serve_type_data,
    #             explode=[0.1 for _ in p1_serve_type_data],
    #             labels=p1_serve_type_labels,
    #             # colors=,
    #             autopct='%1.1f%%',
    #             shadow=True,
    #             startangle=90
    #         )
    #         ax1.axis('equal')
    #
    #         p2_serve_data = player_data[Players.PLAYER_2.value]['serves']
    #         p2_serve_type_data = []
    #         p2_serve_type_labels = []
    #         for serve_type in ServeType:
    #             count = p2_serve_data[p2_serve_data.serve_type == serve_type.value].shape[0]
    #             if count > 0:
    #                 p2_serve_type_data.append(count)
    #                 p2_serve_type_labels.append(serve_type.name)
    #
    #         ax2.pie(
    #             p2_serve_type_data,
    #             explode=[0.1 for _ in p2_serve_type_data],
    #             labels=p2_serve_type_labels,
    #             autopct='%1.1f%%',
    #             shadow=True,
    #             startangle=90
    #         )
    #         ax2.axis('equal')
    #
    #         st.pyplot(fig)
    #     except RuntimeError:
    #         pass

    with st.container():
        st.header("Rally Length")

        rl_x_labels = ("0", "1-4", "5-8", "9+")
        rl_p1_serves_data = player_data[Players.PLAYER_1.value]['serves']
        rl_p1_data = [rl_p1_serves_data[rl_p1_serves_data.rally_length == enum.value].shape[0] for enum in RallyLength]
        rl_p2_serves_data = player_data[Players.PLAYER_2.value]['serves']
        rl_p2_data = [rl_p2_serves_data[rl_p2_serves_data.rally_length == enum.value].shape[0] for enum in RallyLength]
        rl_data = {
            st.session_state['player1_name']: rl_p1_data,
            st.session_state['player2_name']: rl_p2_data,
        }

        rl_fig, rl_ax = plt.subplots()

        rl_x = np.arange(len(rl_x_labels))  # the label locations
        rl_width = 0.25  # width of the bars
        rl_multiplier = 0

        for attribute, measurement in rl_data.items():
            offset = rl_width * rl_multiplier
            rects = rl_ax.bar(rl_x + offset, measurement, rl_width, label=attribute)
            rl_ax.bar_label(rects, padding=3)
            rl_multiplier += 1

        rl_ax.set_ylabel('Count')
        rl_ax.set_xticks(rl_x + rl_width, rl_x_labels)
        rl_ax.legend(loc='upper left', ncols=2)

        st.pyplot(rl_fig)

        rl1_player = st.selectbox(
            "Select Serving Player",
            (
                st.session_state['player1_name'],
                st.session_state['player2_name']
            )
        )
        rl1_player_val = Players.PLAYER_1.value if rl1_player == st.session_state['player1_name'] else Players.PLAYER_2.value

        rl1_serves_data = match_data[match_data.server == rl1_player_val]
        rl1_data = [rl1_serves_data[rl1_serves_data.rally_length == enum.value].shape[0] for enum in RallyLength]

        rl1_fig, rl1_ax = plt.subplots()

        rl1_ax.bar(("0", "1-4", "5-8", "9+"), rl1_data)

        st.pyplot(rl1_fig)

    with st.container():
        st.header("Net")

    with st.container():
        st.header("Winners & Errors")

    with st.container():
        st.write("###")
        st.divider()
        left, right = st.columns(2)
        if left.button("Add to Current Match"):
            switch_page("New_Match")
        if right.button("Load Another Match"):
            switch_page("Load Match")
