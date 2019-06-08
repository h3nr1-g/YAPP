from bots.api import get_worst_pictures, get_favourite_pictures, get_picture, set_title, add_like, add_dislike, show_help

STRING_DICTIONARY = {
    'ADDED_DISLIKE': 'Okay, I added a dislike to this picture.',
    'ADDED_LIKE': 'Okay, I added a like to this picture.',
    'EMPTY_DATABASE': 'Sorry, my database is empty. I need some pictures first.',
    'INTERNAL_ERROR': 'Ups, there wen\'t something wrong.',
    'INVALID_COMMAND': 'Sorry, I did not understand the last message',
    'HELP_INTRODUCTION': 'Hello, I\'m the Yapp-Telegrambot. Send me a photo and I will show it immediately. At the moment I accept a bunch of text based commands. You retrieve them via the text message "help".',
    'PICTURE_NOT_FOUND': 'Sorry, I could not find a picture with this ID.',
    'TITLE_UPDATE': 'Okay, I updated the title of this picture',
    'UPLOAD_FAILURE': 'Ups, upload failed',
    'UPLOAD_SUCCESS': 'Okay, thanks for the picture. I will store it with unique ID {}.',
}

COMMANDS = [
    {
        'callback': lambda tokens: get_worst_pictures(int(tokens[2]), STRING_DICTIONARY['EMPTY_DATABASE']),
        'description': 'Following command retrieves a list of the most disliked photos. Exampe: "get worst 3"',
        'regex': r'get worst \d+'
    },
    {
        'callback': lambda tokens: get_favourite_pictures(int(tokens[2]), STRING_DICTIONARY['EMPTY_DATABASE']),
        'description': 'Following command retrieves a list of the most favorite photos. Exampe: "get top 10"',
        'regex': r'get top \d+'
    },
    {
        'callback': lambda tokens: get_picture(int(tokens[2]), STRING_DICTIONARY['PICTURE_NOT_FOUND']),
        'description': 'Following command retrieves a specific picture (defined by it\'s ID). Exampe: "get picture 10"',
        'regex': r'get picture \d+'
    },
    {
        'callback': lambda tokens: set_title(
            int(tokens[4]),
            (' '.join(tokens[3:])).strip(),
            STRING_DICTIONARY['TITLE_UPDATE'],
            STRING_DICTIONARY['PICTURE_NOT_FOUND']
        ),
        'description': 'Following command changes the title of a specific picture (defined by it\'s ID). Exampe: "set title of picture"',
        'regex': r'set title of picture \d+: [a-z]+'
    },
    {
        'callback': lambda tokens: add_like(int(tokens[-1]), STRING_DICTIONARY['ADDED_LIKE']),
        'description': 'Following command adds a like to a specific picture (defined by it\'s ID). Exampe: "👍 picture 2"',
        'regex': r'👍 (picture )?\d+'
    },
    {
        'callback': lambda tokens: add_dislike(int(tokens[-1]), STRING_DICTIONARY['ADDED_DISLIKE']),
        'description': 'Following command adds a dislike to a specific picture (defined by it\'s ID). Exampe: "👎 picture 2"',
        'regex': r'👎 (picture )?\d+'
    },
    {
        'callback': lambda tokens: show_help(),
        'description': 'Following command sends you these help messages. Beispiel: "help"',
        'regex': r'help',
    },
    {
        'callback': lambda tokens: (True, STRING_DICTIONARY['HELP_INTRODUCTION']),
        'description': 'Following command shows an initial greeting message. Example: "/start"',
        'regex': r'/?start',
    },
]
