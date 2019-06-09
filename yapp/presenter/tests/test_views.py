import os

from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext
from django_webtest import WebTest
from webtest import Upload

from presenter.models import Picture
from presenter.tests import get_dummy_data_dir, create_sample_picture


class RandomPictureViewTest(TestCase):
    """
    Test class for the view class RandomPictureView
    """

    def tearDown(self):
        for picture in Picture.objects.all():
            picture.delete()

    def test_no_stored_pictures(self):
        response = self.client.get(reverse('presenter:random_picture'))
        self.assertEqual(404, response.status_code)

    def test_one_stored_picture(self):
        create_sample_picture()
        response = self.client.get(reverse('presenter:random_picture'))
        self.assertEqual(200, response.status_code)

    def test_one_stored_picture_as_json(self):
        create_sample_picture()
        response = self.client.get(reverse('presenter:random_picture') + '?json=1')
        self.assertEqual(200, response.status_code)
        json_data = response.json()
        self.assertIn('url', json_data.keys())
        self.assertIn('title', json_data.keys())
        self.assertIn('likes', json_data.keys())
        self.assertIn('dislikes', json_data.keys())


class UploadPictureViewTest(WebTest):
    """
    Test class for the view class UploadPictureView
    """

    def tearDown(self):
        for picture in Picture.objects.all():
            picture.delete()

    def test_get_page(self):
        response = self.app.get(reverse('presenter:upload_picture'))
        self.assertEqual(200, response.status_code)

    def test_post_invalid_data(self):
        response = self.app.get(reverse('presenter:upload_picture'))
        upload_form = response.forms[0]
        response = upload_form.submit(expect_errors=True)
        self.assertEqual(400, response.status_code)
        self.assertIn(gettext('Form contains invalid input.'), str(response))

    def test_post_valid_upload(self):
        self.assertEqual(0, len(Picture.objects.all()))
        response = self.app.get(reverse('presenter:upload_picture'))
        self.assertEqual(200, response.status_code)
        upload_form = response.forms[0]
        upload_form['filePath'] = Upload(os.path.join(get_dummy_data_dir(), 'sample.jpg'))
        upload_form['title'] = 'Foobar'
        response = upload_form.submit()
        self.assertEqual(200, response.status_code)
        self.assertIn(gettext('Picture saved'), str(response))
        self.assertEqual(1, len(Picture.objects.all()))
        self.assertTrue(os.path.exists(Picture.objects.all()[0].filePath.path))


class PlainPictureViewTest(TestCase):
    """
    Test class for the view class PlainPictureView
    """

    def tearDown(self):
        for picture in Picture.objects.all():
            picture.delete()

    def setUp(self):
        self.picture = create_sample_picture()

    def test_get_non_existing_picture(self):
        response = self.client.get(reverse('presenter:plain_picture', args=[1234]))
        self.assertEqual(404, response.status_code)

    def test_get_existing_picture(self):
        response = self.client.get(reverse('presenter:plain_picture', args=[self.picture.id]))
        self.assertEqual(200, response.status_code)
        self.assertGreater(len(response.content), 1000)


class AllPicturesViewTest(TestCase):
    """
    Test class for the view class AllPicturesView
    """

    def tearDown(self):
        for picture in Picture.objects.all():
            picture.delete()

    def test_get_no_pictures(self):
        response = self.client.get(reverse('presenter:all_pictures'))
        self.assertEqual(200, response.status_code)

    def test_get_existing_pictures(self):
        create_sample_picture()
        response = self.client.get(reverse('presenter:all_pictures'))
        self.assertEqual(200, response.status_code)


class LiveModeViewTest(TestCase):
    """
    Test class for the view class LiveModeView
    """

    def setUp(self):
        create_sample_picture()

    def tearDown(self):
        for picture in Picture.objects.all():
            picture.delete()

    def test_get_normal(self):
        response = self.client.get(reverse('presenter:live'))
        self.assertEqual(200, response.status_code)

    def test_get_fullscreen(self):
        response = self.client.get(reverse('presenter:live') + '?fullscreen=1')
        self.assertEqual(200, response.status_code)
