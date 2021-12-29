from django.urls import path
from ..views.views import *


urlpatterns = [
    path('albums/', AlbumList.as_view(), name='albums_list'),
    path('albums/<int:pk>/', AlbumDetail.as_view(), name='album_detail'),
    path('images/', ImageList.as_view(), name='images_list'),
    path('images/<int:pk>/', ImageDetail.as_view(), name='image_detail'),

]
