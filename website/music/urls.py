from django.urls import path
from music import views

#给应用一个命名空间
app_name = 'music'
urlpatterns = [
    #歌曲列表
    path('',views.song_list,name='song_list'),
    #歌曲详情页
    path('song/<int:song_id>/',views.song_detail,name='song_detail'),
    #歌手列表
    path('artists/',views.artist_list,name='artist_list'),
    #歌手详情页
    path('artist/<int:artist_id>/',views.artist_detail,name='artist_detail'),
    #搜索路径
    path('search/',views.search,name='search')
]