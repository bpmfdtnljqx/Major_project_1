import requests
from crawler.settings import(
    SEARCH_API,
    DEFAULT_PAGESIZE,
    TIME_OUT,
    HEADERS
)

def get_songs(keyword, page):
    """从网站得到歌曲"""
    #请求参数
    Params={
        "text": keyword,
        "pageNo": page,
        "pageSize": DEFAULT_PAGESIZE
    }
    #获取响应数据
    response=requests.get(
        SEARCH_API,
        params= Params,
        headers= HEADERS,
        timeout= TIME_OUT
    )

    response.raise_for_status()
    
    return response.json()