import requests
import re

def get_lyric(Lyric_url):
    """得到原始歌词"""
    response = requests.get(Lyric_url)
    lyric_text=response.text
    return lyric_text

def clean_lyric(raw_lyric):
    """将原始歌词的时间清洗"""
    cleaned_lyric=re.sub(r'\[\d{2}:\d{2}(?:\.\d+)?\]','',raw_lyric)
    return cleaned_lyric