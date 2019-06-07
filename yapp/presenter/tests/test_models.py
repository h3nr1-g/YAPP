import json
import os
from multiprocessing import Process
from time import sleep

from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer
from django.test import TestCase

from yapp.settings.base import WS_BROKER_PORT
from presenter.tests import create_sample_picture


class DummyBroker(WebSocket, TestCase):
    def handleMessage(self):
        try:
            self.assertIsInstance(self.data, str)
            keys = json.loads(self.data).keys()
            self.assertIn('url', keys)
            self.assertIn('number', keys)
            self.assertIn('title', keys)
            exit(0)
        except Exception as e:
            print(e)
            exit(2)


def run_broker():
    SimpleWebSocketServer('0.0.0.0', WS_BROKER_PORT, DummyBroker).serveforever()


class PostSaveSignalHandlerTest(TestCase):
    """
    Test class for the Picture class post-save callback function
    """

    def test_announcement_of_new_picture(self):
        broker_process = Process(target=run_broker)
        broker_process.start()
        sleep(0.1)
        create_sample_picture()
        sleep(0.2)
        if broker_process.is_alive():
            broker_process.terminate()
        broker_process.join()
        self.assertEqual(0, broker_process.exitcode)

    def test_file_deletion(self):
        picture_obj = create_sample_picture()
        self.assertTrue(os.path.exists(picture_obj.filePath.path))
        picture_obj.delete()
        self.assertFalse(os.path.exists(picture_obj.filePath.path))


class ModelStringTest(TestCase):
    """
    Test class for the string
    """

    def test_to_string(self):
        model_obj = create_sample_picture()
        self.assertEqual(model_obj.title, str(model_obj))
