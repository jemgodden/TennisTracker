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
            "This app is used to track the score of a tennis match, as well as some accompanying statistics and "
            "analysis of both the players and their actions during the match."
        )

    with st.container():
        st.header("History")
        st.write(
            "The purpose of this app originated as a fun way to help track my friend's tennis matches.\n"
        )
        st.write(
            "Previously I would just write down the scores and stats by hand on a notepad. "
            "Eventually I decided to digitise this, which made things much easier. "
            "This allowed for more detailed and useful options and analysis to be added.\n"
        )
        st.write(
            "The hope is that this app can be used by coaches to help their coachees identify their strengths and "
            "weaknesses in their game."
        )

    with st.container():
        st.write("###")
        st.divider()
        left, right = st.columns(2)
        if left.button("Populate New Match"):
            switch_page("New_Match")
        if right.button("Load Previous Match"):
            switch_page("Load Match")
