from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        from bots.bots import TelegramBot
        from ppp2.settings import BOT_CREDENTIALS, MEDIA_ROOT

        telegram_bot = TelegramBot(BOT_CREDENTIALS['Telegram'], MEDIA_ROOT)
        telegram_bot.start()

        telegram_bot.join()
