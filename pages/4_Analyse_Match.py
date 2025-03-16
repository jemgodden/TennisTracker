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
# Let the user visualise information about the players' performance in the current match, using filters to see desired data.


if __name__ == "__main__":

    st.set_page_config(
        page_title="Analyse Match",
        page_icon=":chart_with_upwards_trend:",
        layout='wide',
        # initial_sidebar_state="collapsed",
    )

    st.title("Analysis :chart_with_upwards_trend:")

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

        player_data = {
            Players.PLAYER_1.value: add_player_data(Players.PLAYER_1.value, overview_match_data),
            Players.PLAYER_2.value: add_player_data(Players.PLAYER_2.value, overview_match_data)
        }

        overview_body_left, overview_body_middle, overview_body_right = st.columns(3)

        def add_stat(title: str, player1_val: int or float or str, player2_val: int or float or str, end_str: str=""):
            overview_body_left.markdown(f"<h6 style='text-align: center;'>{player1_val}{'' if player1_val == '-' else end_str}</h6>", unsafe_allow_html=True)
            overview_body_middle.markdown(f"<h6 style='text-align: center;'>{title}</h6>", unsafe_allow_html=True)
            overview_body_right.markdown(f"<h6 style='text-align: center;'>{player2_val}{'' if player2_val == '-' else end_str}</h6>", unsafe_allow_html=True)

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
            round(((player_data[Players.PLAYER_1.value]['first_serves'].shape[0] / player_data[Players.PLAYER_1.value]['serves'].shape[0]) * 100), 1) if player_data[Players.PLAYER_1.value]['serves'].shape[0] > 0 else '-',
            round(((player_data[Players.PLAYER_2.value]['first_serves'].shape[0] / player_data[Players.PLAYER_2.value]['serves'].shape[0]) * 100), 1) if player_data[Players.PLAYER_2.value]['serves'].shape[0] > 0 else '-',
            "%"
        )

        add_stat(
            "First Serve Win %",
            round(((player_data[Players.PLAYER_1.value]['first_serve_points_won'].shape[0] / player_data[Players.PLAYER_1.value]['first_serves'].shape[0]) * 100), 1) if player_data[Players.PLAYER_1.value]['first_serves'].shape[0] > 0 else '-',
            round(((player_data[Players.PLAYER_2.value]['first_serve_points_won'].shape[0] / player_data[Players.PLAYER_2.value]['first_serves'].shape[0]) * 100), 1) if player_data[Players.PLAYER_2.value]['first_serves'].shape[0] > 0 else '-',
            "%"
        )

        add_stat(
            "Second Serve Win %",
            round(((player_data[Players.PLAYER_1.value]['second_serve_points_won'].shape[0] / player_data[Players.PLAYER_1.value]['second_serves'].shape[0]) * 100), 1) if player_data[Players.PLAYER_1.value]['second_serves'].shape[0] > 0 else '-',
            round(((player_data[Players.PLAYER_2.value]['second_serve_points_won'].shape[0] / player_data[Players.PLAYER_2.value]['second_serves'].shape[0]) * 100), 1) if player_data[Players.PLAYER_2.value]['second_serves'].shape[0] > 0 else '-',
            "%"
        )

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
            round(((player_data[Players.PLAYER_1.value]['net_approach_points_won'].shape[0] / player_data[Players.PLAYER_1.value]['net_approach_points'].shape[0]) * 100), 1) if player_data[Players.PLAYER_1.value]['net_approach_points'].shape[0] > 0 else '-',
            round(((player_data[Players.PLAYER_2.value]['net_approach_points_won'].shape[0] / player_data[Players.PLAYER_2.value]['net_approach_points'].shape[0]) * 100), 1) if player_data[Players.PLAYER_2.value]['net_approach_points'].shape[0] > 0 else '-',
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

            serve_data = analysis_match_data[analysis_match_data['server'] == analysis_player_filter]

            serve_left, serve_right = st.columns(2)

            serve_map = {
                Serve.ACE.value: "Ace",
                Serve.FIRST_SERVE.value: "First Serve",
                Serve.SECOND_SERVE.value: "Second Serve",
            }
            serve_filter = serve_right.selectbox(
                "Select Serve ",
                options=serve_map.keys(),
                format_func=lambda val: serve_map[val],
                key='serve_filter',
            )

            try:
                serve_fig, (serve_ax, serve_hm_ax) = plt.subplots(1, 2)

                serve_ax.set_facecolor('#0d0e12')

                # pie chart
                serve_ax.pie(
                    [serve_data[serve_data['serve'] == enum.value].shape[0] for enum in Serve],
                    explode=(0.1, 0.1, 0.1, 0.1),
                    labels=("Ace", "First Serve", "Second Serve", "Double Fault"),
                    autopct='%1.1f%%',
                    shadow=True,
                    startangle=90,
                    colors=plt.cm.Pastel1.colors,
                )

                # heat map
                serve_hm_data = [[serve_data[(serve_data['serve'] == serve_filter) & (serve_data['serve_type'] == serve_type.value) & (serve_data['serve_target'] == serve_target.value)].shape[0] for serve_target in ServeTarget] for serve_type in ServeType]
                serve_targets = ["Inside", "Body", "Outside", "Short"]
                serve_types = ["Flat", "Kick", "Slice", "Underarm"]

                im = serve_hm_ax.imshow(
                    serve_hm_data,
                    cmap='Wistia',
                )

                serve_hm_ax.set_xticks(
                    range(len(serve_targets)),
                    labels=serve_targets,
                    rotation=45,
                    ha="right",
                    rotation_mode="anchor",
                )
                serve_hm_ax.set_yticks(
                    range(len(serve_types)),
                    labels=serve_types,
                )

                for i in range(len(serve_types)):
                    for j in range(len(serve_targets)):
                        text = serve_hm_ax.text(
                            j,
                            i,
                            serve_hm_data[i][j],
                            ha="center",
                            va="center",
                            color="k",
                        )

                st.pyplot(
                    serve_fig,
                    facecolor='#0F1116'
                )
            except:
                st.warning("There is no relevant match data to analyse.")

        with st.container():
            st.subheader("Net")

            # TODO: Breakdown by percentage of service points that go to net. Radial bars.

            try:
                net_fig, (net_rb_ax, net_ax) = plt.subplots(1, 2)

                net_x_labels = ("Aggressive", "Forced")

                net_server_data = analysis_match_data[analysis_match_data['server'] == analysis_player_filter]
                net_returner_data = analysis_match_data[analysis_match_data['server'] == other_player(analysis_player_filter)]
                net_data = {
                    'Server': [net_server_data[net_server_data.net_approach_type == enum.value].shape[0] for enum in NetApproachType],
                    'Returner': [net_returner_data[net_server_data.net_approach_type == enum.value].shape[0] for enum in NetApproachType],
                }

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

            # rp_data = [
            #     analysis_match_data[(analysis_match_data['server'] == analysis_player_filter) & (analysis_match_data['net_approach'] == True)].shape[0],
            #     analysis_match_data[(analysis_match_data['server'] == other_player(analysis_player_filter)) & (analysis_match_data['net_approach'] == True)].shape[0]
            # ]

            rp_data = [23.6, 9.4]

            rp_fig = plt.figure()

            ax_polar_bg = rp_fig.add_axes((1.0, 1.0, 1.0, 1.0), polar=True, frameon=False)
            ax_polar_bg.set_theta_zero_location('N')
            ax_polar_bg.set_theta_direction(-1)

            for i in range(len(rp_data)):
                ax_polar_bg.barh(
                    i, 100*2*np.pi/100,
                    color='grey',
                    alpha=0.1
            )
            ax_polar_bg.axis('off')

            ax_polar = rp_fig.add_axes((1.0, 1.0, 1.0, 1.0), polar=True, frameon=False)
            ax_polar.set_theta_zero_location('N')
            ax_polar.set_theta_direction(-1)
            ax_polar.set_rgrids(
                [0, 1],
                labels=["server", "returner"],
                angle=0,
                fontsize=10,
                color='black',
                verticalalignment='center'
            )

            for i in range(len(rp_data)):
                ax_polar.barh(
                    i,
                    rp_data[i]*2*np.pi/100,
                    color=plt.cm.Pastel1.colors[i]
                )

            ax_polar.grid(False)
            ax_polar.tick_params(
                axis='both',
                left=False,
                bottom=False,
                labelbottom=False,
                labelleft=True
            )

            st.pyplot(rp_fig)

        with st.container():
            st.subheader("Rally Length")

            st.write(f"Rally length of points when {player_map[analysis_player_filter]} is serving.")

            rally_length_server_data = analysis_match_data[analysis_match_data.server == analysis_player_filter]
            rally_length_data = [rally_length_server_data[rally_length_server_data.rally_length == enum.value].shape[0] for enum in RallyLength]

            rally_length_fig, rally_length_ax = plt.subplots()
            rally_length_ax.bar(("0-1", "2-4", "5-8", "9+"), rally_length_data)

            st.pyplot(rally_length_fig)

        with st.container():
            st.subheader("Winners & Errors")

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

            # TODO: Add filter for hand.

            winerr_fig, winerr_ax = plt.subplots()

            # heat map
            winerr_hm_data = [
                [fs_winner_data[fs_winner_data['final_shot_type'] == fs_type.value].shape[0] for fs_type in FinalShotType],
                [fs_error_data[fs_error_data['final_shot_type'] == fs_type.value].shape[0] for fs_type in FinalShotType],
                [fs_unforced_error_data[fs_unforced_error_data['final_shot_type'] == fs_type.value].shape[0] for fs_type in FinalShotType],
            ]
            winerr = ["Winner", "Error", "Unforced Error"]
            winerr_types = ["Drive", "Smash", "Volley", "Drop Shot", "Lob", "Other"]

            im = winerr_ax.imshow(
                winerr_hm_data,
                cmap='Wistia',
            )

            winerr_ax.set_xticks(
                range(len(winerr_types)),
                labels=winerr_types,
                rotation=45,
                ha="right",
                rotation_mode="anchor",
            )
            winerr_ax.set_yticks(
                range(len(winerr)),
                labels=winerr,
            )

            for i in range(len(winerr)):
                for j in range(len(winerr_types)):
                    text = winerr_ax.text(
                        j,
                        i,
                        winerr_hm_data[i][j],
                        ha="center",
                        va="center",
                        color="k",
                    )

            st.pyplot(winerr_fig)

    with st.container():
        st.write("###")
        st.divider()
        left, right = st.columns(2)
        if left.button("Continue Tracking Current Match"):
            switch_page("Track Match")
        if right.button("Load Another Match"):
            switch_page("Load Match")
