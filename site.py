import streamlit as st
from connection import LastFMConnector
import pandas as pd

st.title('Last.FM Similar Artists Generator')
connection = LastFMConnector()

