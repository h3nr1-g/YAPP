import os
import shutil

from django.test import TestCase
from django.urls import reverse_lazy

from ppp2.settings import MEDIA_ROOT
from presenter.models import Picture


class OverviewViewTest(TestCase):
    """
    Test class for the view controller class OverviewView
    """

    def setUp(self):
        Picture.objects.create(
            filePath='/tmp/foo.png',
            title='Hello 12345',
            likes=10,
            dislikes=5
        )

        self.picture = Picture.objects.create(
            filePath='/tmp/abc.png',
            title='Moep Moep',
            likes=22,
            dislikes=11
        )

    def test_get(self):
        response = self.client.get(reverse_lazy('presenter:overview'))
        self.assertEqual(response.status_code, 200)


class LiveModeViewTest(TestCase):
    """
    Test class for the view controller class class LiveModeView
    """

    def setUp(self):
        dummy_file = os.path.dirname(os.path.realpath(__file__))
        dummy_file = os.path.join(dummy_file, 'dummydata', 'dummy.jpg')
        self.file_path = os.path.join(MEDIA_ROOT, 'foo.jpg')
        shutil.copy(dummy_file, self.file_path)

        self.picture = Picture.objects.create(
            filePath=self.file_path,
            title='Hey Ho',
            likes=1234,
            dislikes=123
        )

    def test_get(self):
        response = self.client.get(reverse_lazy('presenter:live'))
        self.assertEqual(response.status_code, 200)
        picture_url = reverse_lazy('presenter:picture', args=[self.picture.id])
        self.assertTrue(str(picture_url) in response.content.decode())

    def test_get_no_pictures(self):
        for p in Picture.objects.all():
            p.delete()
        response = self.client.get(reverse_lazy('presenter:live'))
        self.assertEqual(response.status_code, 200)


class SignalHandlerTest(TestCase):
    """
    Test class for the signal handler method
    """

    def setUp(self):
        dummy_file = os.path.dirname(os.path.realpath(__file__))
        dummy_file = os.path.join(dummy_file, 'dummydata', 'dummy.jpg')
        self.file_path = os.path.join(MEDIA_ROOT, 'foo.jpg')
        shutil.copy(dummy_file, self.file_path)

        self.picture = Picture.objects.create(
            filePath=self.file_path,
            title='Hey Ho',
            likes=1234,
            dislikes=123
        )

    def test_picture_deletion(self):
        self.assertTrue(os.path.exists(self.file_path))
        self.picture.delete()
        self.assertFalse(os.path.exists(self.file_path))


class PictureViewTest(TestCase):
    """
    Test class for the signal handler method
    """

    def setUp(self):
        dummy_file = os.path.dirname(os.path.realpath(__file__))
        dummy_file = os.path.join(dummy_file, 'dummydata', 'dummy.jpg')
        self.file_path = os.path.join(MEDIA_ROOT, 'foo.jpg')
        shutil.copy(dummy_file, self.file_path)

        self.picture = Picture.objects.create(
            filePath=self.file_path,
            title='Hey Ho',
            likes=1234,
            dislikes=123
        )

    def test_get(self):
        response = self.client.get(reverse_lazy('presenter:picture', args=[self.picture.id]))
        self.assertEqual(response.status_code, 200)

    def test_get_invalid_id(self):
        response = self.client.get(reverse_lazy('presenter:picture', args=[123456]))
        self.assertEqual(response.status_code, 404)

    def test_get_deleted_picture(self):
        os.remove(self.file_path)
        response = self.client.get(reverse_lazy('presenter:picture', args=[self.picture.id]))
        self.assertEqual(response.status_code, 404)
