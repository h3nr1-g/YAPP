import os
import shutil

from yapp.settings.base import MEDIA_ROOT
from presenter.models import Picture


def get_dummy_data_dir():
    """
    Small helper method to provide the absolute path of the dummy data directory

    :return: Path of the dummy data directory
    :rtype: str
    """
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dummydata')


def create_sample_picture():
    """
    Small helper method for the creation of a DB entry

    :return: Created Picture class instance
    :rtype: Picture
    """

    picture_media_path = os.path.join(MEDIA_ROOT, 'sample.jpg')
    shutil.copy(os.path.join(get_dummy_data_dir(), 'sample.jpg'), picture_media_path)
    return Picture.objects.create(
        filePath=picture_media_path,
        title='Hello World',
        likes=1,
        dislikes=1,
    )
