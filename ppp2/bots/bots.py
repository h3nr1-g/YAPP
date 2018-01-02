import os
import re
from threading import Thread
from time import sleep
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater
from bots.api import COMMANDS
from presenter.models import Picture


class BaseBot():
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

        message = message.lower()
        if not self.check_command_syntax(message):
            return False, 'Sorry, I could not understand your message.'

        parts = message.split(' ')
        callback = self.get_callback(parts, COMMANDS)
        if callback is None:
            return False, 'Sorry, this command is not supported.'
        try:
            if 'set' in parts[0]:
                return callback(int(parts[-2]), parts[-1])
            else:
                return callback(int(parts[-1]))
        except:
            return False, 'Ups. Something went wrong.'

    def check_command_syntax(self, command):
        """
        Method itereates over all regular expressions (provided by build_regex_list()) and checks if one regex matches

        :param command: raw command
        :return: True if one of the regular expression matches else False
        """
        expressions = self.build_regex_list(COMMANDS)
        for expr in expressions:
            if re.match(expr, command):
                return True
        return False

    def build_regex_list(self, command_dictionary):
        """
        Method traverses the command set dictionary and builds a list with all regular expressions defined in the
        dictionary

        :param command_dictionary: Dictionary with the supported command set
        :return: List of the found regular expressions
        """
        regex_list = []
        for key in command_dictionary:
            if isinstance(command_dictionary[key], dict):
                regex_list += self.build_regex_list(command_dictionary[key])
            elif key == 'regex':
                regex_list.append(command_dictionary[key])
            else:
                continue
        return regex_list

    def get_callback(self, cmd_parts, cmd_dictionary):
        """
        Method traverses the command set dictionary and tries to find the right callback method

        :param cmd_parts: Command parts
        :param cmd_dictionary: Dictionary with the supported command set
        :return: Reference to the right callback method
        """
        try:
            if isinstance(cmd_dictionary[cmd_parts[0]], dict) and 'callback' in cmd_dictionary[cmd_parts[0]]:
                return cmd_dictionary[cmd_parts[0]]['callback']
            elif isinstance(cmd_dictionary[cmd_parts[0]], dict):
                callback = self.get_callback(cmd_parts[1:], cmd_dictionary[cmd_parts[0]])
                if callback is not None:
                    return callback
        except (KeyError, TypeError, IndexError):
            return None

    def new_picture(self, file):
        """
        Method creates a new database entry for the specified file

        :param file: Absolute path to the file
        :return: True, Instance of the created database entry or False, error message
        :rtype: tuple
        """
        try:
            return True, Picture.objects.create(filePath=file)
        except:
            import traceback
            traceback.print_exc()
            return False, 'Ups. Upload failed.'

    def generate_filename(self, directory, prefix):
        """
        Method generates an unique file name

        :param directory:
        :param prefix:
        :return:
        """
        post_fix = 0
        filename = '%s-%d.jpg' % (prefix, post_fix)
        filename = os.path.join(directory, filename)
        while os.path.exists(filename):
            post_fix += 1
            filename = '%s-%d.jpg' % (prefix, post_fix)
            filename = os.path.join(directory, filename)

        return filename


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

    def run(self):
        dispatcher = self.updater.dispatcher
        dispatcher.add_handler(MessageHandler(Filters.photo, self.new_photo_message))
        dispatcher.add_handler(MessageHandler(Filters.chat, self.new_text_message))
        self.updater.start_polling()
        while True:
            sleep(1)

    def new_photo_message(self, bot, update):
        """
        Call back method for incoming photo messages
        :param bot:
        :param update:
        :return: None
        """
        file_handler = bot.get_file(update.message.photo[-1].file_id)
        filename = super().generate_filename(self.download_directory, 'telegram')
        file_handler.download(filename)
        success, response = super().new_picture(filename)

        if success:
            update.message.reply_text('Thanks for the picture. It has the unique ID %d' % response.id)
        else:
            update.message.reply_text(response)

    def new_text_message(self, bot, update):
        """
        Call back method for incoming text messages

        :param bot:
        :param update:
        :return: None
        """
        _, response = super().process_message(update.message.text)
        if isinstance(response, str):
            update.message.reply_text(response)
        elif isinstance(response, Picture):
            bot.send_photo(chat_id=update.message.chat_id, photo=open(response.filePath.path, 'rb'))
        elif isinstance(response, list):
            update.message.reply_text('Here are the pictures')
            for element in response:
                bot.send_photo(chat_id=update.message.chat_id, photo=open(element.filePath.path, 'rb'))
