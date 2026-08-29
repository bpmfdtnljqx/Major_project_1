from django.urls import path
from music import views

#给应用一个命名空间
app_name = 'music'
urlpatterns = [
    #歌曲列表
    path('',views.song_list,name='song_list'),
    #歌手列表
    path('artists/',views.artist_list,name='artist_list')
    #歌手详情页
    
]