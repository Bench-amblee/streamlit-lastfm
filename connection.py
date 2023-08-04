import requests
import json
from streamlit.connections import ExperimentalBaseConnection
from streamlit.runtime.caching import cache_data
from PIL import Image
from io import BytesIO

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
