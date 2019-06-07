from django.test import TestCase

from bots.api import get_favourite_pictures, get_worst_pictures, get_picture, add_like, add_dislike, set_title
from presenter.models import Picture
from presenter.tests import create_sample_picture


class APIFunctionsTest(TestCase):
    """
    Test class for the different API functions
    """

    def setUp(self):
        self.pic_1 = create_sample_picture()
        self.pic_1.likes = 10
        self.pic_1.dislikes = 10
        self.pic_1.save()
        self.pic_2 = create_sample_picture()
        self.pic_2.likes = 20
        self.pic_2.dislikes = 20
        self.pic_2.save()

    def test_get_favourite_pictures(self):
        result, top_pics = get_favourite_pictures(1)
        self.assertTrue(result)
        self.assertIsInstance(top_pics, list)
        self.assertEqual(1, len(top_pics))
        self.assertEqual(self.pic_2, top_pics[0])
        _, top_pics = get_favourite_pictures(2)
        self.assertEqual([self.pic_2, self.pic_1], top_pics)

    def test_get_worst_pictures(self):
        result, worst_pics = get_worst_pictures(1)
        self.assertTrue(result)
        self.assertIsInstance(worst_pics, list)
        self.assertEqual(1, len(worst_pics))
        self.assertEqual(self.pic_2, worst_pics[0])
        _, worst_pics = get_worst_pictures(2)
        self.assertEqual([self.pic_2, self.pic_1], worst_pics)

    def test_get_picture_valid_id(self):
        result, picture = get_picture(1)
        self.assertTrue(result)
        self.assertEqual(self.pic_1, picture)

    def test_get_picture_invalid_id(self):
        result, response = get_picture(12345, 'foobar')
        self.assertIsInstance(response, str)

    def test_add_like_valid_id(self):
        old_likes = self.pic_1.likes
        result, _ = add_like(1)
        self.assertTrue(result)
        self.assertGreater(Picture.objects.get(id=1).likes, old_likes)

    def test_add_like_id(self):
        result, _ = add_like(12345)
        self.assertFalse(result)

    def test_add_dislike_valid_id(self):
        old_dislikes = self.pic_1.dislikes
        result, _ = add_dislike(1)
        self.assertTrue(result)
        self.assertGreater(Picture.objects.get(id=1).dislikes, old_dislikes)

    def test_add_dislike_invalid_id(self):
        result, _ = add_dislike(12345)
        self.assertFalse(result)

    def test_set_title_valid_id(self):
        result, _ = set_title(1, 'moep moep')
        self.assertTrue(result)
        self.assertEqual('moep moep', Picture.objects.get(id=1).title)

    def test_set_title_invalid_id(self):
        result, _ = set_title(12345, 'blub')
        self.assertFalse(result)
