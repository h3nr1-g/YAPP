import logging

from django.core.management import BaseCommand
from yapp.settings.base import WS_BROKER_PORT
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('WSBroker')

clients = []


class UploadAnnouncement(WebSocket):

    def handleMessage(self):
        logger.info('Publish new message: {}'.format(str(self.data)))
        for client in clients:
            if client != self:
                client.sendMessage(self.data)

    def handleConnected(self):
        logger.info('Client connected')
        clients.append(self)

    def handleClose(self):
        clients.remove(self)
        logger.info('Client closed connection')


class Command(BaseCommand):
    help = 'Run Web Socket Broker for communication with web browsers'

    def add_arguments(self, parser):
        parser.add_argument(
            '--bind-address', '-b',
            type=str,
            default='0.0.0.0',
            help='Bind address for the web socket broker, default: 0.0.0.0'
        )

        parser.add_argument(
            '--port', '-p',
            type=int,
            default=WS_BROKER_PORT,
            help='Port for the web socket broker, default: {}'.format(WS_BROKER_PORT)
        )

    def handle(self, *args, **options):
        logger.info('Start Web Socket Broker at {}:{} ...'.format(options['bind_address'], options['port']))
        server = SimpleWebSocketServer(options['bind_address'], options['port'], UploadAnnouncement)
        server.serveforever()
