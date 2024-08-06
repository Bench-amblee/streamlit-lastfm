import streamlit as st
from openai import OpenAI
from connection import LastFMConnector
import requests
from PIL import Image
import pandas as pd 
import ast
from io import BytesIO


key = st.secrets['openai']['KEY']

def get_openai_response(api_key,messages):
   client = OpenAI(api_key=api_key)
   response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      temperature=1,
      messages=messages
   )
   return response.choices[0].message.content

def get_album_cover(album,artist):
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
      payload['limit'] = 50

      response = requests.get(url, headers=headers, params=payload)
      return response
   r_image = lastfm_get({'method': 'artist.getTopAlbums'})
   r_json = r_image.json()
   r_images = r_json['topalbums']['album']
   ri_df = pd.DataFrame(r_images)
        
   alb_df = ri_df[ri_df['name']==album]

   alb_df = alb_df.reset_index(drop=True)

   album_cover = alb_df['image'][0][3]["#text"]
   response1 = requests.get(album_cover)
   img = Image.open(BytesIO(response1.content))

   return img

tab1, tab2 = st.tabs(["'Find Similar Artists", 'Album Recommendation'])

with tab1:
   
  st.image('lastfm.png')
  st.title('Last.fm Similar Artists Generator')
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

      test_response = LastFMConnector.similar_artist(artist_input,similar_count)
      st.write(test_response)
      st.write('Of the suggested Artists, pick one and the app will recommend one of their albums')
      similar_input = st.selectbox('Select a Similar Artist',list(test_response['Artist']),index=0)
      test_image = LastFMConnector.get_album_cover(similar_input)
      st.image(test_image)
      album_name = LastFMConnector.get_album_name(similar_input)
      final_response = ('If you like ' + artist_input + ', you should check out the album ' + album_name + ' by ' + similar_input)
      st.write(final_response)

with tab2:
   st.title ('Find an Album')
   st.write ('Use the input below to search for an album - you can search for albums in any way, no matter how obscure the prompt is you will get an album in return!')

   st.write("Find an album that....")
   options = ['sounds like ', 'feels like  ', 'reminds me of ', 'makes me want to ', 'makes me feel']
   question = st.selectbox('Select',options, index=0)
   
   user_message = st.text_input("")
   if user_message:
      full_message = "Find an album that " + question + ' ' + user_message
      st.write(full_message)
      if st.button("Send"):
         if user_message:
            messages = [
                  {"role": "system", "content": 'Hello you are a music expert and are tasked with providing people album recommendations based on obscure questions like “give me an album that sounds like how lemons taste”. You must provide them with one album based on their question, no matter how obscure in the form of ["Album Name","Artist Name"]. '},
                  {"role": "user", "content": full_message}
               ]

            response_content = get_openai_response(key, messages)
            album_artist_list = ast.literal_eval(response_content)

            #output = 'listen to ' + album_artist_list[0] + ' by ' + album_artist_list[1]
            st.write(output)
            st.image(get_album_cover(album_artist_list[0],album_artist_list[1]))
            final_statement = 'If you want an album that ' + question + ' ' + user_message + ' you should listen to ' + album_artist_list[0] + ' by ' + album_artist_list[1]
            st.write(final_statement)
