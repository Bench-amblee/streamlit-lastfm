import requests
import json
import pandas as pd
from PIL import Image
import requests
from io import BytesIO
import random
from streamlit.connections import ExperimentalBaseConnection
from streamlit.runtime.caching import cache_data
import openai
import python-dotenv


class LastFMConnector(ExperimentalBaseConnection[requests.Session]):
    def __init__(self, *args, connection_name=None, **kwargs):
        super().__init__(*args, connection_name=connection_name, **kwargs)
        self._resource = self._connect()
    def _connect(self) -> requests.Session:
        return requests.Session()
    def cursor(self):
        return self._resource
    
    def randon_query(self):
        cache_data(ttl=0)
        def getmusic():
            url = 'https://ws.audioscrobbler.com/2.0/'
            print(f"URL is {url}")
            response = self._resource.get(url)
            if response.status_code == 200:
                return response.content
            else:
                raise Exception(f"Failed to fetch.")
        return getmusic()
    
    def query(self, tag = None, gif=False, says = None, ttl: int = 10):
        @cache_data(ttl=ttl)
        def getUrl(url):
            url = 'https://ws.audioscrobbler.com/2.0/'
        return getmusic(url)

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
        global rn
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

        return img

    def get_album_name(artist):
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
        album_name = ri_df['name'][rn]

        return album_name
