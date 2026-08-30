import time
from django.shortcuts import render,redirect
from music.data_loader import load_artists,load_songs
from math import ceil
from music.comment_loader import load_comment,save_comment
from datetime import datetime
def artist_list(request):
    #加载歌手数据
    artists = load_artists()
    #每页显示数量
    per_page = 20
    #获取当前页码，默认第一页
    page = request.GET.get('page',1)
    try:
        page = int(page)
    except ValueError:
        page = 1
    #计算分页
    total_page = ceil(len(artists)/per_page)
    start_index = (page-1)*per_page
    end_index = start_index+per_page
    current_pagedata = artists[start_index:end_index]
    #页码列表
    page_range = range(1,total_page+1)
    display_page = 2
    start_page = max(1,page-display_page)
    end_page = min(total_page,page+display_page)
    page_numbers = range(start_page,end_page+1)    #传递数据给模板
    context = {
        'artists' : current_pagedata,
        'total' : len(artists),
        'page' : page,
        'total_pages' : total_page,
        'page_range' : page_range,
        'page_numbers' : page_numbers
    }
    return render(request,"artist_list.html",context)

def song_list(request):
    songs = load_songs()
    per_page = 20
    page = request.GET.get('page',1)
    try:
        page = int(page)
    except ValueError:
        page = 1
    total_page = ceil(len(songs)/per_page)
    start_index = (page-1)*per_page
    end_index = start_index+per_page
    current_pagedata = songs[start_index:end_index]
    page_range = range(1,total_page+1)
    display_page = 2
    start_page = max(1,page-display_page)
    end_page = min(total_page,page+display_page)
    page_numbers = range(start_page,end_page+1)
    context = {
        'songs' : current_pagedata,
        'total' : len(songs),
        'page' : page,
        'total_pages' : total_page,
        'page_range' : page_range,
        'page_numbers' : page_numbers
    }
    return render(request,"song_list.html",context)

def song_detail(request,song_id):
    songs = load_songs()
    all_artists = load_artists()
    song = None
    for item in songs:
        if item["song_id"] == song_id:
            song = item
            break
    song_artists = []
    if song:
        names = song["artist_names"].split("/")
        for index,artist_id in enumerate(song["artist_ids"]):
            found = False
            for artist in all_artists:
                if artist["artist_id"] == artist_id:
                    song_artists.append(artist)
                    found = True
                    break
            if not found:
                song_artists.append(
                    {
                        "artist_id" : artist_id,
                        "artist_name" : names[index],
                        "artist_image" : "",
                        "artist_intro" : "这个人很神秘，但希望他的歌声可以打动你"
                    }
                )
    all_comments = load_comment()
    comments = []
    for comment in all_comments:
        if comment["song_id"] == song_id:
            comments.append(comment)
    return render(request,"song_detail.html",{"song":song,
                                              "comments":comments,
                                              "artists" : song_artists})

def artist_detail(request,artist_id):
    artists = load_artists()
    songs = load_songs()
    artist = None
    for item in artists:
        if item["artist_id"] == artist_id:
            artist = item
            break
    if artist is None:
        artist_name = "未知歌手"
        for song in songs:
            if artist_id in song["artist_ids"]:
                names = song["artist_names"].split("/")
                index = song["artist_ids"].index(artist_id)
                artist_name = names[index]
                break
        artist = {
            "artist_id" : artist_id,
            "artist_name" : artist_name,
            "artist_image" : "",
            "artist_intro" : "这个人很神秘，但希望ta的歌声可以打动你",
            "artsit_url" : ""
        }
    artist_songs = []
    for song in songs:
        if artist_id in song["artist_ids"]:
            artist_songs.append(song)
    return render(request,"artist_detail.html",{"artist":artist,
                                                "songs":artist_songs})

def search(request):
    #获取搜索内容
    keyword = request.GET.get("keyword","")
    #获取搜索类型
    search_type = request.GET.get("type","song")
    results = []
    cost = 0
    if keyword:
        start = time.time()
        if search_type == "song":
            songs = load_songs()
            for song in songs:
                if(keyword in song["song_name"]
                   or keyword in song["artist_names"]
                   or keyword in song["lyric"]):
                    results.append(song)
        elif search_type == "artist":
            artists = load_artists()
            for artist in artists:
                if(keyword in artist["artist_name"]
                   or keyword in artist["artist_intro"]):
                    results.append(artist)
        end = time.time()
        cost = end - start
    per_page = 20
    page = request.GET.get("page",1)
    try:
        page = int(page)
    except ValueError:
        page = 1
    total_page = ceil(len(results)/per_page)
    start_result = (page-1)*per_page
    end_result = start_result+per_page
    current_result = results[start_result:end_result]
    page_range = range(1,total_page+1)
    context = {
        "keyword" : keyword,
        "type" : search_type,
        "results" : current_result,
        "count" : len(results),
        "cost" : cost,
        "page" : page,
        "total_page" : total_page,
        "page_range" : page_range
    }
    return render(request,"search.html",context)

def add_comment(request,song_id):
    if request.method == "POST":
        content = request.POST.get("content","")
        if content.strip():
            comments = load_comment()
            new_comment = {
                "comment_id" : len(comments)+1,
                "song_id" : song_id,
                "content" : content,
                "time" : datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            }
            comments.insert(0,new_comment)
            save_comment(comments)
    return redirect(f"/song/{song_id}")

def delete_comment(request,comment_id):
    song_id = None
    if request.method == "POST":
        song_id = request.POST.get("song_id")
        comments = load_comment()
        new_comments = []
        for comment in comments:
            if comment["comment_id"] != comment_id:
                new_comments.append(comment)
        save_comment(new_comments)
    return redirect(f"/song/{song_id}")