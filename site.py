import streamlit as st
from connection import LastFMConnection
import pandas as pd

st.title('Last.FM Similar Artists Generator')
conn = st.experimental_connection('LastFM', type=LastFMConnection)
