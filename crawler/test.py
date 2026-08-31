import requests
from crawler.client import (
    get_songs,
    get_lyric,
    get_songdetail,
    get_artistdetail,
    get_artistintro
)
from crawler.parser import (
    parse_song,
    parse_songdetail,
    clean_lyric
)
from crawler.saver import save_json

#测试2位歌手
TEST_ARTISTS = [
    {
        "artist_id": 3684,
        "artist_name": "林俊杰"
    },
    {
        "artist_id": 2116,
        "artist_name": "陈奕迅"
    },
]
#每位歌手测试5首歌曲
SONGS_PER_ARTIST = 5

def test_crawler():
    artists = []
    songs = []
    song_ids = set()
    for artist in TEST_ARTISTS:
        artist_id = artist["artist_id"]
        artist_name = artist["artist_name"]
        #获取歌手详情
        try:
            detail = get_artistdetail(artist_id)
            artist_image = detail.get("picUrl", "")
            intro = get_artistintro(artist_id)
            if not intro or len(intro.strip()) < 10:
                continue
            artist_data = {
                "artist_id": artist_id,
                "artist_name": artist_name,
                "artist_image": artist_image,
                "artist_url": f"https://music.163.com/artist?id={artist_id}",
                "artist_intro": intro
            }
            artists.append(artist_data)
            print(
                f"成功获取歌手详情：{artist_name}",
                flush=True
            )
        except requests.RequestException:
            continue
        #获取歌曲
        song_count = 0
        page = 1
        while song_count < SONGS_PER_ARTIST:
            data = get_songs(artist_name, page)
            song_list = data.get(
                "result", {}
            ).get(
                "songs", []
            )
            if not song_list:
                break
            for song in song_list:
                if song_count >= SONGS_PER_ARTIST:
                    break
                song_data = parse_song(song)
                song_id = song_data["song_id"]
                if song_id in song_ids:
                    continue
                # 获取歌词
                raw_lyric = get_lyric(song_id)
                if not raw_lyric or len(raw_lyric) < 10:
                    continue
                song_data["lyric"] = clean_lyric(raw_lyric)
                #获取歌曲详情
                detail = get_songdetail(song_id)
                song_data = parse_songdetail(
                    detail,
                    song_data
                )
                song_ids.add(song_id)
                songs.append(song_data)
                song_count += 1
                print(
                    f"成功获取歌曲：{song_data['song_name']}",
                    flush=True
                )
            page += 1
    #保存测试结果
    save_json(
        {
            "artists": artists,
            "songs": songs
        },
        "data/raw/test_song.json"
    )
if __name__ == "__main__":
    test_crawler()