import streamlit as st
from connection import LastFMConnector
import pandas as pd

st.title('Last.FM Similar Artists Generator')
connection = LastFMConnector() 

examples = ['Radiohead', 'Daft Punk', 'Weezer', 'Porter Robinson', 'The Weeknd', 'Kali Uchis', 'Custom']
artist_input = st.selectbox('Select An Artist', examples, index=0)

if artist_input == 'Custom':
  custom = st.text_input('Choose a musical artist (Case Sensitive)')
  artist_input = custom




  

