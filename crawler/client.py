import requests
from crawler.settings import(
    SEARCH_API,
    LYRIC_API,
    DEFAULT_PAGESIZE,
    COOKIE,
    TIME_OUT,
    HEADERS
)

def get_songs(keyword, page):
    """从网站得到歌曲"""
    #请求参数
    data={
        "PARAMS" : ("9jfcU6fwrks/3++gMPqNYDC6yIs3dk7nNKjWbx"
        "BK1EDTC5RcxylAt32Mf08QZ2hv7sBM7BwnIiCVs0z"
        "y8+sqx9oFBenzslT9BOfcHc485xfSlwKeUOxzY7zptnH"
        "HmRr92I79Y+WIjCw/lwNx0jLqesnYtKnUd4QuPOcbxHn"
        "O/jZDTeRFVXUXABb9rKbmhALAo/tkR4Q3PoP0RQ74XCwkW5"
        "2mANOSYBJjPwUPTLsoToFQrZ1+tU0H8dverENqjmu3"
        "loJ5Yd6oAfrN/RXavSOjDvWoBA9J3wf+fdAgDhL5DC29VgyS7lNGzkF/XqMzzBzx"),
        "ENCSECKEY" : ("4ec7e6836b4657f51b214177b737c93e164af898cdda498ec28"
        "e8f4096ed6ca10aa624dad506fb436de27e77a1e7c5dccdd7b88e183b5733b1d7200b9f901705"
        "0f604dff67fe1028c3445ee4a3db5ffc72e12041a08ab6"
        "0e5503cb025cc0cf5f2a882bc2b73b308d9c9427171012cd9d12a167b8a04f86a087349f45a838a125")
    }
    #获取响应数据
    response=requests.post(
        SEARCH_API,
        data = data,
        headers= HEADERS,
        cookies=COOKIE,
        timeout= TIME_OUT
    )

    response.raise_for_status()
    
    return response.json()

def get_artists(tab):
    #请求参数
    Params={
        "tab":tab
    }
    #获取响应数据
    response=requests.get(
        ARTIST_API,
        params=Params,
        headers=HEADERS,
        timeout=TIME_OUT
    )

    response.raise_for_status()

    return response.json()

def get_lyric(Lyric_url):
    """得到原始歌词"""
    response = requests.get(Lyric_url,timeout=TIME_OUT)
    response.raise_for_status()
    lyric_text = response.text

    return lyric_text
