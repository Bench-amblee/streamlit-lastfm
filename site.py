import streamlit as st
from connection import LastFMConnector
import pandas as pd
from PIL import Image
import requests
from io import BytesIO
import json
import requests
import random

def similar_artist(artist_choice,number_input):
    global test_df
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
    test_df['Artist'] = ra_df['name']
    test_df['Similarity Score'] = ra_df['match']

    return test_df

def get_album_cover(artist):
    global album_name
    def lastfm_get(payload):
        # define headers and URL
        headers = {'user-agent': 'BosHosChos'}
        url = 'https://ws.audioscrobbler.com/2.0/'

        # Add API key and format to the payload
        payload['api_key'] = 'd7efefdd2ff6cdec4b1a223857dba69e'
        payload['format'] = 'json'
        payload['artist'] = artist
        payload['limit'] = 4

        response = requests.get(url, headers=headers, params=payload)
        return response
    r_image = lastfm_get({'method': 'artist.getTopAlbums'})
    r_json = r_image.json()
    r_images = r_json['topalbums']['album']
    ri_df = pd.DataFrame(r_images)
    rn = random.randint(0,(len(ri_df)-1))
    album_name = ri_df['name'][rn]
    album_cover = ri_df['image'][rn][3]['#text']

    response1 = requests.get(album_cover)
    img = Image.open(BytesIO(response1.content))

    return st.image(img)
    


st.image('lastfm.png')
st.title('Last.FM Similar Artists Generator')
st.write("Pick a musical artist you like and this app will recommend a similar artist based on Last.fm's algorithm.")
connection = LastFMConnector() 

examples = ['Taylor Swift','Radiohead', 'Daft Punk', 'Weezer', 'Porter Robinson', 'The Weeknd', 'Kali Uchis', 'Custom']
artist_input = st.selectbox('Select An Artist', examples, index=0)

if artist_input == 'Custom':
  custom = st.text_input('Choose a musical artist (Case Sensitive)')
  artist_input = custom

similar_count = st.slider('How many similar artists would you like?',1,30)

if artist_input == '':
    st.write('Please select an artist')
else:

    test_response = similar_artist(artist_input,similar_count)
    st.write(test_response)

st.write('Of the suggested Artists, pick one and the app will recommend one of their albums')
similar_input = st.selectbox('Select a Similar Artist',list(test_df['Artist']),index=0)
get_album_cover(similar_input)
final_response = ('If you like ' + artist_input + ', you should check out the album ' + album_name + ' by ' + similar_input)
st.write(final_response)


  

