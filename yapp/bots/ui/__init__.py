import importlib
from yapp.settings.base import LANGUAGE_CODE

module = importlib.import_module('bots.ui.' + LANGUAGE_CODE.lower())
COMMANDS = getattr(module, 'COMMANDS')
STRING_DICTIONARY = getattr(module, 'STRING_DICTIONARY')
