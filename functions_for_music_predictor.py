import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from IPython.display import Javascript
import pandas as pd



##################Part 1, conecting to the api and dowloading the data frames##############
#### Takes user input: (only works with the numerical part of the link or the uri)
def getting_user_playlist():
    user_input = input("please paste your share playlist link")
    
    return user_input

#### takes user input and conects to the api so that i can download the 
#### returns a dictionary named Playlist_dict
def one_one(user_imput_url):
    global sp
    playlist = sp.user_playlist_tracks("spotify", user_imput_url)
    long_json = playlist['items']
    
    while playlist['next']:
        
        playlist = sp.next(playlist)
        long_json.extend(playlist['items'])
        song_names = [i["track"]["name"] for i in long_json]
        artist_names =  [i["track"]["artists"][0]["name"] for i in long_json]
        uris = [i["track"]["uri"] for i in long_json]
        
        Playlist_dict = {
        "Songs":song_names,
        "Artists":artist_names,
        "uri":uris,
        }
        
    return Playlist_dict

#### Fetches the data features from the data frame that was downloaded in one_one
#### Will return a data frame with the audio features 
def returning_dict(data_frame):
    dataframe_return = []
    for uri in data_frame["uri"]:
        features = sp.audio_features(uri)
        temp_df = pd.DataFrame(features)
        dataframe_return.append(temp_df)
    
    return dataframe_return

#### defines main for the data importer, merges the previous two data frames 
#### will return a data frame that then has to be saved, as well as all the info necessary
##### have to add keys for spotify api 
def main():
   
    user_input = getting_user_playlist()
    data_frame = pd.DataFrame(one_one(user_input))
    concatt = pd.concat(returning_dict(data_frame))
    final_playlist = pd.merge(data_frame, concatt[['uri', 'acousticness', 'analysis_url', 'danceability',
           'duration_ms', 'energy', 'id', 'instrumentalness', 'key', 'liveness',
           'loudness', 'mode', 'speechiness', 'tempo', 'time_signature',
           'track_href', 'type', 'valence']], on='uri')
    print("the name of the data frame is final_playlist, use......"
          "(final_playlist.to_csv(##whatever_name.csv)) to save it")
          
    return final_playlist




