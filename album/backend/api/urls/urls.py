from django.urls import  path
from  rest_framework.urlpatterns import format_suffix_patterns
from ..views.views import *


urlpatterns = [
    path('albums/', AlbumList.as_view()),
    path('albums/<int:pk>/', AlbumDetail.as_view()),
    path('images/', ImageList.as_view()),
    path('images/<int:pk>/', ImageDetail.as_view()),

]


