import json
import os

from django.apps import AppConfig
from django.db.models.signals import post_save, pre_delete
from django.urls import reverse_lazy
from websocket import create_connection


def delete_obsolete_file(sender, instance, **kwargs):
    if os.path.exists(instance.filePath.path):
        os.remove(instance.filePath.path)


def publish_picture(instance, **kwargs):
    from yapp.settings.base import WS_BROKER_ADDRESS, WS_BROKER_PORT
    try:
        data = {
            'url': str(reverse_lazy('presenter:plain_picture', args=[instance.id])),
            'number': instance.id,
            'title': instance.title,
            'type': 'picture'
        }
        ws = create_connection("ws://{}:{}".format(WS_BROKER_ADDRESS, WS_BROKER_PORT))
        ws.send(json.dumps(data))
        ws.close()
    except ConnectionRefusedError:
        print('Could not establish WS connection for announcement of new picture')

def publish_video(instance, **kwargs):
    from yapp.settings.base import WS_BROKER_ADDRESS, WS_BROKER_PORT
    try:
        data = {
            'url': str(reverse_lazy('presenter:plain_picture', args=[instance.id])),
            'number': instance.id,
            'title': instance.title,
            'mimetype': instance.mimeType,
        }
        ws = create_connection("ws://{}:{}".format(WS_BROKER_ADDRESS, WS_BROKER_PORT))
        ws.send(json.dumps(data))
        ws.close()
    except ConnectionRefusedError:
        print('Could not establish WS connection for announcement of new picture')


class PresenterConfig(AppConfig):
    name = 'presenter'

    def ready(self):
        from presenter.models import Picture
        post_save.connect(publish_picture, sender=Picture)
        pre_delete.connect(delete_obsolete_file, sender=Picture)
