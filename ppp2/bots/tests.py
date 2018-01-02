from unittest import TestCase, mock

import os

from bots.bots import BaseBot
from bots.api import COMMANDS, get_worst_pictures, get_favourite_pictures, get_picture, add_like, add_dislike, set_title
from ppp2.settings import MEDIA_ROOT
from presenter.models import Picture


class BaseBotTest(TestCase):
    """
    Test class for the chat bot base class
    """

    def setUp(self):
        self.bot = BaseBot()
        self.picture = Picture.objects.create(
            filePath='/tmp/foo.png',
            title='Hello 12345',
        )

    def test_get_callback_valid_command(self):
        callback = self.bot.get_callback(['get', 'worst', '5'], COMMANDS)
        self.assertEqual(get_worst_pictures, callback)

    def test_get_callback_invalid_command(self):
        callback = self.bot.get_callback(['foobar', 'foobar', '1234'], COMMANDS)
        self.assertIsNone(callback)

    def test_get_callback_incomplete_command(self):
        callback = self.bot.get_callback(['get'], COMMANDS)
        self.assertIsNone(callback)

    def test_get_callback_none_as_command(self):
        callback = self.bot.get_callback(None, COMMANDS)
        self.assertIsNone(callback)

    def test_build_regex_list(self):
        regex_list = self.bot.build_regex_list(COMMANDS)
        self.assertGreater(len(regex_list), len(COMMANDS))

    def test_check_commad_syntax_valid_command(self):
        self.assertTrue(self.bot.check_command_syntax('get worst 5'))

    def test_check_commad_syntax_invalid_command(self):
        self.assertFalse(self.bot.check_command_syntax('get foobar 1234 foobar'))

    def test_message_processing_valid_command(self):
        success, picture = self.bot.process_message('get picture %d' % self.picture.id)
        self.assertTrue(success)
        self.assertEqual(picture.id, self.picture.id)

    def test_message_processing_valid_command2(self):
        success, _ = self.bot.process_message('set title %d moep-moep' % self.picture.id)
        self.assertTrue(success)
        self.assertEqual(Picture.objects.get(pk=self.picture.id).title, 'moep-moep')

    def test_message_processing_invalid_command(self):
        success, response = self.bot.process_message('get foobar foobar %d aaaaa' % self.picture.id)
        self.assertFalse(success)
        self.assertTrue(isinstance(response, str))

    def test_message_processing_with_exception(self):
        with mock.patch('presenter.models.Picture.objects.all') as fail_function:
            fail_function.side_effect = Exception()
            success, response = self.bot.process_message('get top 5')
            self.assertFalse(success)
            self.assertTrue(isinstance(response, str))

    def test_new_photo(self):
        success, response = self.bot.new_picture('/tmp/blub.png')
        self.assertTrue(success)
        self.assertTrue(isinstance(response, Picture))

    def test_new_photo_failure(self):
        with mock.patch('presenter.models.Picture.objects.create') as fail_function:
            fail_function.side_effect = Exception()
            success, response = self.bot.new_picture('/tmp/blub.png')
        self.assertFalse(success)
        self.assertTrue(isinstance(response, str))

    def test_generate_filename(self):
        with mock.patch('os.path.exists') as mock_exists:
            mock_exists.side_effect = [True, True, False]
            filename = self.bot.generate_filename('/tmp', 'foo')
            self.assertTrue('/tmp/foo-2' in filename)


class APIMethodsTest(TestCase):
    """
    Test class for the API methods
    """

    def setUp(self):
        for p in Picture.objects.all():
            p.delete()

        Picture.objects.create(
            filePath=os.path.join(MEDIA_ROOT, 'foo.png'),
            title='Hello 12345',
            likes=10,
            dislikes=5
        )

        self.picture = Picture.objects.create(
            filePath=os.path.join(MEDIA_ROOT, 'abc.png'),
            title='Moep Moep',
            likes=22,
            dislikes=11
        )

    def test_get_favourite_pictures(self):
        success, pictures = get_favourite_pictures(top_n=3)
        self.assertTrue(success)
        self.assertEqual(len(pictures), len(Picture.objects.all()))
        self.assertGreater(pictures[0].likes, pictures[1].likes)

    def test_get_worst_pictures(self):
        success, pictures = get_worst_pictures(top_n=3)
        self.assertTrue(success)
        self.assertEqual(len(pictures), len(Picture.objects.all()))
        self.assertGreater(pictures[0].likes, pictures[1].likes)

    def test_get_picture(self):
        success, picture = get_picture(self.picture.id)
        self.assertTrue(success)
        self.assertEqual(self.picture.id, picture.id)

    def test_get_picture_invalid_id(self):
        success, response = get_picture(12345)
        self.assertFalse(success)
        self.assertTrue(isinstance(response, str))

    def test_add_like(self):
        success, response = add_like(self.picture.id)
        self.assertTrue(success)
        self.assertNotEqual(self.picture.likes, Picture.objects.get(pk=self.picture.id).likes)

    def test_add_like_invalid_id(self):
        success, response = add_like(12345)
        self.assertFalse(success)
        self.assertTrue(isinstance(response, str))

    def test_add_dislike(self):
        success, response = add_dislike(self.picture.id)
        self.assertTrue(success)
        self.assertNotEqual(self.picture.dislikes, Picture.objects.get(pk=self.picture.id).dislikes)

    def test_add_dislike_invalid_id(self):
        success, response = add_dislike(12345)
        self.assertFalse(success)
        self.assertTrue(isinstance(response, str))

    def test_set_title(self):
        success, response = set_title(self.picture.id, 'new-title')
        self.assertTrue(success)
        self.assertEqual(Picture.objects.get(pk=self.picture.id).title, 'new-title')

    def test_set_title_invalid_id(self):
        success, response = set_title(12345, 'new-title')
        self.assertFalse(success)
        self.assertTrue(isinstance(response, str))
