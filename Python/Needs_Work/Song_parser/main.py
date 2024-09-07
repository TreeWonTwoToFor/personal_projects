import spotipy
from spotipy.oauth2 import SpotifyOAuth
from musixmatch import Musixmatch
import time
import json

scope = "user-library-read"
f = open("C:\\Tree's Stuff\\discord_tokens\\musixmatch.json", "r")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
musixmatch = Musixmatch(json.loads(f.read()).get("token"))

playlist_id = '6LuKH3zTSJrivrBzZDFB9E'

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
for track in info_list:
    lyric_list.append(get_track_musixmatch(track[0], track[1]))
end = time.time() - start
print(f"time elapsed: {end}")