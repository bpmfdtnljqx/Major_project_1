from crawler.client import get_songs
from crawler.parser import parse_song


songs = get_songs("晴天",1)

song,artist = parse_song(songs[0])

print(song)
print(artist)