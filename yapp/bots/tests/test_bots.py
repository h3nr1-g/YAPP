from unittest import mock

from django.test import TestCase

from bots.bots import BaseBot
from presenter.models import Picture
from presenter.tests import create_sample_picture


class BaseBotTest(TestCase):
    """
    Test class for the class BaseBot
    """

    def setUp(self):
        self.bot = BaseBot()
        self.picture = create_sample_picture()

    def tearDown(self):
        for p in Picture.objects.all():
            p.delete()

    def test_process_message_invalid_message(self):
        success, _ = self.bot.process_message('foobar 1234')
        self.assertFalse(success)

    @mock.patch('bots.bots.BaseBot.get_callback')
    def test_process_message_missing_callback(self, mock_callback):
        mock_callback.return_value = None
        success, _ = self.bot.process_message('like 1234')
        self.assertFalse(success)

    def test_process_message_full_add_like(self):
        old_likes = self.picture.likes
        success, _ = self.bot.process_message('👍 {}'.format(self.picture.id))
        self.assertTrue(success)
        self.assertGreater(Picture.objects.get(id=self.picture.id).likes, old_likes)

    def test_process_message_change_title(self):
        old_title = self.picture.title
        success, _ = self.bot.process_message('set title {} foobar1234'.format(self.picture.id))
        self.assertTrue(success)
        self.assertNotEqual(Picture.objects.get(id=self.picture.id).title, old_title)
