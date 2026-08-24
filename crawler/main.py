from crawler.client import get_songs
from crawler.parser import parse_song
from crawler.lyric_parser import get_lyric, clean_lyric
import random
import time

keyword = "周杰伦"
songs = get_songs(keyword,1)

result_song = []
result_artist = {}

for song in songs:

    song_data, artist_data = parse_song(song)
    raw_lyric = None
    #筛出纯音乐
    if not song_data["lyric_url"]:
        continue

    raw_lyric = get_lyric(song_data["lyric_url"])
    cleaned_lyric = clean_lyric(raw_lyric)
    song_data["lyric"] = cleaned_lyric

    result_song.append(song_data)
    print("成功获取",song_data["song_name"])

    artist_id=artist_data["artist_id"]
    if artist_id not in result_artist:
        result_artist[artist_id] = artist_data
        print("成功获取",artist_data["artist_name"])
        
    time.sleep(
        random.uniform(0.5,2.5)
    )