from presenter.models import Picture


def get_favourite_pictures(top_n, fail_msg=None):
    """
    Method returns a list with the most favorite pictures

    :param top_n: Number of elements
    :type top_n: int
    :return: Tuple of bool flag for indication of success and requested list of pictures
    :rtype: tuple
    """
    pictures = list(Picture.objects.all().order_by('-likes', ))
    pictures = pictures if top_n >= len(pictures) else pictures[:top_n]
    if len(pictures) < 1:
        return True, fail_msg

    return True, pictures


def get_worst_pictures(top_n, fail_msg=None):
    """
    Method returns a list with the most disliked pictures

    :param top_n: Number of elements
    :type top_n: int
    :return: Tuple of bool flag for indication of success and requested list of pictures
    :rtype: tuple
    """
    pictures = list(Picture.objects.all().order_by('-dislikes'))
    pictures = pictures if top_n >= len(pictures) else pictures[:top_n]
    if len(pictures) < 1:
        return True, fail_msg

    return True, pictures


def get_picture(pid, fail_msg=None):
    """
    Method fetches the requested picture from the database

    :param pid: ID of the requested picture
    :type pid: int
    :return: Tuple of bool flag for indication of success and the requested picture or an error message
    :rtype: tuple
    """
    try:
        return True, Picture.objects.get(pk=pid),
    except Picture.DoesNotExist:
        return False, fail_msg


def add_like(pid, success_msg=None, fail_msg=None):
    """
    Method increases the number of likes by one for the requested picture

    :param pid: ID of the picture
    :type pid: int
    :return: Tuple of bool flag for indication of success and a response text message
    :rtype: tuple
    """
    try:
        picture = Picture.objects.get(pk=pid)
        picture.likes += 1
        picture.save()
        return True, success_msg
    except Picture.DoesNotExist:
        return False, fail_msg


def add_dislike(pid, success_msg=None, fail_msg=None):
    """
    Method increases the number of dislikes by one for the requested picture

    :param pid: ID of the picture
    :type pid: int
    :return: Tuple of bool flag for indication of success and a response text message
    :rtype: tuple
    """
    try:
        picture = Picture.objects.get(pk=pid)
        picture.dislikes += 1
        picture.save()
        return True, success_msg
    except Picture.DoesNotExist:
        return False, fail_msg


def set_title(pid, title, success_msg=None, fail_msg=None):
    """
    Method changes the title for requested picture

    :param pid: ID of the picture
    :type pid: int
    :param title: New title of the picture
    :type title: str
    :return: Tuple of bool flag for indication of success and a response text message
    :rtype: tuple
    """
    try:
        picture = Picture.objects.get(pk=pid)
        picture.title = title
        picture.save()
        return True, success_msg
    except Picture.DoesNotExist:
        return False, fail_msg
