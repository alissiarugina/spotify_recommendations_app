import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import streamlit as st

# Set up Spotify credentials
client_id = "" 
client_secret = ""
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
#client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_recommendations(track_name, track_artist):
    # Get track URI
    results = sp.search(q=track_name+track_artist, type='track')
    #track_uri = results['tracks']['items'][0]['uri']
    track_uri = results['tracks']['items'][0]

    # Get recommended tracks
    recommendations = sp.recommendations(seed_tracks=[track_uri['uri']])['tracks']
    return track_uri, recommendations

st.title("Music Recommendation System")
track_name = st.text_input("Enter a song name:")
track_artist = st.text_input("Enter the artist name:")

if track_name or track_artist:
    chosen_track, recommendations = get_recommendations(track_name, track_artist)
    #sp.add_to_queue(chosen_track['uri'])
    st.header("Chosen song:") #chosen_track 
    st.write(chosen_track['name'])
    st.image(chosen_track['album']['images'][0]['url'])
    st.link_button("Open in Spotify", chosen_track['external_urls']['spotify'])
    st.header("Recommended songs:")
    for track in recommendations:
        artists = ""
        for a in track['artists']:
            artists += a['name'] + ", "
        st.write(track['name'])
        st.write("Artists: ", artists[:len(artists)-2])
        st.image(track['album']['images'][0]['url'])
        st.link_button("Open in Spotify", track['external_urls']['spotify'] )