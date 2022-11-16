# SETTING IT ALL UP (MODULES, SPOTIPY SET-UP, CLIENT INFO)

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import spotipy 
from spotipy.oauth2 import SpotifyClientCredentials
client_id = "8d378f6fe98a4d0cb29139a7c13ce631"
client_secret = "4cd92ca9c2d8444598f1c6766932627f"
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# PLAYLIST INFO

url = "https://open.spotify.com/playlist/3UqvpsWjefG0cwtCjL3cB0?si=e7a321ceaa5e455c"
username = "soumya"
playlist_id = "3UqvpsWjefG0cwtCjL3cB0"

# GETTING PLAYLIST DATA

sp.user_playlist_tracks(username, playlist_id)


# GETTING FULL PLAYLIST (still under construction)

def get_full_tracks(username, playlist_id):
    results = sp.user_playlist_tracks(username, playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

# IMPORTING PLAYLIST DATA INTO A DATAFRAME

def make_dataframe(username, playlist_id):
    #df columns
    features = ["artist", "album", "track_name", "track_id", "danceability", "energy", "key", "loudness","mode", "speechiness", "instrumentalness", "liveness", "valence", "tempo", "duration_ms", "time_signature"]
    #make df
    playlist_df = pd.DataFrame(columns=features)
    #get playlist
    playlist = get_full_tracks(username, playlist_id)

    #adding track info to df
    for track in playlist:
        playlist_dict = {}
        # track data
        playlist_dict["artist"]=track["track"]["album"]["artists"][0]["name"]
        playlist_dict["album"]=track["track"]["album"]["name"]
        playlist_dict["track"]=track["track"]["name"]
        playlist_dict["track_id"]=track["track"]["id"]

        #audio data
        audio_features = sp.audio_features(playlist_dict["track_id"])[0]
        for feature in features[4:]:
            playlist_dict[feature]=audio_features[feature]
        
        #combining data
        track_df=pd.DataFrame(playlist_dict, index = [0])
        playlist_df=pd.concat([playlist_df, track_df], ignore_index = True)
    return playlist_df

data=make_dataframe(username, playlist_id)

# VISUALISING DATA - BOXPLOTS

select_features=["danceability", "energy", "key", "loudness","mode", "speechiness", "liveness", "valence", "tempo", "duration_ms", "time_signature"]

## some predictions for general data behaviour -
##  danceability: > 0.6
##  mode : 1.0 (major)
##  speechiness: 0

def box_plots(dataframe, features_list):
    for feature in features_list:
        plt.figure(figsize=(10, 7))
        sns.boxplot(y=dataframe[feature])
        sns.set_style('darkgrid')
        sns.set_palette('bright')
        plt.show()
        plt.clf()

box_plots(data, select_features)

        
