from django.urls import path

from . import views

urlpatterns = [
    path('', views.show_albums, name='albums'),
    path('^thumbnail/<int:album_id>', views.get_thumbnail, name='get_thumbnail'),
]
