import spotipy
from spotipy.oauth2 import SpotifyOAuth
from musixmatch import Musixmatch
import time
import json
import JapaneseTokenizer

scope = "user-library-read"
single_song_test = True

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
musixmatch = Musixmatch('f3a32cf530b7a0f2c522f7e7f5ddef8a')

playlist_id = '6LuKH3zTSJrivrBzZDFB9E'

mecab_wrapper = JapaneseTokenizer.MecabWrapper(dictType='ipadic')

def tokenize(text):
    return mecab_wrapper.tokenize(text).convert_list_object()

def get_tracks_spotify():
    track_list = []
    results = sp.current_user_playlists()
    for playlist in results["items"]:
        if playlist.get('id') == playlist_id:
            for item in sp.playlist_tracks(playlist_id=playlist_id)["items"]:
                track_list.append(item)
            for item in sp.playlist_tracks(playlist_id=playlist_id, offset=100)["items"]:
                track_list.append(item)
    return track_list

def get_track_link(track_list):
    list = []
    for track in track_list:
        list.append(track.get("track").get("external_urls").get("spotify"))
    return list

def get_track_info(track_list):
    list = []
    for track in track_list:
        name = track.get("track").get("name")
        artist = track.get("track").get("artists")[0].get("name")
        list.append((name, artist))
    return list

def get_track_musixmatch(track_name, track_artist):
    song = musixmatch.track_search(track_name, track_artist, 1, 1, "desc")
    try:
        lyric_body = musixmatch.track_lyrics_get(
            song.get("message").get("body").get("track_list")[0].get("track").get("track_id"))
        lyrics = lyric_body.get("message").get("body").get("lyrics").get("lyrics_body")
        lyrics = lyrics.replace("\n\n******* This Lyrics is NOT for Commercial use *******", "")
        return lyrics
    except:
        print("No lyrics found for: " + track_name + " | "+ track_artist)

start = time.time()
track_list = get_tracks_spotify()
info_list = get_track_info(track_list)
print(f"Number of tracks found: {len(track_list)}")
lyric_list = []
if single_song_test:
    track = info_list[0]
    lyric_list.append(get_track_musixmatch(track[0], track[1]))
if not single_song_test:
    for track in info_list:
        lyric_list.append(get_track_musixmatch(track[0], track[1]))
end = time.time() - start
print(f"time elapsed: {end}")
print(lyric_list)
file = open('items.txt','w')
index = 0
for song in lyric_list:
    file.write(info_list[index][0] + " | " + info_list[index][1] + "\n")
    print(song)
    if song is not None:
        song_tokens = tokenize(song)
        print(song_tokens)
        file.write("//".join(song_tokens) + "\n")
    else:
        file.write("None type\n")
    index += 1
file.close()
