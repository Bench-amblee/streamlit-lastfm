import streamlit as st
from connection import LastFMConnection
import pandas as pd

st.title('Last.FM Similar Artists Generator')
connection = LastFMConnection()

