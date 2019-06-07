from bots.api import get_worst_pictures, get_favourite_pictures, get_picture, set_title, add_like, add_dislike

STRING_DICTIONARY = {
    'ADDED_DISLIKE': 'Okay, ich habe dem Bild ein Dislike hinzugefügt.',
    'ADDED_LIKE': 'Okay, Ich habe dem Bild ein Like hinzugefügt.',
    'EMPTY_DATABASE': 'Ups, meine Datenbank ist noch leer. Ich benötigte erst ein paar Fotos',
    'INTERNAL_ERROR': 'Ups, da ist etwas schief gegangen.',
    'INVALID_COMMAND': 'Entschuldigung, ich habe Ihre letzte Nachricht nicht verstanden',
    'PICTURE_NOT_FOUND': 'Entschuldigung, ich konnte kein Bild mit dieser ID finden.',
    'TITLE_UPDATE': 'Okay, ich habe den Titel des Bildes aktualisiert.',
    'UPLOAD_FAILURE': 'Ups, der Upload ist fehlgeschlagen',
    'UPLOAD_SUCCESS': 'Danke für das Bild. Ich speichere es mit der ID {}.',
}

COMMANDS = [
    {
        'callback': lambda tokens: get_worst_pictures(int(tokens[4]), STRING_DICTIONARY['EMPTY_DATABASE']),
        'regex': r'gib mir die schlechtesten \d+ bilder'
    },
    {
        'callback': lambda tokens: get_favourite_pictures(int(tokens[4]), STRING_DICTIONARY['EMPTY_DATABASE']),
        'regex': r'gib mir die besten \d+ bilder'
    },
    {
        'callback': lambda tokens: get_picture(int(tokens[3]), STRING_DICTIONARY['PICTURE_NOT_FOUND']),
        'regex': r'gib mir bild \d+'
    },
    {
        'callback': lambda tokens: set_title(
            int(tokens[3].replace(':', '')),
            (' '.join(tokens[4:])).strip(),
            STRING_DICTIONARY['TITLE_UPDATE'],
            STRING_DICTIONARY['PICTURE_NOT_FOUND']
        ),
        'regex': r'titel für bild \d+: .+'
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
