import pandas as pd
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
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
    )

    st.title("Analysis :chart_with_upwards_trend:")

    with st.container(key="match_information"):
        st.header(f"Match: {st.session_state['player1_name']} vs {st.session_state['player2_name']}")
        st.subheader(f"Played: {st.session_state['match_datetime'].strftime('%d/%m/%Y %H:%M:%S')}")

    # with st.container(key="show_data"):
    #     st.write("######")
    #     if st.toggle("Show Data"):
    #         st.dataframe(st.session_state['match_data'])
    #     st.caption("Only intended for developer use.")

    if st.session_state['match_data'].empty:
        st.warning("There is no match data to analyse.")
        st.stop()

    with st.container(key="overview"):
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

        def add_stat(title: str, player1_val: str, player2_val: str):
            overview_body_left.markdown(f"<h6 style='text-align: center;'>{player1_val}</h6>", unsafe_allow_html=True)
            overview_body_middle.markdown(f"<h6 style='text-align: center;'>{title}</h6>", unsafe_allow_html=True)
            overview_body_right.markdown(f"<h6 style='text-align: center;'>{player2_val}</h6>", unsafe_allow_html=True)

        add_stat(
            "Points Won",
            str(player_data[Players.PLAYER_1.value]['points_won'].shape[0]),
            str(player_data[Players.PLAYER_2.value]['points_won'].shape[0])
        )

        add_stat(
            "Break Points",
            f"{player_data[Players.PLAYER_1.value]['break_points_won'].shape[0]}/{player_data[Players.PLAYER_1.value]['break_points'].shape[0]}",
            f"{player_data[Players.PLAYER_2.value]['break_points_won'].shape[0]}/{player_data[Players.PLAYER_2.value]['break_points'].shape[0]}",
        )

        add_stat(
            "Set Points",
            f"{player_data[Players.PLAYER_1.value]['set_points_won'].shape[0]}/{player_data[Players.PLAYER_1.value]['set_points'].shape[0]}",
            f"{player_data[Players.PLAYER_2.value]['set_points_won'].shape[0]}/{player_data[Players.PLAYER_2.value]['set_points'].shape[0]}",
        )

        add_stat(
            "Match Points",
            f"{player_data[Players.PLAYER_1.value]['match_points_won'].shape[0]}/{player_data[Players.PLAYER_1.value]['match_points'].shape[0]}",
            f"{player_data[Players.PLAYER_2.value]['match_points_won'].shape[0]}/{player_data[Players.PLAYER_2.value]['match_points'].shape[0]}",
        )

        add_stat(
            "Aces",
            str(player_data[Players.PLAYER_1.value]['aces'].shape[0]),
            str(player_data[Players.PLAYER_2.value]['aces'].shape[0])
        )

        add_stat(
            "Double Faults",
            str(player_data[Players.PLAYER_1.value]['double_faults'].shape[0]),
            str(player_data[Players.PLAYER_2.value]['double_faults'].shape[0])
        )

        add_stat(
            "First Serve %",
            f"{((player_data[Players.PLAYER_1.value]['first_serves'].shape[0] / player_data[Players.PLAYER_1.value]['serves'].shape[0]) * 100):.1f}%" if player_data[Players.PLAYER_1.value]['serves'].shape[0] > 0 else '-',
            f"{((player_data[Players.PLAYER_2.value]['first_serves'].shape[0] / player_data[Players.PLAYER_2.value]['serves'].shape[0]) * 100):.1f}%" if player_data[Players.PLAYER_2.value]['serves'].shape[0] > 0 else '-'
        )

        add_stat(
            "Serve Win %",
            f"{((player_data[Players.PLAYER_1.value]['serve_points_won'].shape[0] / player_data[Players.PLAYER_1.value]['serves'].shape[0]) * 100):.1f}%" if player_data[Players.PLAYER_1.value]['first_serves'].shape[0] > 0 else '-',
            f"{((player_data[Players.PLAYER_2.value]['serve_points_won'].shape[0] / player_data[Players.PLAYER_2.value]['serves'].shape[0]) * 100):.1f}%" if player_data[Players.PLAYER_2.value]['first_serves'].shape[0] > 0 else '-'
        )

        add_stat(
            "First Serve Win %",
            f"{((player_data[Players.PLAYER_1.value]['first_serve_points_won'].shape[0] / player_data[Players.PLAYER_1.value]['first_serves'].shape[0]) * 100):.1f}%" if player_data[Players.PLAYER_1.value]['first_serves'].shape[0] > 0 else '-',
            f"{((player_data[Players.PLAYER_2.value]['first_serve_points_won'].shape[0] / player_data[Players.PLAYER_2.value]['first_serves'].shape[0]) * 100):.1f}%" if player_data[Players.PLAYER_2.value]['first_serves'].shape[0] > 0 else '-'
        )

        add_stat(
            "Second Serve Win %",
            f"{((player_data[Players.PLAYER_1.value]['second_serve_points_won'].shape[0] / player_data[Players.PLAYER_1.value]['second_serves'].shape[0]) * 100):.1f}%" if player_data[Players.PLAYER_1.value]['second_serves'].shape[0] > 0 else '-',
            f"{((player_data[Players.PLAYER_2.value]['second_serve_points_won'].shape[0] / player_data[Players.PLAYER_2.value]['second_serves'].shape[0]) * 100):.1f}%" if player_data[Players.PLAYER_2.value]['second_serves'].shape[0] > 0 else '-',
        )

        add_stat(
            "Winners",
            str(player_data[Players.PLAYER_1.value]['winners'].shape[0]),
            str(player_data[Players.PLAYER_2.value]['winners'].shape[0])
        )

        add_stat(
            "Errors",
            str(player_data[Players.PLAYER_1.value]['errors'].shape[0]),
            str(player_data[Players.PLAYER_2.value]['errors'].shape[0])
        )

        add_stat(
            "Unforced Errors",
            str(player_data[Players.PLAYER_1.value]['unforced_errors'].shape[0]),
            str(player_data[Players.PLAYER_2.value]['unforced_errors'].shape[0])
        )

        add_stat(
            "Net Approach %",
            f"{((player_data[Players.PLAYER_1.value]['net_approach_points'].shape[0] / player_data[Players.PLAYER_1.value]['all_points'].shape[0]) * 100):.1f}%" if player_data[Players.PLAYER_1.value]['all_points'].shape[0] > 0 else '-',
            f"{((player_data[Players.PLAYER_2.value]['net_approach_points'].shape[0] / player_data[Players.PLAYER_2.value]['all_points'].shape[0]) * 100):.1f}%" if player_data[Players.PLAYER_2.value]['all_points'].shape[0] > 0 else '-',
        )

        add_stat(
            "Net Approach Win %",
            f"{((player_data[Players.PLAYER_1.value]['net_approach_points_won'].shape[0] / player_data[Players.PLAYER_1.value]['net_approach_points'].shape[0]) * 100):.1f}%" if player_data[Players.PLAYER_1.value]['net_approach_points'].shape[0] > 0 else '-',
            f"{((player_data[Players.PLAYER_2.value]['net_approach_points_won'].shape[0] / player_data[Players.PLAYER_2.value]['net_approach_points'].shape[0]) * 100):.1f}%" if player_data[Players.PLAYER_2.value]['net_approach_points'].shape[0] > 0 else '-',
        )

    with st.container(key="analysis"):
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

        with st.container(key="serve_analysis"):
            st.subheader("Serve")

            serve_data = analysis_match_data[analysis_match_data['server'] == analysis_player_filter]

            serve_analysis_left, serve_analysis_right = st.columns(2, vertical_alignment='center')

            try:
                serve_pie_fig, serve_pie_ax = plt.subplots()

                serve_pie_data = []
                serve_pie_labels = []
                for enum in Serve:
                    enum_count = serve_data[serve_data['serve'] == enum.value].shape[0]
                    if enum_count > 0:
                        serve_pie_data.append(enum_count)
                        serve_pie_labels.append(format_enum_name(enum.name))

                # pie chart
                serve_pie_ax.pie(
                    serve_pie_data,
                    explode=[0.1 for _ in serve_pie_data],
                    labels=serve_pie_labels,
                    autopct='%1.1f%%',
                    shadow=True,
                    startangle=90,
                    colors=plt.cm.Set3.colors,
                )

                serve_pie_ax.set_title(f"Serve Percentages for {player_map[analysis_player_filter]}")

                serve_analysis_left.pyplot(
                    serve_pie_fig,
                    facecolor='#0F1116',
                )
            except:
                serve_analysis_left.warning("There is no relevant match data to analyse.")

            try:
                serve_map = {enum.value: format_enum_name(enum.name) for enum in Serve}
                serve_map.pop(Serve.DOUBLE_FAULT.value)
                serve_filter = serve_analysis_right.selectbox(
                    "Select Serve to Show on Heatmap",
                    options=serve_map.keys(),
                    format_func=lambda val: serve_map[val],
                    key='serve_filter',
                )

                serve_hm_fig, serve_hm_ax = plt.subplots()

                serve_hm_data = [[serve_data[(serve_data['serve'] == serve_filter) & (serve_data['serve_type'] == serve_type.value) & (serve_data['serve_target'] == serve_target.value)].shape[0] for serve_target in ServeTarget] for serve_type in ServeType]
                serve_targets = [format_enum_name(enum.name) for enum in ServeTarget]
                serve_types = [format_enum_name(enum.name) for enum in ServeType]

                im = serve_hm_ax.imshow(
                    serve_hm_data,
                    cmap='YlGn',
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

                serve_hm_ax.set_title(f"Serve Types & Targets by Serve for {player_map[analysis_player_filter]}")

                serve_analysis_right.pyplot(
                    serve_hm_fig,
                    facecolor='#0F1116',
                )
            except:
                serve_analysis_right.warning("There is no relevant match data to analyse.")

        with st.container(key="net_analysis"):
            st.subheader("Net")

            net_analysis_left, net_analysis_right = st.columns(2, vertical_alignment='center')

            try:
                rp_data = [
                    0,
                    analysis_match_data[(analysis_match_data['server'] == other_player(analysis_player_filter)) & (analysis_match_data['first_net_approacher'] == analysis_player_filter)].shape[0] * 100 / analysis_match_data[analysis_match_data['server'] == other_player(analysis_player_filter)].shape[0] if analysis_match_data[analysis_match_data['server'] == other_player(analysis_player_filter)].shape[0] > 0 else 0,
                    analysis_match_data[(analysis_match_data['server'] == analysis_player_filter) & (analysis_match_data['first_net_approacher'] == analysis_player_filter)].shape[0] * 100 / analysis_match_data[analysis_match_data['server'] == analysis_player_filter].shape[0] if analysis_match_data[analysis_match_data['server'] == analysis_player_filter].shape[0] > 0 else 0
                ]

                rp_bg_data = [0, 1, 1]
                rp_labels = ["", "Returner", "Server"]

                net_rb_fig = plt.figure()

                net_rb_bg_polar_ax = net_rb_fig.add_axes((1.0, 1.0, 1.0, 1.0), polar=True, frameon=False)
                net_rb_bg_polar_ax.set_theta_zero_location('N')
                net_rb_bg_polar_ax.set_theta_direction(-1)

                for i in range(len(rp_data)):
                    net_rb_bg_polar_ax.barh(
                        i,
                        rp_bg_data[i]*2*np.pi,
                        color='grey',
                        alpha=0.1,
                    )
                net_rb_bg_polar_ax.axis('off')

                net_rb_polar_ax = net_rb_fig.add_axes((1.0, 1.0, 1.0, 1.0), polar=True, frameon=False)
                net_rb_polar_ax.set_theta_zero_location('N')
                net_rb_polar_ax.set_theta_direction(-1)
                net_rb_polar_ax.set_rgrids(
                    [0, 1, 2],
                    labels=[""] + [f"{val:.1f}%" for val in rp_data[1:]],
                    angle=0,
                    fontsize=12,
                    fontweight='bold',
                    color='black',
                    verticalalignment='center',
                )

                rb_color_map = plt.cm.Set3.colors[:3][::-1]
                for i in range(len(rp_data)):
                    net_rb_polar_ax.barh(
                        i,
                        rp_data[i]*2*np.pi/100,
                        color=rb_color_map[i],
                        label=rp_labels[i],
                    )

                net_rb_polar_ax.grid(False)
                net_rb_polar_ax.tick_params(
                    axis='both',
                    left=False,
                    bottom=False,
                    labelbottom=False,
                    labelleft=True,
                )

                handles, labels = net_rb_polar_ax.get_legend_handles_labels()
                net_rb_polar_ax.legend(handles[::-1], labels[::-1], loc='upper left')
                net_rb_polar_ax.set_title(f"Net Approach by Service for {player_map[analysis_player_filter]}")

                net_analysis_left.pyplot(
                    net_rb_fig,
                    facecolor='#0F1116',
                )
            except:
                net_analysis_left.warning("There is no relevant match data to analyse.")

            try:
                net_server_data = analysis_match_data[analysis_match_data['server'] == analysis_player_filter]
                net_returner_data = analysis_match_data[analysis_match_data['server'] == other_player(analysis_player_filter)]
                net_data = {
                    'Server': [net_server_data[net_server_data.net_approach_type == enum.value].shape[0] for enum in NetApproachType],
                    'Returner': [net_returner_data[net_returner_data.net_approach_type == enum.value].shape[0] for enum in NetApproachType],
                }

                net_x_labels = [format_enum_name(enum.name) for enum in NetApproachType]

                net_bar_fig, net_bar_ax = plt.subplots()

                net_x = np.arange(len(net_x_labels))  # the label locations
                net_width = 0.4  # width of the bars
                net_multiplier = 0

                for net_attribute, net_measurement in net_data.items():
                    net_offset = net_width * net_multiplier
                    net_rects = net_bar_ax.bar(net_x + net_offset, net_measurement, net_width, label=net_attribute)
                    net_bar_ax.bar_label(net_rects, padding=3)
                    net_multiplier += 1

                net_bar_ax.set_xticks(net_x + (net_width / 2), net_x_labels)
                net_bar_ax.yaxis.set_major_locator(MaxNLocator(integer=True))
                net_bar_ax.legend(loc='upper right')
                net_bar_ax.set_title(f"Net Approach Counts by Type and Service for {player_map[analysis_player_filter]}")

                net_analysis_right.pyplot(
                    net_bar_fig,
                    facecolor='#0F1116',
                )
            except:
                net_analysis_right.warning("There is no relevant match data to analyse.")

        with st.container(key="rally_analysis"):
            st.subheader("Rally Length")

            rally_analysis_left, rally_analysis_right = st.columns(2, vertical_alignment='center')

            rally_length_x_labels = [format_enum_name(enum.name, True) for enum in RallyLength]

            try:
                rally_length_server_data = analysis_match_data[analysis_match_data.server == analysis_player_filter]
                rally_length_data = [rally_length_server_data[rally_length_server_data.rally_length == enum.value].shape[0] for enum in RallyLength]

                rally_length_serve_fig, rally_length_serve_ax = plt.subplots()

                rally_length_serve_ax.bar(
                    rally_length_x_labels,
                    rally_length_data,
                    color=plt.cm.Set3.colors,
                )

                rally_length_serve_ax.yaxis.set_major_locator(MaxNLocator(integer=True))
                rally_length_serve_ax.set_title(f"Count of Rally Lengths When {player_map[analysis_player_filter]} is Serving")

                rally_analysis_left.pyplot(
                    rally_length_serve_fig,
                    facecolor='#0F1116',
                )
            except:
                rally_analysis_left.warning("There is no relevant match data to analyse.")

            try:
                rally_length_all_data = [analysis_match_data[analysis_match_data.rally_length == enum.value].shape[0] for enum in RallyLength]
                rally_length_all_win_data = [analysis_match_data[(analysis_match_data.winner == analysis_player_filter) & (analysis_match_data.rally_length == enum.value)].shape[0] for enum in RallyLength]
                rally_length_all_win_labels = [f"{((win_count/all_count)*100):.1f}%" for (win_count, all_count) in zip(rally_length_all_win_data, rally_length_all_data)]

                rally_length_all_fig, rally_length_all_ax = plt.subplots()

                rally_length_all_ax.bar(
                    rally_length_x_labels,
                    rally_length_all_data,
                    color='dimgrey',
                )

                vbar = rally_length_all_ax.bar(
                    rally_length_x_labels,
                    rally_length_all_win_data,
                    color=plt.cm.Set3.colors,
                )

                def add_labels(ax: plt.Axes, x: list[str], y: list[int], text_label: list[str]):
                    for i in range(len(x)):
                        ax.text(i, y[i]//2, text_label[i], ha='center', color='k')

                add_labels(rally_length_all_ax, rally_length_x_labels, rally_length_all_win_data, rally_length_all_win_labels)

                rally_length_all_ax.yaxis.set_major_locator(MaxNLocator(integer=True))
                rally_length_all_ax.set_title(f"Points Won by Rally Length for {player_map[analysis_player_filter]}")

                rally_analysis_right.pyplot(
                    rally_length_all_fig,
                    facecolor='#0F1116',
                )
            except:
                rally_analysis_right.warning("There is no relevant match data to analyse.")

        with st.container(key="final_shot_analysis"):
            st.subheader("Winners & Errors")

            fs_analysis_left, fs_analysis_right = st.columns(2, vertical_alignment='center')

            fs_winner_data = analysis_match_data[
                (analysis_match_data['winner'] == analysis_player_filter)
                & (analysis_match_data['final_shot'] == FinalShot.WINNER.value)
            ]
            fs_error_data = analysis_match_data[
                (analysis_match_data['winner'] == other_player(analysis_player_filter))
                & (analysis_match_data['final_shot'] == FinalShot.ERROR.value)
            ]
            fs_unforced_error_data = analysis_match_data[
                (analysis_match_data['winner'] == other_player(analysis_player_filter))
                & (analysis_match_data['final_shot'] == FinalShot.UNFORCED_ERROR.value)
            ]

            winerr_data_map = {
                FinalShot.WINNER.value: fs_winner_data,
                FinalShot.ERROR.value: fs_error_data,
                FinalShot.UNFORCED_ERROR.value: fs_unforced_error_data,
            }

            try:
                fs_x_labels = [format_enum_name(enum.name) for enum in FinalShot]

                fs_mbar_data = {
                    format_enum_name(FinalShotHand.FOREHAND.name): [
                        fs_winner_data[fs_winner_data['final_shot_hand'] == FinalShotHand.FOREHAND.value].shape[0],
                        fs_error_data[fs_error_data['final_shot_hand'] == FinalShotHand.FOREHAND.value].shape[0],
                        fs_unforced_error_data[fs_unforced_error_data['final_shot_hand'] == FinalShotHand.FOREHAND.value].shape[0],
                    ],
                    format_enum_name(FinalShotHand.BACKHAND.name): [
                        fs_winner_data[fs_winner_data['final_shot_hand'] == FinalShotHand.BACKHAND.value].shape[0],
                        fs_error_data[fs_error_data['final_shot_hand'] == FinalShotHand.BACKHAND.value].shape[0],
                        fs_unforced_error_data[fs_unforced_error_data['final_shot_hand'] == FinalShotHand.BACKHAND.value].shape[0],
                    ],
                    format_enum_name(FinalShotHand.OTHER.name): [
                        fs_winner_data[fs_winner_data['final_shot_hand'] == FinalShotHand.OTHER.value].shape[0],
                        fs_error_data[fs_error_data['final_shot_hand'] == FinalShotHand.OTHER.value].shape[0],
                        fs_unforced_error_data[fs_unforced_error_data['final_shot_hand'] == FinalShotHand.OTHER.value].shape[0],
                    ],
                }

                fs_mbar_fig, fs_mbar_ax = plt.subplots()

                fs_x = np.arange(len(fs_x_labels))  # the label locations
                fs_width = 0.25  # width of the bars
                fs_multiplier = 0

                for fs_attribute, fs_measurement in fs_mbar_data.items():
                    fs_offset = fs_width * fs_multiplier
                    fs_rects = fs_mbar_ax.bar(fs_x + fs_offset, fs_measurement, fs_width, label=fs_attribute)
                    fs_mbar_ax.bar_label(fs_rects, padding=3)
                    fs_multiplier += 1

                fs_mbar_ax.set_xticks(fs_x + fs_width, fs_x_labels)
                fs_mbar_ax.yaxis.set_major_locator(MaxNLocator(integer=True))
                fs_mbar_ax.legend(loc='upper right')
                fs_mbar_ax.set_title(f"Counts of Winners & Errors for {player_map[analysis_player_filter]}")

                fs_analysis_left.pyplot(
                    fs_mbar_fig,
                    facecolor='#0F1116',
                )
            except:
                fs_analysis_left.warning("There is no relevant match data to analyse.")

            try:
                winerr_map = {enum.value: format_enum_name(enum.name) for enum in FinalShot}
                winerr_filter = fs_analysis_right.selectbox(
                    "Select Winners or Errors",
                    options=winerr_map.keys(),
                    format_func=lambda val: winerr_map[val],
                    key='winerr_filter',
                )

                winerr_data = winerr_data_map[winerr_filter]

                fs_sbar_fig, fs_sbar_ax = plt.subplots()

                shot_types = [format_enum_name(enum.name) for enum in FinalShotType]
                fs_sbar_data = {
                    format_enum_name(FinalShotHand.FOREHAND.name): [winerr_data[(winerr_data['final_shot_hand'] == FinalShotHand.FOREHAND.value) & (winerr_data['final_shot_type'] == enum.value)].shape[0] for enum in FinalShotType],
                    format_enum_name(FinalShotHand.BACKHAND.name): [winerr_data[(winerr_data['final_shot_hand'] == FinalShotHand.BACKHAND.value) & (winerr_data['final_shot_type'] == enum.value)].shape[0] for enum in FinalShotType],
                    format_enum_name(FinalShotHand.OTHER.name): [winerr_data[(winerr_data['final_shot_hand'] == FinalShotHand.OTHER.value) & (winerr_data['final_shot_type'] == enum.value)].shape[0] for enum in FinalShotType],
                }
                base = [0 for shot_type in shot_types]

                for label, vals in fs_sbar_data.items():
                    p = fs_sbar_ax.bar(shot_types, vals, 0.75, label=label, bottom=base)
                    base = [sum(i) for i in zip(base, vals)]

                fs_sbar_ax.yaxis.set_major_locator(MaxNLocator(integer=True))
                fs_sbar_ax.legend(loc="upper right")
                fs_sbar_ax.set_title(f"Count of Types of Winners & Errors by Shot for {player_map[analysis_player_filter]}")

                fs_analysis_right.pyplot(
                    fs_sbar_fig,
                    facecolor='#0F1116',
                )
            except:
                fs_analysis_right.warning("There is no relevant match data to analyse.")

    with st.container(key="page_navigation"):
        st.write("###")
        st.divider()
        left, right = st.columns(2)
        if left.button("Continue Tracking Current Match"):
            switch_page("Track Match")
        if right.button("Load Another Match"):
            switch_page("Load Match")
