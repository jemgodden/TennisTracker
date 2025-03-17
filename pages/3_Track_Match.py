from datetime import datetime
import pandas as pd
import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from src.utils import *
from src.tennis import MatchSections


# Application page - 'Track Match':
# Display the scoreboard for the current match.
# Let the user add points to the match using the current point form, which sends data to the backend and updates scoreboard.
# Let the user save the match data csv file to be used and analysed later.


if __name__ == "__main__":

    st.set_page_config(
        page_title="Track Match",
        page_icon=":memo:",
        layout='wide',
        # initial_sidebar_state="collapsed",
    )

    st.title("Track Current Match :memo:")

    with st.container("Scoreboard"):
        st.header("Scoreboard")

        scores = st.session_state['match'].get_score()
        scoreboard_df = pd.DataFrame(
            {
                'Player': [st.session_state['match'].player1_name, st.session_state['match'].player2_name],
                'Serve': ['o', ''] if st.session_state['match'].current_server == 1 else ['', 'o'],
                'Sets': scores[MatchSections.SETS.value],
                'Games': scores[MatchSections.GAMES.value],
                'Points': scores[MatchSections.POINTS.value]
            }
        )

        scoreboard_df = scoreboard_df.set_index(scoreboard_df.columns[0])
        scoreboard = st.table(scoreboard_df)

    with st.container("Point Form"):
        st.header("Current Point")

        left, middle, right = st.columns(3)

        if left.button("Ace - Inside"):
            add_ace(st.session_state, ServeTarget.INSIDE.value)
            st.session_state['match'].add_point(st.session_state['match'].current_server)
            st.rerun()

        if middle.button("Ace - Outside"):
            add_ace(st.session_state, ServeTarget.OUTSIDE.value)
            st.session_state['match'].add_point(st.session_state['match'].current_server)
            st.rerun()

        if right.button("Double Fault"):
            add_double_fault(st.session_state)
            st.session_state['match'].add_point(other_player(st.session_state['match'].current_server))
            st.rerun()

        st.caption("Quick-press buttons to mark the point as an ace (assuming serve type is flat) or double fault, without having to submit the point below.")

        with st.form(
                "Point Information",
                clear_on_submit=True,
        ):
            player_map = {
                Players.PLAYER_1.value: st.session_state['match'].player1_name,
                Players.PLAYER_2.value: st.session_state['match'].player2_name,
            }

            st.caption("If any options do not apply to the point then leave them blank/unselected.")

            st.subheader("Serve")

            serve_form_left, serve_form_middle, serve_form_right = st.columns(3)

            serve_map = {
                Serve.ACE.value: "Ace",
                Serve.FIRST_SERVE.value: "First",
                Serve.SECOND_SERVE.value: "Second",
                Serve.DOUBLE_FAULT.value: "Double Fault",
            }
            serve = serve_form_left.pills(
                "Serve",
                options=serve_map.keys(),
                format_func=lambda val: serve_map[val],
                selection_mode="single",
                key='serve',
            )

            serve_type_map = {
                ServeType.FLAT.value: "Flat",
                ServeType.KICK.value: "Kick",
                ServeType.SLICE.value: "Slice",
                ServeType.UNDERARM.value: "Underarm",
            }
            serve_type = serve_form_middle.pills(
                "Serve Type",
                options=serve_type_map.keys(),
                format_func=lambda val: serve_type_map[val],
                selection_mode="single",
                key='serve_type',
            )

            serve_target_map = {
                ServeTarget.INSIDE.value: "Inside",
                ServeTarget.BODY.value: "Body",
                ServeTarget.OUTSIDE.value: "Outside",
                ServeTarget.SHORT.value: "Short",
            }
            serve_target = serve_form_right.pills(
                "Serve Target",
                options=serve_target_map.keys(),
                format_func=lambda val: serve_target_map[val],
                selection_mode="single",
                key='serve_target',
            )

            st.write("######")

            st.subheader("Net")

            net_form_left, net_form_middle, net_form_right = st.columns(3)

            net_approach = net_form_left.checkbox(
                "Net Approach",
                key='net_approach',
            )

            first_net_approacher = net_form_middle.pills(
                "First Net Approacher",
                options=player_map.keys(),
                format_func=lambda player: player_map[player],
                selection_mode="single",
                key='first_net_approacher',
            )

            nat_approach_map = {
                NetApproachType.AGGRESSIVE.value: "Aggressive",
                NetApproachType.FORCED.value: "Forced",
            }
            net_approach_type = net_form_right.pills(
                "Net Approach Type",
                options=nat_approach_map.keys(),
                format_func=lambda val: nat_approach_map[val],
                selection_mode="single",
                key='net_approach_type',
            )

            st.write("######")

            st.subheader("Rally")

            rally_length_map = {
                RallyLength.RL_0_1.value: "0-1",
                RallyLength.RL_2_4.value: "2-4",
                RallyLength.RL_5_8.value: "5-8",
                RallyLength.RL_9_PLUS.value: "9+",
            }
            rally_length = st.pills(
                "Rally Length",
                options=rally_length_map.keys(),
                format_func=lambda val: rally_length_map[val],
                selection_mode="single",
                key='rally_length',
            )

            st.write("######")

            st.subheader("Point End")

            fs_form_left, fs_form_middle, fs_form_right = st.columns(3)

            final_shot_map = {
                FinalShot.WINNER.value: "Winner",
                FinalShot.ERROR.value: "Error",
                FinalShot.UNFORCED_ERROR.value: "Unforced Error",
            }
            final_shot = fs_form_left.pills(
                "Final Shot",
                options=final_shot_map.keys(),
                format_func=lambda val: final_shot_map[val],
                selection_mode="single",
                key='final_shot',
            )

            final_shot_hand_map = {
                FinalShotHand.FOREHAND.value: "Forehand",
                FinalShotHand.BACKHAND.value: "Backhand",
                FinalShotHand.OTHER.value: "Other",
            }
            final_shot_hand = fs_form_middle.pills(
                "Final Shot Type",
                options=final_shot_hand_map.keys(),
                format_func=lambda val: final_shot_hand_map[val],
                selection_mode="single",
                key='final_shot_hand',
            )

            final_shot_type_map = {
                FinalShotType.DRIVE.value: "Drive",
                FinalShotType.VOLLEY.value: "Volley",
                FinalShotType.SMASH.value: "Smash",
                FinalShotType.DROP_SHOT.value: "Drop Shot",
                FinalShotType.LOB.value: "Lob",
                FinalShotType.OTHER.value: "Other",
            }
            final_shot_type = fs_form_right.pills(
                "Final Shot Type",
                options=final_shot_type_map.keys(),
                format_func=lambda val: final_shot_type_map[val],
                selection_mode="single",
                key='final_shot_type',
            )

            # final_shot_spin = st.pills(
            #     "Final Shot Type",
            #     options=["Flat", "Topspin", "Slice", "Other"],
            #     selection_mode="single",
            #     key='final_shot_spin',
            # )

            # final_shot_target = st.pills(
            #     "Final Shot Target",
            #     options=["Inside In", "Inside Out", "Outside Out", "Outside In", "Other"],
            #     selection_mode="single",
            #     key='final_shot_target',
            # )

            winner = st.pills(
                "Winner",
                options=player_map.keys(),
                format_func=lambda player: player_map[player],
                selection_mode="single",
                key='winner',
            )

            st.caption("A winner must be selected in order to add the point.")

            if st.form_submit_button('Add Point'):
                if st.session_state['winner'] is None:
                    st.warning("No winner was selected so the point was not added. Please try again.")
                else:
                    add_point(st.session_state)
                    st.session_state['match'].add_point(winner)
                    st.rerun()

    with st.container("Save Data"):
        st.header("Save Match")

        output_file_name = st.text_input(
            "Output File Name",
            value=f"{st.session_state['match'].player1_name.replace(' ', '_')}_vs_{st.session_state['match'].player2_name.replace(' ', '_')}-{datetime.now().strftime('%d%m%Y_%H:%M:%S')}"
        )

        st.download_button(
            label="Download Match Data to CSV",
            data=st.session_state['match_data'].to_csv(index=False).encode("utf-8"),
            file_name=f"{output_file_name}.csv",
            mime="text/csv",
            disabled=st.session_state['match_data'].empty  # Do not allow saving if no data has yet been inputted.
        )

    with st.container("Page Navigation"):
        st.write("###")
        st.divider()
        if st.button("Analyse Current Match"):
            switch_page("Analyse Match")
