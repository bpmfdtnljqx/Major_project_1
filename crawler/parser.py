from crawler.settings import TIME_OUT
import requests
import re

def parse_song(song):
    """解析歌曲数据"""
    #处理多个歌手的问题
    artists = []
    singer_list = song.get("singerList",[])
    for singer in singer_list:
        artists.append(
            {
                "artist_id" : singer.get("id"),
                "artist_name" : singer.get("name")
            }
        )

    song_data={
        "song_id": song.get("songId"),
        "song_name": song.get("songName"),
        "album": song.get("album"),
        "duration": song.get("duration"),
        "play_count": song.get("playNumDesc"),
        "cover_url": song.get("img1"),
        "lyric_url": song.get("ext",{}).get("lrcUrl"),
        "artists" : artists,
        "lyric": ""
    }
    
    return song_data

def parser_artist(artist):
    """解析歌手数据"""
    artist_data={
        "artist_id" : artist.get("txt2"),
        "artist_name" : artist.get("txt"),
        "artist_image" : artist.get("img")
    }

    return artist_data

def get_lyric(Lyric_url):
    """得到原始歌词"""
    response = requests.get(Lyric_url,timeout=TIME_OUT)
    response.raise_for_status()
    lyric_text = response.text

    return lyric_text

def clean_lyric(raw_lyric):
    """将原始歌词的时间清洗"""
    cleaned_lyric = re.sub(r'\[\d{2}:\d{2}(?:\.\d+)?\]','',raw_lyric)
    
    return cleaned_lyric.strip()