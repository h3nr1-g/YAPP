import logging
import os
import re
from threading import Thread
from time import sleep, time
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater
from bots.ui import COMMANDS, STRING_DICTIONARY
from presenter.models import Picture, Video

logging.basicConfig(level=logging.INFO)
_TELEGRAM_LOGGER = logging.getLogger('TelegramBot')


class BaseBot:
    """
    Base class for all implemented chat bots
    """

    def process_message(self, message):
        """
        Generic processing methods for incoming messages/commands

        :param message: Command message
        :return: True, Requested resources or False, Error description
        :rtype: tuple
        """

        message = message.lower().strip()
        callback = self.get_callback(message)
        if not callback:
            return False, STRING_DICTIONARY['INVALID_COMMAND']
        return callback(message.split(' '))

    def get_callback(self, message):
        """
        Method iterates of the languages specific command list and tries to find a suitable callback method for the
        received message

        :param message: Stripped and lowered text message
        :type message: str
        :return: Reference to the right callback method or None if no suitable callback method could be found
        """
        for entry in COMMANDS:
            if re.match(entry['regex'], message) is not None:
                return entry['callback']
        return None


class TelegramBot(BaseBot, Thread):
    """
    Chat bot for Telegram
    """

    def __init__(self, token, download_directory):
        super().__init__()
        self.daemon = True
        self.updater = Updater(token)
        self.download_directory = download_directory
        self.post_fix = 0
        self.logger = _TELEGRAM_LOGGER

    def run(self):
        os.makedirs(self.download_directory, exist_ok=True)
        dispatcher = self.updater.dispatcher
        dispatcher.add_handler(MessageHandler(Filters.photo, self.new_photo_message))
        dispatcher.add_handler(MessageHandler(Filters.chat, self.new_text_message))
        self.updater.start_polling()
        self.logger.info('Bot started')
        while True:
            sleep(1)

    def new_photo_message(self, bot, update):
        """
        Call back method for incoming photo messages
        :param bot:
        :param update:
        :return: None
        """
        self.logger.info('Received new photo')
        file_handler = bot.get_file(update.message.photo[-1].file_id)
        filename = 'telegram_{}.jpg'.format(int(time()))
        filename = os.path.join(self.download_directory, filename)
        try:
            file_handler.download(filename)
            picture_obj = Picture.objects.create(filePath=filename)
            self.logger.info('Photo stored')
            self.logger.debug('Photo ID {}'.format(picture_obj.id))
            self.send_response(bot, update, STRING_DICTIONARY['UPLOAD_SUCCESS'].format(picture_obj.id))
        except Exception as e:
            self.logger.error('Processing of photo failed: {}'.format(str(e)))
            update.message.reply_text(STRING_DICTIONARY['UPLOAD_FAILURE'])

    def new_text_message(self, bot, update):
        """
        Call back method for incoming text messages

        :param bot:
        :param update:
        :return: None
        """
        try:
            self.logger.info('Received new text message')
            if update.message.text:
                self.logger.debug('Message text: {}'.format(update.message.text))
                _, response = super().process_message(update.message.text)
                self.logger.info('Message processed successfully')
                self.send_response(bot, update, response)
            if update.message.video:
                file_handler = bot.get_file(update.message.video.file_id)
                filename = 'telegram_{}.{}'.format(int(time()), update.message.video.mime_type.split('/')[-1])
                filename = os.path.join(self.download_directory, filename)
                try:
                    file_handler.download(filename)
                    picture_obj = Video.objects.create(
                        filePath=filename,
                        mimeType=update.message.video.mime_type,
                    )
                    self.logger.info('Video stored')
                    self.logger.debug('Video ID {}'.format(picture_obj.id))
                    self.send_response(bot, update, STRING_DICTIONARY['UPLOAD_SUCCESS'].format(picture_obj.id))
                except Exception as e:
                    self.logger.error('Processing of video failed: {}'.format(str(e)))
                    update.message.reply_text(STRING_DICTIONARY['UPLOAD_FAILURE'])
        except Exception as e:
            self.logger.error('Processing of message failed: {}'.format(str(e)))

    def send_response(self, bot, update, response):
        if isinstance(response, str):
            self.logger.debug('Send text message: {}'.format(response))
            update.message.reply_text(response)

        elif isinstance(response, Picture):
            self.logger.debug('Send photo with ID: {}'.format(response.id))
            bot.send_photo(chat_id=update.message.chat_id, photo=open(response.filePath.path, 'rb'))

        elif isinstance(response, list):
            for element in response:
                self.send_response(bot, update, element)