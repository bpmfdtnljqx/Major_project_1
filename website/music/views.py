from django.shortcuts import render
from music.data_loader import load_artists,load_songs
from math import ceil
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
    return render(request,"_list.html",context)