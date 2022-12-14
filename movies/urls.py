from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from movies.views import *

urlpatterns = [
    path('', movies_list, name='movies_list'),
    path('movies/<int:pk>', movie_detail, name='movie_detail'),
    path('movies/add', movie_add, name='movie_add'),
    path('edit_movie/<int:pk>/', edit_movie, name="edit_movie"),
    path('delete_movie/<int:pk>/', delete_movie, name="delete_movie"),
    path('movies/<int:pk>/comment', movie_comment, name='movie_comment'),
    path('<int:pk>/rate', movie_rate, name='movie_rate')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
