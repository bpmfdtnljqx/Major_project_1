def parse_song(song):
    """解析数据"""
    song_data={
        "song_id":song.get("songId"),
        "song_name":song.get("songName"),
        "album":song.get("album"),
        "duration":song.get("duration"),
        "play_count":song.get("playNumDesc"),
        "cover_url":song.get("img1"),
        "lyric_url":song.get("ext").get("lrcUrl"),
        "artist_id":song.get("singerList")[0].get("id"),
        "artist_name":song.get("singerList")[0].get("name")
    }
    artist_data={
        "artist_name":song.get("singerList")[0].get("name"),
        "artist_id":song.get("singerList")[0].get("id"),
        "artist_image":song.get("singerList")[0].get("img")
    }
    return song_data, artist_data