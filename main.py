import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st

CLIENT_ID = 'd6cf77c016f9443aa41dc992e4532464'
CLIENT_SECRET = '119dc27b862b467db03b361f8e4cb8ae'
REDIRECT_URI = 'https://localhost:3000'



# Set up the Spotify API client
scope = "user-library-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=scope))

# Streamlit UI
st.title("Spotify Liked Songs")

# Prompt the user to log in
username = st.text_input("Enter your Spotify username:")

if username:
    try:
        # Fetch the user's liked songs
        results = sp.current_user_saved_tracks()
        liked_songs = results['items']

        # Paginate through the results if there are more than 20 songs
        while results['next']:
            results = sp.next(results)
            liked_songs.extend(results['items'])

        # Display the liked songs
        st.subheader(f"Liked Songs for {username}:")
        for idx, item in enumerate(liked_songs):
            track = item['track']
            st.write(f"{idx + 1}. {track['name']} - {', '.join([a['name'] for a in track['artists']])}")

    except spotipy.SpotifyException:
        st.error("Invalid username or authentication failed.")