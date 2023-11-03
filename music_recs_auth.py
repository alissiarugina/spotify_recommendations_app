import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util

import streamlit as st

# Set up Spotify credentials
client_id = "" 
client_secret = ""
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
scope = "user-modify-playback-state"
sp_oauth = SpotifyOAuth(
    client_id,
    client_secret,
    redirect_uri="http://localhost:8888/callback",
    scope = "user-modify-playback-state"
    )
#sp = spotipy.Spotify(oauth_manager=sp_oauth)

token = util.prompt_for_user_token('USERNAME_TO_AUTHORIZE',scope,client_id=client_id,client_secret=client_secret,redirect_uri="http://localhost:8888/callback")
sp = spotipy.Spotify(auth=token)


def get_recommendations(track_name, track_artist):
    # Get track URI
    results = sp.search(q=track_name+track_artist, type='track')
    track_uri = results['tracks']['items'][0]

    # Get recommended tracks
    recommendations = sp.recommendations(seed_tracks=[track_uri['uri']])['tracks']
    return track_uri, recommendations

if('show_results' not in st.session_state):
    st.session_state['show_results'] = False
st.session_state["run_recommendations"] = False
# search_recs = {}
# search_recs.val = False

def search():
    st.session_state['show_results'] = True
    st.session_state['run_recommendations'] = True

st.title("Music Recommendation System")
track_name = st.text_input("Enter a song name:")
track_artist = st.text_input("Enter the artist name:")
if(st.button("Search", key="search_recommendations")):
    on_click=search()

if (track_name or track_artist) and st.session_state['show_results'] :
    if ("chosen_track" not in st.session_state) or st.session_state['run_recommendations']:
        st.session_state["chosen_track"], st.session_state["recommendations"] = get_recommendations(track_name, track_artist)
    # retrieve values from state
    chosen_track = st.session_state['chosen_track']
    recommendations = st.session_state['recommendations']
    st.header("Chosen song:") #chosen_track 
    st.write(chosen_track['name'])
    st.image(chosen_track['album']['images'][0]['url'])
    if (st.button("Add to queue",key='chosen')):
       sp.add_to_queue(chosen_track['uri'])
    st.link_button("Open in Spotify", chosen_track['external_urls']['spotify'])
    st.header("Recommended songs:")
    i = 0
    for track in recommendations:
        artists = ""
        for a in track['artists']:
            artists += a['name'] + ", "
        st.write(track['name'])
        st.write("Artists: ", artists[:len(artists)-2])
        st.image(track['album']['images'][0]['url'])
        
        if st.button("Add to queue",key=i):
            sp.add_to_queue(track['uri'])
        st.link_button("Open in Spotify", track['external_urls']['spotify'] )
        i += 1
