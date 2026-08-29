#负责找到和提取json
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR/"data"/"raw"

#为搜索做优化
songs_cache = None
artists_cache = None

def load_songs():
    global songs_cache
    if songs_cache is None:
        file_path = DATA_DIR/"song.json"
        with open(file_path,"r",encoding="utf-8") as file:
            songs_cache = json.load(file)
    return songs_cache

def load_artists():
    global artists_cache
    if artists_cache is None:
        file_path = DATA_DIR/"artist.json"
        with open(file_path,"r",encoding="utf-8") as file:
            artists_cache = json.load(file)
    return artists_cache
