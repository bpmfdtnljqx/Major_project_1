import requests
import time
import random
from crawler.settings import(
    SEARCH_API,
    LYRIC_API,
    DEFAULT_PAGESIZE,
    TIME_OUT,
    COOKIE,
    HEADERS,
    SONG_DETAIL_API,
    ARTIST_API,
    ARTIST_INTRO_API,
    ARTISTLIST_API,
    DEFAULT_ARTISTLIST,
    PLAYLIST_CATALOGUE_API
)

session = requests.Session()
session.headers.update(HEADERS)
if COOKIE:
    session.cookies.update(COOKIE)

def _sleep():
    """间歇爬取"""
    time.sleep(random.uniform(1,3))

def get_songs(keyword, page):
    """从网站得到歌曲"""
    params = {
        "s": keyword,
        "type": 1,
        "offset": (page-1)*DEFAULT_PAGESIZE,
        "limit": DEFAULT_PAGESIZE,
        "total": "true"
    }
    #获取响应数据
    response = session.get(SEARCH_API,params=params,timeout = TIME_OUT)
    response.raise_for_status()
    _sleep()
    return response.json()

def get_lyric(song_id):
    """通过歌曲id获得歌词"""
    params = {
        "id": song_id,
        "lv": -1,
        "kv": -1,
        "tv": -1,
    }
    response = session.get(
        LYRIC_API,
        params=params,
        timeout=TIME_OUT)
    response.raise_for_status()
    _sleep()
    lyric = response.json().get("lrc",{}).get("lyric")
    return lyric

def get_songdetail(song_id):
    """通过歌曲id获得除歌词外的信息"""
    params = {
        "ids": f"[{song_id}]"
    }
    response = session.get(
        SONG_DETAIL_API,
        params=params,
        timeout=TIME_OUT
    )
    response.raise_for_status()
    _sleep()
    song = response.json().get("songs",[])[0]
    return song

def get_artists(keyword, page):
    """按关键词搜索歌手"""
    params = {
        "s": keyword,
        "type": 100,
        "offset": (page - 1) * DEFAULT_PAGESIZE,
        "limit": DEFAULT_PAGESIZE,
    }
    response = session.get(SEARCH_API, params=params, timeout=TIME_OUT)
    response.raise_for_status()
    _sleep()
    return response.json()

def get_artistdetail(artist_id):
    """按歌手id获取歌手信息"""
    url = ARTIST_API.format(artist_id=artist_id)
    response = session.get(url, timeout=TIME_OUT)
    response.raise_for_status()
    _sleep()
    return response.json().get("artist", {})


def get_artistintro(artist_id):
    """按歌手id获取歌手简介,部分冷门歌手可能没有"""
    params = {"id": artist_id}
    response = session.get(ARTIST_INTRO_API, params=params, timeout=TIME_OUT)
    response.raise_for_status()
    _sleep()
    intro_list = response.json().get("introduction",[])
    parts = []
    for item in intro_list:
        title = item.get("ti", "").strip()
        text = item.get("txt", "").strip()
        if text:
            parts.append(f"{title}\n{text}" if title else text)
    return "\n\n".join(parts)

def get_artistlist(page):
    "按分页获取歌手目录"
    params = {
        "limit" : DEFAULT_ARTISTLIST,
        "offset" : (page-1)*DEFAULT_ARTISTLIST
    }
    response = session.get(ARTISTLIST_API,params=params,timeout=TIME_OUT)
    response.raise_for_status()
    _sleep()
    return response.json().get("artists",[])

def get_playlist_catalogue():
    """获取标签目录"""
    response = session.get(PLAYLIST_CATALOGUE_API,timeout=TIME_OUT)
    response.raise_for_status()
    _sleep()
    return response.json()