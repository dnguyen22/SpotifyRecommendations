import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import config


def setup():
    cid = config.CLIENT_ID
    secret = config.SECRET_ID
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    sp.trace = False
    return sp


def get_playlist_features(sp, user_id, playlist_id):
    playlist = sp.user_playlist_tracks(user_id, playlist_id)
    frames = []
    while True:
        songs = playlist["items"]
        ids = []
        for i in range(len(songs)):
            ids.append(songs[i]["track"]["id"])
        features = sp.audio_features(ids)
        df = pd.DataFrame(features)
        frames.append(df)
        if not playlist['next']:
            break
        playlist = sp.next(playlist)

    return pd.concat(frames)


if __name__ == "__main__":
    playlist_likes_id = config.PLAYLIST_LIKES_ID
    playlist_dislikes_id = config.PLAYLIST_DISLIKES_ID
    user_id = config.USER_ID

    sp = setup()
    df_likes = get_playlist_features(sp, user_id, playlist_likes_id)
    df_dislikes = get_playlist_features(sp, user_id, playlist_dislikes_id)
    df_likes['like?'] = 'yes'
    df_dislikes['like?'] = 'no'

    result = pd.concat([df_likes, df_dislikes])
    result.to_csv(config.FILE_NAME, sep='\t')

