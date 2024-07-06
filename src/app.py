import streamlit as st


st.button('Ace')
st.button('Double Fault')

st.selectbox('Serve', ['', 'First', 'Second'])

st.button('Let')

st.selectbox('Winner', ['', 'Forehand', 'Backhand', 'Smash'])
st.selectbox('Error', ['', 'Forced', 'Unforced'])

st.button('End Game')
st.button('End Set')
st.button('End Match')
