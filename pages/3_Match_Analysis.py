import pandas as pd
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import matplotlib.pyplot as plt
import numpy as np

from src.utils import *


plt.style.use('dark_background')
np.seterr(divide='ignore', invalid='ignore')


# Application page - 'Match Analysis':
# Show summary statistics for the current match.
# Let the user visualise information about the players performance in the current match, using filters to see desired data.


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
        st.header("Overview")

        overview_match_data = st.session_state['match_data']

        overview_set_filter = st.pills(
            "Select All Sets To Show Statistics For",
            options=st.session_state['match_data'].set_id.unique(),
            selection_mode="multi",
            default=st.session_state['match_data'].set_id.unique(),
            key='overview_set_filter',
        )
        overview_match_data = overview_match_data[overview_match_data['set_id'].isin(overview_set_filter)]

        overview_title_left, overview_title_middle, overview_title_right = st.columns(3)
        overview_title_left.markdown(f"<h3 style='text-align: center;'>{st.session_state['player1_name']}</h3>", unsafe_allow_html=True)
        overview_title_middle.markdown(f"<h3 style='text-align: center;'>VS</h3>", unsafe_allow_html=True)
        overview_title_right.markdown(f"<h3 style='text-align: center;'>{st.session_state['player2_name']}</h3>", unsafe_allow_html=True)
        st.divider()

        overview_body_left, overview_body_middle, overview_body_right = st.columns(3)

        def add_player_data(player: int, match_data: pd.DataFrame) -> dict[str, pd.DataFrame]:
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

            data['net_approach_points_won'] = data['points_won'][(data['points_won'].net_approach == True)]

            return data

        player_data = {
            Players.PLAYER_1.value: add_player_data(Players.PLAYER_1.value, overview_match_data),
            Players.PLAYER_2.value: add_player_data(Players.PLAYER_2.value, overview_match_data)
        }

        def add_stat(title: str, player1_val: int or float, player2_val: int or float, end_str: str=""):
            overview_body_left.markdown(f"<h6 style='text-align: center;'>{player1_val}{end_str}</h6>", unsafe_allow_html=True)
            overview_body_middle.markdown(f"<h6 style='text-align: center;'>{title}</h6>", unsafe_allow_html=True)
            overview_body_right.markdown(f"<h6 style='text-align: center;'>{player2_val}{end_str}</h6>", unsafe_allow_html=True)

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
            ((player_data[Players.PLAYER_1.value]['first_serve_points_won'].shape[0] / player_data[Players.PLAYER_1.value]['first_serves'].shape[0]) * 100) if player_data[Players.PLAYER_1.value]['first_serves'].shape[0] > 0 else 0,
            ((player_data[Players.PLAYER_2.value]['first_serve_points_won'].shape[0] / player_data[Players.PLAYER_2.value]['first_serves'].shape[0]) * 100) if player_data[Players.PLAYER_2.value]['first_serves'].shape[0] > 0 else 0,
            "%"
        )

        add_stat(
            "Second Serve Win %",
            ((player_data[Players.PLAYER_1.value]['second_serve_points_won'].shape[0] / player_data[Players.PLAYER_1.value]['second_serves'].shape[0]) * 100) if player_data[Players.PLAYER_1.value]['second_serves'].shape[0] > 0 else 0,
            ((player_data[Players.PLAYER_2.value]['second_serve_points_won'].shape[0] / player_data[Players.PLAYER_2.value]['second_serves'].shape[0]) * 100) if player_data[Players.PLAYER_2.value]['second_serves'].shape[0] > 0 else 0,
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

    with st.container():
        st.header("Analysis")

        analysis_match_data = st.session_state['match_data']

        analysis_filter_left, analysis_filter_right = st.columns(2)

        player_map = {
            Players.PLAYER_1.value: st.session_state['player1_name'],
            Players.PLAYER_2.value: st.session_state['player2_name'],
        }
        analysis_player_filter = analysis_filter_left.selectbox(
            "Select Player To Show Analysis For",
            options=player_map.keys(),
            format_func=lambda val: player_map[val],
            key='analysis_player_filter',
        )

        analysis_set_filter = analysis_filter_right.pills(
            "Select All Sets To Show Analysis For",
            options=st.session_state['match_data'].set_id.unique(),
            selection_mode="multi",
            default=st.session_state['match_data'].set_id.unique(),
            key='analysis_set_filter',
        )
        analysis_match_data = analysis_match_data[analysis_match_data['set_id'].isin(analysis_set_filter)]

        with st.container():
            st.subheader("Serve")

            # TODO: Breakdown by serve type.
            # TODO: Breakdown by serve target.
            try:
                serve_data = analysis_match_data[analysis_match_data['server'] == analysis_player_filter]

                serve_fig, serve_ax = plt.subplots()

                serve_ax.pie(
                    [serve_data[serve_data['serve'] == enum.value].shape[0] for enum in Serve],
                    explode=(0.1, 0.1, 0.1, 0.1),
                    labels=("Ace", "First Serve", "Second Serve", "Double Fault"),
                    autopct='%1.1f%%',
                    shadow=True,
                    startangle=90
                )

                st.pyplot(serve_fig)
            except:
                st.warning("There is no relevant match data to analyse.")

        with st.container():
            st.subheader("Net")

            # TODO: Breakdown by percentage of service points that go to net.

            try:
                net_x_labels = ("Aggressive", "Forced")

                net_server_data = analysis_match_data[analysis_match_data['server'] == analysis_player_filter]
                net_returner_data = analysis_match_data[analysis_match_data['server'] == other_player(analysis_player_filter)]
                net_data = {
                    'Server': [net_server_data[net_server_data.net_approach_type == enum.value].shape[0] for enum in NetApproachType],
                    'Returner': [net_returner_data[net_server_data.net_approach_type == enum.value].shape[0] for enum in NetApproachType],
                }

                net_fig, net_ax = plt.subplots()

                net_x = np.arange(len(net_x_labels))  # the label locations
                net_width = 0.4  # width of the bars
                net_multiplier = 0

                for net_attribute, net_measurement in net_data.items():
                    net_offset = net_width * net_multiplier
                    net_rects = net_ax.bar(net_x + net_offset, net_measurement, net_width, label=net_attribute)
                    net_ax.bar_label(net_rects, padding=3)
                    net_multiplier += 1

                net_ax.set_xticks(net_x + (net_width / 2), net_x_labels)
                net_ax.legend(loc='upper right')

                st.pyplot(net_fig)
            except:
                st.warning("There is no relevant match data to analyse.")

        with st.container():
            st.subheader("Rally Length")

            rally_length_server_data = analysis_match_data[analysis_match_data.server == analysis_player_filter]
            rally_length_data = [rally_length_server_data[rally_length_server_data.rally_length == enum.value].shape[0] for enum in RallyLength]

            rally_length_fig, rally_length_ax = plt.subplots()
            rally_length_ax.bar(("0-1", "2-4", "5-8", "9+"), rally_length_data)

            st.pyplot(rally_length_fig)

        with st.container():
            st.subheader("Winners & Errors")

            # TODO: Breakdown by final shot type.

            try:
                fs_x_labels = ("Winner", "Error", "Unforced Error")

                fs_point_winner_data = analysis_match_data[analysis_match_data['winner'] == analysis_player_filter]
                fs_winner_data = fs_point_winner_data[fs_point_winner_data['final_shot'] == FinalShot.WINNER.value]
                fs_point_loser_data = analysis_match_data[analysis_match_data['winner'] == other_player(analysis_player_filter)]
                fs_error_data = fs_point_loser_data[fs_point_loser_data['final_shot'] == FinalShot.ERROR.value]
                fs_unforced_error_data = fs_point_loser_data[fs_point_loser_data['final_shot'] == FinalShot.UNFORCED_ERROR.value]

                fs_data = {
                    'Forehand': [
                        fs_winner_data[fs_winner_data['final_shot_hand'] == FinalShotHand.FOREHAND.value].shape[0],
                        fs_error_data[fs_error_data['final_shot_hand'] == FinalShotHand.FOREHAND.value].shape[0],
                        fs_unforced_error_data[fs_unforced_error_data['final_shot_hand'] == FinalShotHand.FOREHAND.value].shape[0],
                    ],
                    'Backhand': [
                        fs_winner_data[fs_winner_data['final_shot_hand'] == FinalShotHand.BACKHAND.value].shape[0],
                        fs_error_data[fs_error_data['final_shot_hand'] == FinalShotHand.BACKHAND.value].shape[0],
                        fs_unforced_error_data[fs_unforced_error_data['final_shot_hand'] == FinalShotHand.BACKHAND.value].shape[0],
                    ],
                }

                fs_fig, fs_ax = plt.subplots()

                fs_x = np.arange(len(fs_x_labels))  # the label locations
                fs_width = 0.4  # width of the bars
                fs_multiplier = 0

                for fs_attribute, fs_measurement in fs_data.items():
                    fs_offset = fs_width * fs_multiplier
                    fs_rects = fs_ax.bar(fs_x + fs_offset, fs_measurement, fs_width, label=fs_attribute)
                    fs_ax.bar_label(fs_rects, padding=3)
                    net_multiplier += 1

                fs_ax.set_xticks(fs_x + (fs_width / 2), fs_x_labels)
                fs_ax.legend(loc='upper right')

                st.pyplot(fs_fig)
            except:
                st.warning("There is no relevant match data to analyse.")

    with st.container():
        st.write("###")
        st.divider()
        left, right = st.columns(2)
        if left.button("Add to Current Match"):
            switch_page("New_Match")
        if right.button("Load Another Match"):
            switch_page("Load Match")
