import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from src.utils import *
from src.tennis import Match


if __name__ == "__main__":

    if 'match' not in st.session_state:
        st.session_state['match'] = Match()
    if 'match_data' not in st.session_state:
        st.session_state['match_data'] = create_backend_df()
    if 'player1_name' not in st.session_state:
        st.session_state['player1_name'] = "Player 1"
    if 'player2_name' not in st.session_state:
        st.session_state['player2_name'] = "Player 2"
    if 'match_datetime' not in st.session_state:
        st.session_state['match_datetime'] = datetime.now()

    st.set_page_config(
        page_title="Start",
        # initial_sidebar_state="collapsed",
    )

    st.title("Welcome!")

    with st.container():
        st.header("About")
        st.write(
            "This app is used to track the score of a singles tennis match, and display some accompanying statistics and analysis of both player's actions during the match.\n"
        )
        st.write(
            "It originated as a fun way to help track my friend's tennis matches.\n "
            "The hope is that this app can be used by coaches to help their coachees identify strengths and weaknesses in their game."
        )

    with st.container():
        st.header("Future")
        st.write(
            "The app is currently in it's mvp (minimum viable product) stage, including just the basic features to make it useful to users. In the future I hope to build it out to make it as complete and as useful as possible.\n"
        )
        st.write(
            "Below is a list of features I intend to add:"
            "\n- Prevent the submit point form from resetting if an error is encountered."
            "\n- Show the results of previous sets on the scoreboard."
            "\n- A back button to undo the latest point."
            "\n- The ability to edit the scores."
            "\n- Additional statistics & analysis."
        )

    with st.container():
        st.header("Contact")
        st.write(
            "If you have any feature requests/suggestions or encounter any bugs, please contact me at <jemgodden@gmail.com>.\n "
            "Please include all input steps when reporting a bug so it can be recreated and diagnosed, thanks."
        )

    with st.container():
        st.write("###")
        st.divider()
        left, right = st.columns(2)
        if left.button("Populate New Match"):
            switch_page("New_Match")
        if right.button("Load Previous Match"):
            switch_page("Load Match")
