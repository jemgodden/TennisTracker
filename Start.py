import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from src.utils import *
from src.tennis import Match


# Application page - 'Start':
# Generate initial session state variables upon start-up.
# Include general information about the application as well as contact details for bugs and features.


if __name__ == "__main__":

    # Create session state variables to be carried through app if not already existing.
    # This is the first page loaded, so variables should only be created on initial app load.
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
        page_icon=":information_source:",
        layout='wide',
    )

    st.title("Welcome! :wave:")

    # State general information about the application's history, intended usage, and contact details for issues/ideas.

    with st.container(key="about"):
        st.header("About")
        st.write(
            "This application is intended to be used by amateur tennis players and coaches to track the score of a singles tennis match, and display some accompanying statistics and analysis of both players' actions during the match.  \n"
            "The hope is that it can be used to identify strengths and weaknesses in a player's game and help give areas to focus on or adapt during a match.  \n\n"
            "It is worth noting that the data input for this application is not automated, so requires some manual input for each point from a spectator."
        )

    with st.container(key="usage"):
        st.header("Usage")
        st.write(
            "If you want to start tracking a new match:  \n"
            "- You can set the parameters for the match by navigating to the 'New Match' page.  \n"
            "- You can add point data to the match by navigating to the 'Track Match' page. From this page you can save any populated information to a file, which can be loaded in later.  \n\n"
            "If you want to load a previous match to analyse, or continue populating data for:  \n"
            "- You can load in files previously created by this app by navigating to the 'Load Match' page.  \n\n"
            "Once you have recorded data for a current or loaded match, you can access the statistics and analysis for it by navigating to the 'Analyse Match' page. "
            "There are various filters on this page for what aspect you would like to analyse."
        )

    with st.container(key="future"):
        st.header("Future")
        st.write(
            "The app is currently in it's mvp (minimum viable product) stage, including just the basic features to make it useful to users. In the future I hope to build it out to make it as complete and as useful as possible.  \n"
        )
        st.write(
            "Below is a list of features I intend to add:"
            "\n- Complete logging for application to better diagnose bugs."
            "\n- Prevent the submit point form from resetting if an error is encountered."
            "\n- Show the results of previous sets on the scoreboard."
            "\n- A back button to undo the latest point."
            "\n- The ability to edit the scores."
            "\n- Additional/Improved statistics & analysis."
            "\n- Ability to display both player's statistics/analysis side-by-side."
            "\n- Create a full backend to analyse player data over multiple matches."
        )

    with st.container(key="contact"):
        st.header("Contact")
        st.write(
            "If you have any feature requests/suggestions or encounter any bugs, please contact me at <jemgodden@gmail.com>.  \n"
            "Please include all input steps when reporting a bug so it can be recreated and diagnosed."
        )

    with st.container(key="page_navigation"):
        st.write("###")
        st.divider()
        left, right = st.columns(2)
        if left.button("Create New Match"):
            switch_page("New Match")
        if right.button("Load Previous Match"):
            switch_page("Load Match")
