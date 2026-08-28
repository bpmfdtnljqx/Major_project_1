#负责找到和提取json
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR/"data"/"raw"

def load_songs():
    file_path = DATA_DIR/"song.json"
    with open(file_path,"r",encoding="utf-8") as file:
        return json.load(file)

def load_artists():
    file_path = DATA_DIR/"artist.json"
    with open(file_path,"r",encoding="utf-8") as file:
        return json.load(file)
