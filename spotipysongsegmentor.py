
import spotipy, os, json, datetime
import pandas as pd
from spotipy.oauth2 import SpotifyOAuth

MAX_NUM_SONG_ADD_PLAYLIST = 100
MAX_NUM_SONG_SAVE = 50

scope = "user-library-read playlist-modify-public"


def create_auth_manager(scope):
    # keep in here - private - but setting env variables not working rn
    #username = "ahmediy1" for other auth type
    # os.environ["SPOTIPY_CLIENT_ID"] = "8e528596b3544289a0fa4648fff13438"
    # os.environ["SPOTIPY_CLIENT_SECRET"] = "7d6c1bdddc2942f092a9337bcbe4593e"
    # os.environ["SPOTIPY_REDIRECT_URI"] = "http://localhost:8888/callback/"
    client_id = os.environ("SPOTIPY_CLIENT_ID")
    client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")
    return SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope)

#all saved tracks into list
def raw_data_from_liked_songs(sp):
    liked_songs = []
    num_songs = sp.current_user_saved_tracks(limit=1)["total"] #max # songs to know how many groups of song saves to do
    for i in range(0,num_songs,MAX_NUM_SONG_SAVE):
        songs = sp.current_user_saved_tracks(limit=MAX_NUM_SONG_SAVE, offset=i)["items"]
        liked_songs += songs
    print(f"Found {len(liked_songs)} songs")
    return liked_songs

def clean_song_data(semi_clean_song_data):
    """technically cleaning not from raw but from raw_data['items']"""
    # songs_time_added = [song["added_at"][:-1] for song in semi_clean_song_data]
    # song_time_added_objs = [datetime.datetime.fromisoformat(date) for date in songs_time_added]
    # song_ids = [semi_clean_song_data[0]["track"]["id"] for song in semi_clean_song_data]
    # clean_songs_data = {song_ids[i]:songs_time_added[i] for i in range(len(song_ids))}
    clean_songs_data = {song["track"]["id"]:datetime.datetime.fromisoformat(song["added_at"][:-1]) for song in semi_clean_song_data}

    return clean_songs_data


def segment_songs(songs_data):
    print(songs_data)
    now = datetime.datetime.now()
    min_date = min(songs_data.values())
    print(f"Earliest song added in: {min_date.year}.")
    ordered_segment_names = []
    major_groups = range(min_date.year, now.year + 1)
    # ordered_sub_group_names = ["Winter", "Summer", "Fall"]
    ordered_sub_group_names = [""]
    ordered_segment_criteria = [] #i.e. cutoff
    ordered_sub_group_criteria = [1]
    for major_group in major_groups:
        for sub_group_name in ordered_sub_group_names:
            ordered_segment_names.insert(0,f"{sub_group_name} {major_group}")
        for sub_group_criterion in ordered_sub_group_criteria:
            ordered_segment_criteria.insert(0, datetime.datetime(major_group, sub_group_criterion, 1))

    segment_discriminators = {ordered_segment_names[i]:ordered_segment_criteria[i] for i in range(len(ordered_segment_criteria))}
    # print(segment_discriminators)

    processed_songs_data = {}
    previous_criteria = datetime.datetime(2099,1,1)
    for name, criteria in segment_discriminators.items():
        song_ids = []
        for song_id, date in songs_data.items():
            if date > criteria and date < previous_criteria:
                # print(f"{date} > {criteria}")
                song_ids.insert(0,song_id)
        processed_songs_data[f"{name}"] = song_ids
        previous_criteria = criteria
    return processed_songs_data

def create_playlists(processed_songs_data, sp):
    """   input in format:
     songs = {
        "time_period_1": ["2HbKqm4o0w5wEeEFXm2sD4", "5odlY52u43F5BjByhxg7wg"] #song ids,
        "time_period_2": ["75ZvA4QfFiZvzhj2xkaWAh", "7FbrGaHYVDmfr7KoLIZnQ7"],
        "time_period_3": ["7FbrGaHYVDmfr7KoLIZnQ7", "2HbKqm4o0w5wEeEFXm2sD4"]
    }
    """
    user_id = sp.me()['id']
    # for each chunk in song_list AND song in chunk:
    for segment, song_ids in processed_songs_data.items():
        # create playlist with name and description
        playlist = sp.user_playlist_create(user_id, name=segment, description=f"Songs from {segment} from oldest to newest.")
        # add song list to playlist
            #segment song lists into 100 chunks
        for i in range(0, len(processed_songs_data[segment]), MAX_NUM_SONG_ADD_PLAYLIST):
            song_ids_chunk = song_ids[i:i + MAX_NUM_SONG_ADD_PLAYLIST]
            try:
                sp.playlist_add_items(playlist_id=playlist["id"],items=song_ids_chunk, position=0)
                print(f"Adding songs {i} to {i + MAX_NUM_SONG_ADD_PLAYLIST}.")
            except:
                print(f"Failed to add songs {i} to {i + MAX_NUM_SONG_ADD_PLAYLIST}.")
        print("Playlist generation complete!\n")
    return "Program complete."

def app():
    auth_manager = create_auth_manager(scope=scope)
    sp = spotipy.Spotify(client_credentials_manager= auth_manager)
    pd.options.display.max_columns = None
    liked_songs = raw_data_from_liked_songs(sp)
    clean_liked_songs_data = clean_song_data(liked_songs)
    segmented_songs = segment_songs(clean_liked_songs_data)
    finish_message = create_playlists(segmented_songs, sp)
    print(finish_message)

if __name__ == "main":
    app()
