import streamlit as st
from streamlit.connections import ExperimentalBaseConnection
import requests
from os import path
import time

class LastFMConnection(ExperimentalBaseConnection[requests.Session]):
    
    def _connect(self, **kwargs) -> requests.Session:
        """
        Connects to Last.FMs APIs, generates an access_token, and
        returns the requests session object.
        
        Returns:
            requests.Session: the requests session object.
        """
        oauth_url = self._secrets['oauth_url']
        client_id = self._secrets['client_id']
        client_secret = self._secrets['client_secret']
        query_params = {'grant_type': 'client_credentials'}

        session = requests.Session()
        
        response = session.post(
            url=oauth_url,
            params=query_params,
            auth=(client_id, client_secret)
        )
        self._access_token = response.json()['access_token']
        st.write(self._access_token)

        return session
    
    def cursor(self) -> requests.Session:
        """
        Returns the underlying requests session as the cursor.
        
        Returns:
            requests.Session: the requests session object.
        """
        if hasattr(self, '_instance') and self._instance:
            return self._instance
        
        self._instance = self._connect()
        return self._instance
    
    def get(self, url, ttl:int=3600, **kwargs) -> requests.Response:
        """
        Performs an HTTP get request
        
        Returns:
            requests.response: """

        @st.cache_data(ttl=ttl, **kwargs)
        def _get(url) -> dict:
            headers = {'Authorization': f'Bearer {self._access_token}'}
            cur = self.cursor()
            response = cur.get(url=url, headers=headers)
            return response

        response = _get(url)
        
        if response.status_code == 200:
            time.sleep(0.05)
            return response
        elif response.status_code == 429:
            # st.write(response.json())
            # print(response.json())
            raise Exception(f'Failed to fetch data from {url} with error code {response.status_code}.') 
        else:
            raise Exception(f'Failed to fetch data from {url} with error code {response.status_code}.')
