import os
import random

from django.db import models
import sh


class EmptyAlbumError(Exception):
    pass


class Source(models.Model):
    path = models.CharField(max_length=1024)

    def __init__(self, *args, **kwargs):
        super(Source, self).__init__(*args, **kwargs)

        self.ls = sh.ls.bake('-1', self.path)

    def index(self):
        nodes = [node.strip('\n') for node in self.ls()]

        for node in nodes:
            if os.path.isdir(os.path.join(self.path, node)):
                try:
                    Album(dir=node, source=self).save()
                except EmptyAlbumError:
                    continue

    def __str__(self):
        return self.path


class Album(models.Model):
    dir = models.CharField(max_length=512)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    thumbnail = models.CharField(max_length=1536)

    def __init__(self, *args, **kwargs):
        super(Album, self).__init__(*args, **kwargs)

        self.ls = sh.ls.bake('-1', os.path.join(self.source.path, self.dir))

        if not self.thumbnail:
            nodes = [node.strip('\n') for node in self.ls()]
            photos = [
                node for node in nodes
                if os.path.isfile(os.path.join(self.source.path, self.dir, node))
            ]
            if photos:
                self.thumbnail = photos[random.randint(0, len(photos)-1)]
            else:
                raise EmptyAlbumError('Directory {} contains no images'.format(self.dir))

    @property
    def path(self):
        return os.path.join(self.source.path, self.dir)

    def __str__(self):
        return self.dir
