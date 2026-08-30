import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
COMMENT_FILE = BASE_DIR/"data"/"comment.json"

def load_comment():
    if not COMMENT_FILE.exists():
        return []
    with open(COMMENT_FILE,"r",encoding="utf-8") as file:
        return json.load(file)

def save_comment(comment):
    with open(COMMENT_FILE,"w",encoding="utf-8") as file:
        json.dump(
            comment,
            file,
            ensure_ascii=False,
            indent=4
        )