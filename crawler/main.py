from crawler.client import (
    get_songs,
    get_lyric,
    get_songdetail,
    get_artistdetail,
    get_artistintro,
    get_artistlist,
    get_playlist_catalogue,
    _sleep)
from crawler.parser import parse_song,parse_songdetail,clean_lyric
from crawler.saver import save_json
import requests

#期望歌手数量
ARTIST_TARGET = 360
#每个标签最多搜索页数
DISCOVER_PAGES = 2
#每个歌手最多搜索页数
SONG_PAGES = 2
#歌曲上限数
TARGET_SONGS = 3000
#自动保存
SAVE_EVERY = 50

def discover_artists():
    """从歌手目录发现歌手"""
    artists_result = []
    artist_ids = set()
    #热门歌手
    artists = get_artistlist(1)
    for artist in artists:
        artist_id = artist.get("id")
        if (artist_id and artist_id not in artist_ids):
            artists_result.append(
                {
                    "artist_id": artist_id,
                    "artist_name": artist.get("name"),
                    "artist_image": "",
                    "artist_intro": ""
                }
            )
            artist_ids.add(artist_id)
            print(f"成功获取歌手：{artist.get('name')}",flush=True)
    #通过标签爬取
    catalogue = get_playlist_catalogue()
    sub_tags = catalogue.get("sub",[])
    # 只使用语种和风格标签
    discover_tags = []
    for tag in sub_tags:
        category = tag.get("category")
        if category in [0, 1]:#只选语种或风格
            tag_name = tag.get("name")
            if (tag_name and tag_name not in discover_tags):
                discover_tags.append(tag_name)
    for keyword in discover_tags:
        if len(artists_result) >= ARTIST_TARGET:
            break
        for page in range(1,DISCOVER_PAGES + 1):
            if len(artists_result) >= ARTIST_TARGET:
                break
            data = get_songs(keyword,page)
            song_list = (data.get("result", {}).get("songs", []))
            for song in song_list:
                if len(artists_result) >= ARTIST_TARGET:
                    break
                singer_list = song.get( "artists",[])
                for singer in singer_list:
                    if len(artists_result) >= ARTIST_TARGET:
                        break
                    artist_id = singer.get("id")
                    if (artist_id and artist_id not in artist_ids):
                        artists_result.append(
                            {
                                "artist_id": artist_id,
                                "artist_name": singer.get("name"),
                                "artist_image": "",
                                "artist_intro": ""
                            }
                        )
                        artist_ids.add(artist_id)


                        print(f"成功发现歌手：{singer.get('name')}",flush=True)
    print(f"共获取歌手：{len(artists_result)}名",flush=True)
    return artists_result


def fill_artistdetail(artists):
    """补充歌手简介，并删除没有简介的歌手"""
    valid_artists = []
    for artist in artists:
        artist_id = artist["artist_id"]
        try:
            detail = get_artistdetail(artist_id)
            artist["artist_image"] = (detail.get("picUrl",""))
            intro = get_artistintro(artist_id)
            if not intro or len(intro.strip()) < 10:
                continue
            artist["artist_intro"] = intro
            valid_artists.append(artist)
            print(f"成功获取歌手详情：{artist['artist_name']}",flush=True)
        except requests.RequestException:
            print(f"获取歌手详情失败：{artist['artist_name']}",flush=True)
        _sleep()
    print(f"最终保留歌手{len(valid_artists)}名",flush=True)
    return artists


def crawl_songs(artists):
    """根据歌手爬取歌曲"""
    songs = []
    song_ids = set()
    for artist in artists:
        if len(songs) >= TARGET_SONGS:
            break
        for page in range(1,SONG_PAGES + 1):
            if len(songs) >= TARGET_SONGS:
                break
            data = get_songs(artist["artist_name"],page)
            song_list = (data.get("result", {}).get("songs", []))
            for song in song_list:
                song_data = parse_song(song)
                song_id = song_data["song_id"]
                if song_id in song_ids:
                    continue
                # 检查是否有歌词
                raw_lyric = get_lyric(song_id)
                # 防止暂无歌词
                if (not raw_lyric or len(raw_lyric) < 10):
                    continue
                song_data["lyric"] = clean_lyric(raw_lyric)
                # 获取歌曲详情
                detail = get_songdetail(song_id)
                song_data = parse_songdetail(detail,song_data)
                song_ids.add(song_id)
                songs.append(song_data)
                # 自动保存
                if len(songs) % SAVE_EVERY == 0:
                    save_json(songs,"data/raw/song_temp.json")
                print(f"成功获取歌曲：{song_data['song_name']}",flush=True)
    print(f"共获取歌曲数：{len(songs)}",flush=True)
    return songs

if __name__ == "__main__":
    artists = discover_artists()
    artists = fill_artistdetail(artists)
    save_json(artists,"data/raw/artist.json")
    songs = crawl_songs(artists)
    save_json(songs,"data/raw/song.json")