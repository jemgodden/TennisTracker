from datetime import datetime
import pandas as pd
import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from src.tennis import Match


if __name__ == "__main__":

    st.set_page_config(
        page_title="Load Match",
        # initial_sidebar_state="collapsed",
    )

    st.title("Analyse a Previous Match")

    with st.container():
        st.header("Upload a File")

        uploaded_file = st.file_uploader(
            "Choose a CSV file",
            type=['csv'],
            accept_multiple_files=False
        )
        if uploaded_file:
            if 'match' in st.session_state:
                st.session_state.pop('match')
            st.session_state['match'] = Match()

            if 'match_data' in st.session_state:
                st.session_state.pop('match_data')
            st.session_state['match_data'] = pd.read_csv(uploaded_file)

            file_name_vs, file_name_dt = uploaded_file.name.split('-')
            if 'player1_name' in st.session_state:
                st.session_state.pop('player1_name')
            st.session_state['player1_name'] = file_name_vs.split('_vs_')[0].replace('_', ' ')
            if 'player2_name' in st.session_state:
                st.session_state.pop('player2_name')
            st.session_state['player2_name'] = file_name_vs.split('_vs_')[1].replace('_', ' ')
            if 'match_datetime' in st.session_state:
                st.session_state.pop('match_datetime')
            st.session_state['match_datetime'] = datetime.strptime(file_name_dt, '%d%m%Y_%H:%M:%S')

    with st.container():
        st.write("###")
        st.divider()
        if st.button("Analyse Match Data"):
            switch_page("Analysis")
