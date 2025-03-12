from datetime import datetime, timezone
import pandas as pd
import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from src.utils import *
from src.tennis import Match, MatchSections


# Application page - 'New Match':
# Let user set match parameters for a new match and generate appropriate session state variables.
# Display the scoreboard for the current match.
# Let the user add points to the match using the current point form, which sends data to the backend and updates scoreboard.
# Let the user save the match data csv file to be used and analysed later.


if __name__ == "__main__":

    st.set_page_config(
        page_title="New Match",
        # initial_sidebar_state="collapsed",
    )

    st.title("Track a New Match")

    with st.container():
        st.header("Match Settings")

        st.markdown(
            """
            Default match settings are:
            - Best of three sets.
            - First to 6 games, being at least 2 ahead, to win a set. Tiebreaker game done at 6 games all.
            - Final deciding set is not a tiebreak.
            """
        )

        st.caption("Note that changing the match settings will reset any previously entered match, point or scoreboard data.  \nConsider saving the file first.")

        if st.toggle("Open Match Settings"):
            player1_name = st.text_input(
                "Player 1 Name",
                placeholder="Player 1",
                max_chars=25,
                key='player1_name',  # key parameter used to set the output of this widget as a session state variable.
            )

            player2_name = st.text_input(
                "Player 2 Name",
                placeholder="Player 2",
                max_chars=25,
                key='player2_name',
            )

            server = st.pills(
                "Server (Defaults to Player 1)",
                options=[1, 2],
                selection_mode="single",
            )

            sets = st.number_input(
                "Best of # Sets",
                min_value=1,
                max_value=5,
                value=3,
                step=2
            )

            games = st.number_input(
                "Number of Games to Win Set",
                min_value=2,
                max_value=6,
                value=6
            )

            set_tiebreak_to = st.number_input(
                "Number of Points to Win Set Tiebreak",
                min_value=3,
                max_value=11,
                value=7
            )

            final_set_tiebreak = st.checkbox("Final Set Tiebreak?")

            final_set_tiebreak_to = st.number_input(
                "Number of Points to Win Final Set Tiebreak",
                min_value=3,
                max_value=21,
                value=10
            )

            if st.button("Confirm Match Details"):
                st.session_state['match'] = Match(
                    player1_name=player1_name if player1_name else 'Player 1',
                    player2_name=player2_name if player2_name else 'Player 2',
                    server=server if server else Players.PLAYER_1.value,
                    match_best_of=sets,
                    set_num_games=games,
                    game_tiebreak_to=set_tiebreak_to,
                    final_set_tiebreak=final_set_tiebreak,
                    set_tiebreak_to=final_set_tiebreak_to
                )
                st.session_state['match_data'] = create_backend_df()
                st.session_state['match_datetime'] = datetime.now(timezone.utc)

    with st.container():
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

    with st.container():
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

            serve_map = {
                Serve.ACE.value: "Ace",
                Serve.FIRST_SERVE.value: "First",
                Serve.SECOND_SERVE.value: "Second",
                Serve.DOUBLE_FAULT.value: "Double Fault",
            }
            serve = st.pills(
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
            serve_type = st.pills(
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
            serve_target = st.pills(
                "Serve Target",
                options=serve_target_map.keys(),
                format_func=lambda val: serve_target_map[val],
                selection_mode="single",
                key='serve_target',
            )

            net_approach = st.checkbox(
                "Net Approach",
                key='net_approach',
            )

            first_net_approacher = st.pills(
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
            net_approach_type = st.pills(
                "Net Approach Type",
                options=nat_approach_map.keys(),
                format_func=lambda val: nat_approach_map[val],
                selection_mode="single",
                key='net_approach_type',
            )

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

            final_shot_map = {
                FinalShot.WINNER.value: "Winner",
                FinalShot.ERROR.value: "Error",
                FinalShot.UNFORCED_ERROR.value: "Unforced Error",
            }
            final_shot = st.pills(
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
            final_shot_hand = st.pills(
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
            final_shot_type = st.pills(
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

            if st.form_submit_button('Add point'):
                if st.session_state['winner'] is None:
                    st.warning("No winner was selected so the point was not added. Please try again.")
                else:
                    add_point(st.session_state)
                    st.session_state['match'].add_point(winner)
                    st.rerun()

    with st.container():
        st.header("Save Match")

        st.download_button(
            label="Download Match Data to CSV",
            data=st.session_state['match_data'].to_csv(index=False).encode("utf-8"),
            # Specific file name used to populate match information when loading the file.
            # TODO: Look into adding meta data to the dataframe or file instead. Then give file naming options.
            file_name=f"{st.session_state['match'].player1_name.replace(' ', '_')}_vs_{st.session_state['match'].player2_name.replace(' ', '_')}-{datetime.now().strftime('%d%m%Y_%H:%M:%S')}.csv",
            mime="text/csv",
            disabled=st.session_state['match_data'].empty  # Do not allow saving if no data has yet been inputted.
        )

    with st.container():
        st.write("###")
        st.divider()
        if st.button("Analyse Match Data"):
            switch_page("Analysis")

