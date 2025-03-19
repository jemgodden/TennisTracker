from datetime import datetime, timezone
import pandas as pd
import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from src.utils import *
from src.tennis import Match


# Application page - 'New Match':
# Let user set match parameters for a new match and generate appropriate session state variables.


if __name__ == "__main__":

    st.set_page_config(
        page_title="New Match",
        page_icon=":tennis:",
        layout='wide',
    )

    st.title("Create a New Match :tennis:")

    with st.container(key="new_match_settings"):
        st.header("Match Settings")

        st.write("The default match settings are the default options in the below inputs.")

        with st.form(
            "Match Information",
            clear_on_submit=True,
        ):
            player1_name = st.text_input(
                "Player 1 Name",
                placeholder="Player 1",
                max_chars=25,
            )

            player2_name = st.text_input(
                "Player 2 Name",
                placeholder="Player 2",
                max_chars=25,
            )

            server = st.pills(
                "Player Starting Server (Defaults to Player 1)",
                options=[Players.PLAYER_1.value, Players.PLAYER_2.value],
                selection_mode="single",
                default=Players.PLAYER_1.value,
            )

            match_best_of = st.number_input(
                "Best of # Sets",
                min_value=1,
                max_value=5,
                value=3,
                step=2,
            )

            set_num_games = st.number_input(
                "Number of Games to Win Set",
                min_value=2,
                max_value=6,
                value=6,
            )

            set_tiebreak_to = st.number_input(
                "Number of Points to Win Set Tiebreak",
                min_value=3,
                max_value=11,
                value=7,
            )

            match_tiebreak = st.checkbox("Final Set Tiebreak?")

            match_tiebreak_to = st.number_input(
                "Number of Points to Win Final Set Tiebreak",
                min_value=3,
                max_value=21,
                value=10,
            )

            st.caption("Note that changing the match settings will reset any previously entered match, point or scoreboard data.  \nConsider saving the file first.")

            if st.form_submit_button("Confirm New Match Settings"):
                st.session_state['match_datetime'] = datetime.now(timezone.utc)
                st.session_state['player1_name'] = player1_name if player1_name else "Player 1"
                st.session_state['player2_name'] = player2_name if player2_name else "Player 2"

                new_match = Match(
                    player1_name=st.session_state['player1_name'],
                    player2_name=st.session_state['player2_name'],
                    server=server if server else Players.PLAYER_1.value,
                    match_best_of=match_best_of,
                    set_num_games=set_num_games,
                    set_tiebreak_to=set_tiebreak_to,
                    match_tiebreak=match_tiebreak,
                    match_tiebreak_to=match_tiebreak_to
                )
                st.session_state['match'] = new_match
                st.session_state['match_winner'] = Players.NONE.value
                st.session_state['match_metadata'] = new_match.get_initial_inputs()
                st.session_state['match_metadata']['datetime'] = st.session_state['match_datetime'].strftime('%Y-%m-%d %H:%M:%S')
                st.session_state['match_data'] = create_backend_df()

    with st.container(key="page_navigation"):
        st.write("###")
        st.divider()
        if st.button("Track New Match"):
            switch_page("Track Match")
