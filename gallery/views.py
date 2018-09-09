import io
import os

from django.shortcuts import render, HttpResponse
from PIL import Image, ImageOps
import sh

from gallery import cache
from gallery.models import Album


def show_albums(request):
    return render(
        request,
        'gallery/albums.html',
        {'albums': Album.objects.all()}
    )


def get_thumbnail(request, album_id):
    album = Album.objects.get(id=album_id)
    thumbnail = os.path.join(album.path, album.thumbnail)

    thumb = cache.get(thumbnail)
    if not thumb:
        image = Image.open(io.BytesIO(sh.cat(thumbnail).stdout))
        thumb = ImageOps.fit(image, (800, 600), Image.ANTIALIAS)
        cache.hmset(
            'thumb:' + thumbnail,
            {'thumbnail': thumb, 'format': image.format}
        )

    print('*****', thumb.format)

    response = HttpResponse(content_type=Image.MIME[image.format])
    thumb.save(response, image.format)

    return response
