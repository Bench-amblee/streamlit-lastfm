import streamlit as st
from openai import OpenAI
from connection import LastFMConnector

key = st.secrets['openai']['KEY']

def suggest_album(prompt_input):
   client = OpenAI(api_key=key)

   completion = client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
         {"role": "system", "content": "You are a helpful assistant."},
         {"role": "user", "content": prompt_input}
      ]
      max_tokens=50
   )
   return completion.choices[0].message.content


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
   
   st.header("Album Recommendations")
   user_input = st.text_input("Enter an album or artists you like:")
   if user_input:
      prompt_input = f"Recommend an album that sounds like {user_input}."
      suggestion = suggest_album(prompt_input)
      st.write(f'Album recommendation: {suggestion}')
  

