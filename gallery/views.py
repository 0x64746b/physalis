import io
import os

from django.shortcuts import render, HttpResponse
from PIL import Image, ImageOps
import sh

from gallery.apps import cache
from gallery.models import Album


def show_albums(request):
    return render(
        request,
        'gallery/albums.html',
        {'albums': Album.objects.all()}
    )


def get_thumbnail(request, album_id):
    album = Album.objects.get(id=album_id)
    path = os.path.join(album.path, album.thumbnail)

    thumb = cache.hgetall('thumb:' + path)
    if not thumb:
        image = Image.open(io.BytesIO(sh.cat(path).stdout))
        thumb = {
           b'bytes': ImageOps.fit(image, (800, 600), Image.ANTIALIAS),
           b'format': image.format,
        }
        cache.hmset('thumb:' + path, thumb)

    response = HttpResponse(content_type=Image.MIME[thumb[b'format']])
    thumb[b'bytes'].save(response, thumb[b'format'])

    return response
