import sys
from django.apps import AppConfig


class BotsConfig(AppConfig):
    name = 'bots'
    def ready(self):
        if 'runserver' in sys.argv:
            print('Start bots')
            from bots.bots import TelegramBot
            from ppp2.settings import BOT_CREDENTIALS, MEDIA_ROOT
            telegram_bot = TelegramBot(BOT_CREDENTIALS['Telegram'], MEDIA_ROOT)
            telegram_bot.start()
