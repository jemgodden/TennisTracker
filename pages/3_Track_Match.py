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
    )

    st.title("Track Current Match :memo:")

    with st.container(key="scoreboard"):
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

    with st.container(key="point_form"):
        st.header("Current Point")

        left, middle, right = st.columns(3)

        if left.button("Ace - Inside (Flat)"):
            add_ace(st.session_state, ServeTarget.INSIDE.value)
            st.session_state['match'].add_point(st.session_state['match'].current_server)
            st.rerun()

        if middle.button("Ace - Outside (Flat)"):
            add_ace(st.session_state, ServeTarget.OUTSIDE.value)
            st.session_state['match'].add_point(st.session_state['match'].current_server)
            st.rerun()

        if right.button("Double Fault"):
            add_double_fault(st.session_state)
            st.session_state['match'].add_point(other_player(st.session_state['match'].current_server))
            st.rerun()

        st.caption("Quick-press buttons to mark the point as an ace (on first serve) or double fault, without having to submit the point below.")

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

            serve_map = {enum.value: format_enum_name(enum.name) for enum in Serve}
            serve = serve_form_left.pills(
                "Serve",
                options=serve_map.keys(),
                format_func=lambda val: serve_map[val],
                selection_mode="single",
                key='serve',
                default=Serve.FIRST_SERVE.value,
            )

            serve_type_map = {enum.value: format_enum_name(enum.name) for enum in ServeType}
            serve_type = serve_form_middle.pills(
                "Serve Type",
                options=serve_type_map.keys(),
                format_func=lambda val: serve_type_map[val],
                selection_mode="single",
                key='serve_type',
            )

            serve_target_map = {enum.value: format_enum_name(enum.name) for enum in ServeTarget}
            serve_target = serve_form_right.pills(
                "Serve Target",
                options=serve_target_map.keys(),
                format_func=lambda val: serve_target_map[val],
                selection_mode="single",
                key='serve_target',
            )

            st.subheader("Rally")

            st.write("#### Net")

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

            nat_approach_map = {enum.value: format_enum_name(enum.name) for enum in NetApproachType}
            net_approach_type = net_form_right.pills(
                "Net Approach Type",
                options=nat_approach_map.keys(),
                format_func=lambda val: nat_approach_map[val],
                selection_mode="single",
                key='net_approach_type',
            )

            st.write("#### Length")

            rally_length_map = {enum.value: format_enum_name(enum.name, True) for enum in RallyLength}
            rally_length = st.pills(
                "Rally Length",
                options=rally_length_map.keys(),
                format_func=lambda val: rally_length_map[val],
                selection_mode="single",
                key='rally_length',
            )

            st.subheader("Point End")

            fs_form_left, fs_form_middle, fs_form_right = st.columns(3)

            final_shot_map = {enum.value: format_enum_name(enum.name) for enum in FinalShot}
            final_shot = fs_form_left.pills(
                "Final Shot",
                options=final_shot_map.keys(),
                format_func=lambda val: final_shot_map[val],
                selection_mode="single",
                key='final_shot',
            )

            final_shot_hand_map = {enum.value: format_enum_name(enum.name) for enum in FinalShotHand}
            final_shot_hand = fs_form_middle.pills(
                "Final Shot Type",
                options=final_shot_hand_map.keys(),
                format_func=lambda val: final_shot_hand_map[val],
                selection_mode="single",
                key='final_shot_hand',
            )

            final_shot_type_map = {enum.value: format_enum_name(enum.name) for enum in FinalShotType}
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

    with st.container(key="save_data"):
        st.header("Save Match")

        output_file_name = st.text_input(
            "Output File Name",
            value=f"{st.session_state['match'].player1_name.replace(' ', '_')}_vs_{st.session_state['match'].player2_name.replace(' ', '_')}-{st.session_state['match_datetime'].strftime('%Y-%m-%d_%H:%M:%S')}"
        )

        st.caption("Press enter in above text box to ensure the file name is saved.")

        st.download_button(
            label="Download Match Data to CSV",
            data=st.session_state['match_data'].to_csv(index=False).encode("utf-8"),
            file_name=f"{output_file_name}.csv",
            mime="text/csv",
            disabled=st.session_state['match_data'].empty  # Do not allow saving if no data has yet been inputted.
        )

    with st.container(key="page_navigation"):
        st.write("###")
        st.divider()
        if st.button("Analyse Current Match"):
            switch_page("Analyse Match")
