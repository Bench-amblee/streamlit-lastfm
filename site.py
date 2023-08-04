import streamlit as st
from connection import LastFMConnector
import pandas as pd

st.title('Last.FM Similar Artists Generator')
connection = LastFMConnector() 

examples = ['Radiohead', 'Daft Punk', 'Weezer', 'Porter Robinson', 'The Weeknd', 'Kali Uchis']
artist_input = st.selectbox('Select An Artist', options, index=0,)

