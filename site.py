import streamlit as st
from connection import LastFMConnector
import pandas as pd
from PIL import Image
import requests
from io import BytesIO
import json
import requests

def similar_artist(artist_choice,number_input):
    def lastfm_get(payload):
        # define headers and URL
        headers = {'user-agent': 'BosHosChos'}
        url = 'https://ws.audioscrobbler.com/2.0/'

        # Add API key and format to the payload
        payload['api_key'] = 'd7efefdd2ff6cdec4b1a223857dba69e'
        payload['format'] = 'json'
        payload['artist'] = artist_choice
        payload['limit'] = int(number_input)

        response = requests.get(url, headers=headers, params=payload)
        return response


    r = lastfm_get({
    'method': 'artist.getSimilar'})

    r_json = r.json()
    r_artists = r_json['similarartists']['artist']
    ra_df = pd.DataFrame(r_artists)
    similar_artists_list = ra_df['name']
    url = ra_df['url']
    score = ra_df['match']

    test_df = pd.DataFrame()
    test_df['Arist'] = ra_df['name']
    test_df['Similarity Score'] = ra_df['match']


    st.write(test_df['Artist'])

st.title('Last.FM Similar Artists Generator')
connection = LastFMConnector() 

examples = ['Taylor Swift','Radiohead', 'Daft Punk', 'Weezer', 'Porter Robinson', 'The Weeknd', 'Kali Uchis', 'Custom']
artist_input = st.selectbox('Select An Artist', examples, index=0)

if artist_input == 'Custom':
  custom = st.text_input('Choose a musical artist (Case Sensitive)')
  artist_input = custom

similar_count = st.slider('How many similar artists would you like?',1,10)

if artist_input == '':
    st.write('Please select an artist')
else:

    test_response = similar_artist(artist_input,similar_count)
    st.write(test_response)




  

