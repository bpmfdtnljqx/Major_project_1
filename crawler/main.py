from crawler.client import get_songs
from crawler.parser import parse_song, get_lyric, clean_lyric
from crawler.saver import save_json
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
    if len(result_song)%50 == 0:
        save_json(result_song, "data/raw/songs.json")  

    artist_id=artist_data["artist_id"]
    if artist_id not in result_artist:
        result_artist[artist_id] = artist_data
        print("成功获取",artist_data["artist_name"])
        save_json(result_artist,"data/raw/artist.json")

    time.sleep(
        random.uniform(0.5,2.5)
    )

print("成功获取歌曲数", len(result_song))
print("成功获取歌手数", len(result_artist))