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
      ],
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

   if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
   for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])
    client = OpenAI(api_key=key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)