from crawler.client import get_songs
from crawler.parser import parse_song
from crawler.lyric_parser import get_lyric, clean_lyric

test = get_songs("晴天", 1)
song, artist=parse_song(test[0])
raw_lyric = None
if song["lyric_url"] != '':
    raw_lyric= get_lyric(song["lyric_url"])
    cleaned_lyric=clean_lyric(raw_lyric)
print(cleaned_lyric)
