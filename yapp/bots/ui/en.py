from bots.api import get_worst_pictures, get_favourite_pictures, get_picture, set_title, add_like, add_dislike

STRING_DICTIONARY = {
    'ADDED_DISLIKE': 'Okay, I added a dislike to this picture.',
    'ADDED_LIKE': 'Okay, I added a like to this picture.',
    'EMPTY_DATABASE': 'Sorry, my database is empty. I need some pictures first.',
    'INTERNAL_ERROR': 'Ups, there wen\'t something wrong.',
    'INVALID_COMMAND': 'Sorry, I did not understand the last message',
    'PICTURE_NOT_FOUND': 'Sorry, I could not find a picture with this ID.',
    'TITLE_UPDATE': 'Okay, I updated the title of this picture',
    'UPLOAD_FAILURE': 'Ups, upload failed',
    'UPLOAD_SUCCESS': 'Okay, thanks for the picture. I will store it with unique ID {}.',
}

COMMANDS = [
    {
        'callback': lambda tokens: get_worst_pictures(int(tokens[2]), STRING_DICTIONARY['EMPTY_DATABASE']),
        'regex': r'get worst \d+'
    },
    {
        'callback': lambda tokens: get_favourite_pictures(int(tokens[2]), STRING_DICTIONARY['EMPTY_DATABASE']),
        'regex': r'get top \d+'
    },
    {
        'callback': lambda tokens: get_picture(int(tokens[2]), STRING_DICTIONARY['PICTURE_NOT_FOUND']),
        'regex': r'get picture \d+'
    },
    {
        'callback': lambda tokens: set_title(
            int(tokens[2]),
            (' '.join(tokens[3:])).strip(),
            STRING_DICTIONARY['TITLE_UPDATE'],
            STRING_DICTIONARY['PICTURE_NOT_FOUND']
        ),
        'regex': r'set title \d+ [a-z]+'
    },
    {
        'callback': lambda tokens: add_like(int(tokens[1]), STRING_DICTIONARY['ADDED_LIKE']),
        'regex': r'👍 \d+'
    },
    {
        'callback': lambda tokens: add_dislike(int(tokens[1]), STRING_DICTIONARY['ADDED_DISLIKE']),
        'regex': r'👎 \d+'
    },
]
