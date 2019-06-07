import os

import qrcode
from django.apps import AppConfig

from yapp.settings.base import BOT_SETTINGS, BASE_DIR, STATIC_ROOT


class BotsConfig(AppConfig):
    name = 'bots'

    def ready(self):
        qr_code_content = BOT_SETTINGS['Contact'] if BOT_SETTINGS['Contact'] else 'No Bot Contact URL set'
        img = qrcode.make(qr_code_content)
        file_path = os.path.join(BASE_DIR, 'bots','static', 'bots', 'img', 'telegram-contact.png')
        img.save(file_path)
        file_path = os.path.join(STATIC_ROOT, 'bots', 'img', 'telegram-contact.png')
        if os.path.exists(file_path):
            img.save(file_path)
