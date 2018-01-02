from presenter.models import Picture


def get_favourite_pictures(top_n=5):
    """
    Method fetches the TOP_N most liked pictures from the database
    :param top_n: Number of pictures
    :return: True, Queryset of pictures with the highest number of likes
    :rtype: tuple
    """
    pictures = Picture.objects.all().order_by('-likes', )
    pictures = pictures if top_n >= len(pictures) else pictures[:top_n]
    return True, pictures


def get_worst_pictures(top_n=5):
    """
    Method fetches the TOP_N most disliked pictures from the database
    :param top_n: Number of pictures
    :return: True, Queryset of pictures with the highest number of likes
    :rtype: tuple
    """
    pictures = Picture.objects.all().order_by('-dislikes')
    pictures = pictures if top_n >= len(pictures) else pictures[:top_n]
    return True, pictures


def get_picture(id):
    """
    Method returns the picture with the requested ID

    :param id: Primary key/ ID of this picture
    :return: True, Instance of the requested picture or False, Sorry, I could not find a picture with this ID.'
    :rtype: tuple
    """
    try:
        return True, Picture.objects.get(pk=id),
    except Picture.DoesNotExist:
        return False, 'Sorry, I could not find a picture with this ID.'


def add_like(id):
    """
    Method increases the number of likes for a picture by one

    :param id: ID/primary key of the picture
    :return: True, 'OK, I added +1 to the number of likes.' or False, Sorry, I could not find a picture with this ID.'
    :rtype: tuple
    """
    try:
        picture = Picture.objects.get(pk=id)
        picture.likes += 1
        picture.save()
        return True, 'OK, I added +1 to the number of likes.'
    except Picture.DoesNotExist:
        return False, 'Sorry, I could not find a picture with this ID.'


def add_dislike(id):
    """
    Method increases the number of dislikes for a picture by one

    :param id: ID/primary key of the picture
    :return: True,'OK, I added +1 to the number of dislikes.' or False,'Sorry, I could not find a picture with this ID.'
    :rtype: tuple
    """
    try:
        picture = Picture.objects.get(pk=id)
        picture.dislikes += 1
        picture.save()
        return True, 'OK, I added +1 to the number of dislikes.'
    except Picture.DoesNotExist:
        return False, 'Sorry, I could not find a picture with this ID.'


def set_title(id, title):
    """
    Method sets the title for the specified picture

    :param id: ID/primary key of the picture
    :param title: New title of the picture
    :return: True,'OK, I updated the title of this picture.' or False,'Sorry, I could not find a picture with this ID.'
    :rtype: tuple
    """

    try:
        picture = Picture.objects.get(pk=id)
        picture.title = title
        picture.save()
        return True, 'OK, I updated the title of this picture.'
    except Picture.DoesNotExist:
        return False, 'Sorry, I could not find a picture with this ID.'


COMMANDS = {
    'get': {
        'worst': {
            'callback': get_worst_pictures,
            'description': 'Command returns the worst pictures',
            'regex': r'get worst \d+'
        },
        'top': {
            'callback': get_favourite_pictures,
            'description': 'Command returns the most favorite pictures',
            'regex': r'get top \d+'
        },
        'picture': {
            'callback': get_picture,
            'description': 'Command returns the picture based  on the ID',
            'regex': r'get picture \d+'
        },
    },
    'set': {
        'title': {
            'callback': set_title,
            'description': 'Command sets the title for a given picture ID',
            'regex': r'set title \d+ [a-z]+'
        }
    },
    'like': {
        'callback': add_like,
        'description': 'Command adds a like',
        'regex': r'like \d+'
    },
    'dislike': {
        'callback': add_dislike,
        'description': 'Command adds a disklike',
        'regex': r'dislike \d+'
    }
}
