from bots.api import get_worst_pictures, get_favourite_pictures, get_picture, set_title, add_like, add_dislike, show_help

STRING_DICTIONARY = {
    'ADDED_DISLIKE': 'Okay, ich habe dem Bild ein Dislike hinzugefügt.',
    'ADDED_LIKE': 'Okay, Ich habe dem Bild ein Like hinzugefügt.',
    'EMPTY_DATABASE': 'Ups, meine Datenbank ist noch leer. Ich benötigte erst ein paar Fotos',
    'HELP_INTRODUCTION': 'Hallo, ich bin der Yapp-Telegrambot. Sende mir ein Foto und ich zeige es auf der Leinwand an. Außerdem unterstuetze diverse textbasierte Befehle, die du mit der Nachricht "/hilfe" abrufen kannst.',
    'INTERNAL_ERROR': 'Ups, da ist etwas schief gegangen.',
    'INVALID_COMMAND': 'Entschuldigung, ich habe Ihre letzte Nachricht nicht verstanden',
    'PICTURE_NOT_FOUND': 'Entschuldigung, ich konnte kein Bild mit dieser ID finden.',
    'TITLE_UPDATE': 'Okay, ich habe den Titel des Bildes aktualisiert.',
    'UPLOAD_FAILURE': 'Ups, der Upload ist fehlgeschlagen',
    'UPLOAD_SUCCESS': 'Danke für das Bild bzw. Video. Ich speichere es mit der ID {}.',
}

COMMANDS = [
    {
        'callback': lambda tokens: get_worst_pictures(int(tokens[3]), STRING_DICTIONARY['EMPTY_DATABASE']),
        'description': 'Folgender Befehl liefert eine Liste der Bilder mit den meisten Dislikes (sortiert in absteigender Reihenfolge). Beispiel: "gib mir die 5 schlechtesten bilder"',
        'regex': r'gib mir die \d+ schlechtesten bilder',
    },
    {
        'callback': lambda tokens: get_favourite_pictures(int(tokens[3]), STRING_DICTIONARY['EMPTY_DATABASE']),
        'description': 'Folgender Befehl liefert eine Liste der Bilder mit den meisten Likes (sortiert in absteigender Reihenfolge). Beispiel: "gib mir die 5 schoensten bilder"',
        'regex': r'gib mir die \d+ sch(oe|ö)nsten bilder',
    },
    {
        'callback': lambda tokens: get_picture(int(tokens[4]), STRING_DICTIONARY['PICTURE_NOT_FOUND']),
        'description': 'Folgender Befehl liefert das Bild mit der angegebenen ID. Beispiel: "gib mir das bild 3"',
        'regex': r'gib mir das bild \d+',
    },
    {
        'callback': lambda tokens: set_title(
            int(tokens[3].replace(':', '')),
            (' '.join(tokens[4:])).strip(),
            STRING_DICTIONARY['TITLE_UPDATE'],
            STRING_DICTIONARY['PICTURE_NOT_FOUND']
        ),
        'description': 'Folgender Befehl verändert den Titel für das Bild mit der angegebenen ID. Beispiel: "titel für bild 3: Hallo Welt"',
        'regex': r'titel für bild \d+: .+'
    },
    {
        'callback': lambda tokens: add_like(int(tokens[-1]), STRING_DICTIONARY['ADDED_LIKE']),
        'description': 'Folgender Befehl fügt dem Bild mit der angegebenen ID einen Like hinzu. Beispiel: "👍 bild 3"',
        'regex': r'👍 (bild )?\d+',
    },
    {
        'callback': lambda tokens: add_dislike(int(tokens[-1]), STRING_DICTIONARY['ADDED_DISLIKE']),
        'description': 'Folgender Befehl fügt dem Bild mit der angegebenen ID ein Dislike hinzu. Beispiel: "👎 bild 3"',
        'regex': r'👎 (bild )?\d+',
    },
    {
        'callback': lambda tokens: show_help(),
        'description': 'Folgender Befehl sendet dir diese Nachrichten. Beispiel: "hilfe"',
        'regex': r'/?hilfe',
    },
    {
        'callback': lambda tokens: (True, STRING_DICTIONARY['HELP_INTRODUCTION']),
        'description': 'Folgender Befehl sendet dir eine initiale Begrüßung. Beispiel: "/start"',
        'regex': r'/?start',
    },
]
