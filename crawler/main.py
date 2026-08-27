from crawler.client import get_songs,get_lyric,get_songdetail,get_artistdetail,get_artistintro,get_artistlist,_sleep
from crawler.parser import parse_song,parse_songdetail,clean_lyric
from crawler.saver import save_json
import requests

#歌手分类
ARTIST_CATEGORIES = [
    1001,1002,1003,#华语男、女、组合
    2001,2002,2003,#欧美男、女、组合
    6001,6002,6003#日本男、女、组合
]
#每个分类爬的页数
PER_PAGE = 3
#每个分类最多收集数量
CATEGORY_LIMIT =25
#每个歌手最多搜索页数
SONG_PAGES = 3
#歌曲上限数
TARGET_SONGS = 3000
#自动保存
SAVE_EVERY = 50

def discover_artists():
    """从歌手目录发现歌手"""
    artists_result = []
    artist_ids = set()
    for cat in ARTIST_CATEGORIES:
        category_count = 0
        for page in range(1,PER_PAGE+1):
            if category_count >= CATEGORY_LIMIT:
                break
            artists = get_artistlist(cat,page)
            for artist in artists:
                artist_id = artist.get("id")
                if(artist_id and artist_id not in artist_ids):
                    artists_result.append(
                        {
                            "artist_id" : artist_id,
                            "artist_name" : artist.get("name"),
                            "artist_image" : "",
                            "artist_intro" : ""
                        }
                    )
                    artist_ids.add(artist_id)
                    category_count += 1
                    print(f"成功获取歌手：{artist.get('name')}",flush=True)
                if category_count >= CATEGORY_LIMIT:
                    break
    print(f"共获取歌手：{len(artists_result)}名",flush=True)
    return artists_result

def fill_artistdetail(artists):
    """补充歌手简介"""
    for index,artist in enumerate(artists,1):
        artist_id = artist["artist_id"]
        try:
            detail = get_artistdetail(artist_id)
            artist["artist_image"] = (detail.get("picUrl",""))
            intro = get_artistintro(artist_id)
            artist["artist_intro"] = intro
            print(f"成功获取歌手详情：{artist['artist_name']}",flush=True)
        except requests.RequestException:
            print(f"获取歌手详情失败：{artist['artist_name']}",flush=True)
        _sleep()
    return artists

def crawl_songs(artists):
    """根据歌手爬取歌曲"""
    songs = []
    song_ids = set()
    for artist in artists:
        if len(songs) >= TARGET_SONGS:
            break
        for page in range(1,SONG_PAGES+1):
            if len(songs) >= TARGET_SONGS:
                break
            try:
                data = get_songs(artist["artist_name"],page)
            except requests.RequestException:
                print(f"获取{artist['artist_name']}的歌曲失败",flush=True)
                continue
            song_list = (data.get("result",{}).get("songs",[]))
            for song in song_list:
                song_data = parse_song(song)
                song_id = song_data["song_id"]
                if song_id in song_ids:
                    continue
                #检查是否有歌词
                raw_lyric = get_lyric(song_id)
                #防止暂无歌词通过
                if not raw_lyric or len(raw_lyric) < 10:
                    continue
                song_data["lyric"] = clean_lyric(raw_lyric)
                if not song_data["lyric"]:
                    continue
                detail = get_songdetail(song_id)
                song_data = parse_songdetail(detail,song_data)
                song_ids.add(song_id)
                songs.append(song_data)
                #爬取时方便了解进程
                print(f"成功获取歌曲：{song_data['song_name']}",flush=True)
    print(f"共获取歌曲数：{len(songs)}",flush=True)
    return songs

artists = discover_artists()
artists = fill_artistdetail(artists)
save_json(artists,"data/raw/artist.json")
songs = crawl_songs(artists)
save_json(songs,"data/raw/song.json")