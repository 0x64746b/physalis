from django.apps import AppConfig
from redis import StrictRedis


cache = None


class GalleryConfig(AppConfig):
    name = 'gallery'
    verbose_name = 'Physalis'

    def ready(self):
        global cache
        cache = StrictRedis('172.17.0.2')
