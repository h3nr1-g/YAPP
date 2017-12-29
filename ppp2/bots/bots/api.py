from abc import ABC
from presenter.models import Picture


class ChatBot(ABC):
    """
    Abstract base class for all implemented chat bots
    """

    TEXT_BASED_COMMANDS = {
        'get': None,
        'set': None,
        'delete': None,
        'like': None,
        'dislike': None
    }

    @staticmethod
    def get_favourite_pictures(top_n=5):
        """
        Method fetches the TOP_N most liked pictures from the database
        :param top_n: Number of pictures
        :return: Queryset of pictures with the highest number of likes
        """
        pictures = Picture.objects.all().order_by('likes')
        return pictures if top_n >= len(pictures) else pictures[:top_n]

    @staticmethod
    def get_worst_pictures(top_n=5):
        """
        Method fetches the TOP_N most disliked pictures from the database
        :param top_n: Number of pictures
        :return: Queryset of pictures with the highest number of likes
        """
        pictures = Picture.objects.all().order_by('dislikes')
        return pictures if top_n >= len(pictures) else pictures[:top_n]

    @staticmethod
    def get_picture(id):
        """
        Method returns the picture with the requested ID

        :param id: Primary key/ ID of this picture
        :return: Instance of the picture or None if the ID does not exist
        """
        try:
            return Picture.objects.get(pk=id)
        except Picture.DoesNotExist:
            return None

    @staticmethod
    def add_like( id):
        """
        Method increases the number of likes for a picture by one

        :param id: ID/primary key of the picture
        :return: True if the incrementation was successful else False
        """
        try:
            picture = Picture.objects.get(pk=id)
            picture.likes += 1
            picture.save()
            return True
        except:
            return ChatBot.error_handler()

    @staticmethod
    def add_dislike( id):
        """
        Method increases the number of dislikes for a picture by one

        :param id: ID/primary key of the picture
        :return: True if the incrementation was successful else False
        """
        try:
            picture = Picture.objects.get(pk=id)
            picture.dislikes += 1
            picture.save()
            return True
        except:
            return ChatBot.error_handler()

    @staticmethod
    def set_title( id, title):
        """
        Method sets the title for the specified picture

        :param id: ID/primary key of the picture
        :param title: New title of the picture
        :return: True if the incrementation was successful else False
        """

        try:
            picture = Picture.objects.get(pk=id)
            picture.title = title
            picture.save()
            return True
        except:
            return ChatBot.error_handler()

    @staticmethod
    def error_handler():
        import traceback
        traceback.print_stack()
        return False
