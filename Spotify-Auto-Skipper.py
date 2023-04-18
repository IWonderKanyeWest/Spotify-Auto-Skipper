import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time

# Replace these with your own Spotify API credentials
CLIENT_ID = "Client ID Here"
CLIENT_SECRET = "Client Secret Here"
REDIRECT_URI = "http://localhost:8080/callback/"    

# Prompt the user for the number of songs they want to skip to
num_songs = int(input("Enter the number of songs you want to skip to: "))

# Create a list to store the song names and skip times
song_list = []

# Prompt the user for each song name and skip time
for i in range(num_songs):
    song_name = input("Enter the name of song " + str(i+1) + ": ")
    skip_time = int(input("Enter the time in seconds that you want to skip to in " + song_name + ": "))
    song_list.append((song_name, skip_time))

# Create a SpotifyOAuth object to authenticate with the Spotify API
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope="user-read-playback-state,user-modify-playback-state"))

def check_song():
    # Get the user's current playback information
    playback = sp.current_playback()
    progress = playback['progress_ms'] // 1000

    # Check if the user is currently playing a song
    if playback is None or not playback["is_playing"]:
        print("Nothing is currently playing on Spotify.")
    else:
        # Check if the current song is one of the songs we want to skip to
        track = playback["item"]["name"]
        artist = playback["item"]["artists"][0]["name"]
        for song in song_list:
            song_name, skip_time = song
            if track == song_name:
                if progress <= skip_time:
                    print("Skipping to", skip_time, "seconds in", track, "by", artist)
                    # Skip to the specified time in the song
                    sp.seek_track(skip_time * 1000)
                    break
            else:
                print("Currently playing", track, "by", artist, "which is not", song_name)
    time.sleep(1)

while True:
    check_song()
