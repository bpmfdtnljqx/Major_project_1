import re
from crawler.settings import SONG_URL,ARTIST_URL

def parse_song(song):
    """解析歌曲数据"""
    song_id = song.get("id")
    #处理多个歌手的问题
    artist_ids = []
    artist_names = []
    singer_list = song.get("artists",[])
    for singer in singer_list:
        artist_ids.append(singer.get("id"))
        artist_names.append(singer.get("name"))
    album = song.get("album") or {}
    song_data={
        "song_id" : song.get("id"),
        "song_name" : song.get("name"),
        "song_url" : SONG_URL.format(id=song_id),
        "album_id" : album.get("id"),
        "album_name" : album.get("name"),
        "duration" : song.get("duration"),
        "cover_url" : "",
        "artist_ids" : artist_ids,
        "artist_names" : "/".join(artist_names),
        "lyric" : ""
    }
    return song_data

def parse_songdetail(song,song_data):
    """解析封面等数据"""
    album = song.get("album") or {}
    song_data["cover_url"] = album.get("picUrl","")
    song_data["publish_time"] = album.get("publishTime")
    return song_data

def parse_artist(artist):
    """解析歌手数据"""
    artist_data={
        "artist_id" : artist.get("id"),
        "artist_name" : artist.get("name"),
        "artist_image" : artist.get("picUrl"),
        "artist_url" : ARTIST_URL.format(id=artist.get("id")),
        "artist_intro" : ""
    }
    return artist_data

def clean_lyric(raw_lyric):
    """将原始歌词的时间清洗"""
    cleaned_lyric = re.sub(r'\[\d{2}:\d{2}(?:\.\d{1,3})?\]','',raw_lyric)
    cleaned_lyric = re.sub(r'\n\s*\n+','\n',cleaned_lyric)
    return cleaned_lyric.strip()