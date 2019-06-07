from django.core.management import BaseCommand

from bots.bots import TelegramBot
from yapp.settings.base import BOT_SETTINGS, MEDIA_ROOT


class Command(BaseCommand):
    help = 'Start Telegram messenger bot'

    def handle(self, *args, **options):
        token = BOT_SETTINGS.get('Token', None)
        if token is None:
            raise ValueError('No Telegram bot token defined')

        telegram_bot = TelegramBot(token, MEDIA_ROOT)
        telegram_bot.start()
        telegram_bot.join()
