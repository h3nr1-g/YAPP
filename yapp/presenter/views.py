import os
import random

from django.http import HttpResponseNotFound, HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse_lazy
from django.views import View

from yapp.settings.base import WS_BROKER_PORT, WS_BROKER_ADDRESS, BOT_SETTINGS
from presenter.forms import PictureUploadForm
from presenter.models import Picture
from presenter.tables import PictureTable


class LiveModeView(View):
    """
    View class for the start page
    """
    title = 'Party Picture Presenter 2.0'

    def get(self, request):
        fullscreen = request.GET.get('fullscreen', None)
        context = {
            'title': self.title,
            'ws_broker_port': WS_BROKER_PORT,
            'ws_broker_address': WS_BROKER_ADDRESS,
            'bot_contact': BOT_SETTINGS['Contact'],
            'seconds_per_picture': int(request.GET.get('secondsPerPicture', '3'))
        }
        template = 'presenter/live_fullscreen.html' if fullscreen else 'presenter/live.html'
        return render(request, template, context)


class AllPicturesView(View):
    """
    View class for list of all pictures
    """
    title = 'Bilder - Alle'

    def get(self, request):
        context = {
            'title': self.title,
            'table': PictureTable(Picture.objects.all().order_by(request.GET.get('sort', '-timestamp')))
        }
        return render(request, 'presenter/all_pictures.html', context)


class PlainPictureView(View):
    """
    View class for providing only the picture
    """

    def get(self, request, picture_id):
        picture_obj = get_object_or_404(Picture, pk=picture_id)
        if not os.path.exists(picture_obj.filePath.path):
            return HttpResponseNotFound()
        with open(picture_obj.filePath.path, 'rb') as fh:
            resp = HttpResponse(fh.read(), content_type='image/jpeg')
        return resp


class RandomPictureView(View):
    """
    View class for the provision of a random picture
    """

    def get(self, request):

        all_pictures = list(Picture.objects.all())
        while len(all_pictures) > 0:
            picture_obj = all_pictures[random.randint(0, len(all_pictures) - 1)]
            if not os.path.exists(picture_obj.filePath.path):
                continue
            if request.GET.get('json', None):
                return JsonResponse({
                    'url': str(reverse_lazy('presenter:plain_picture', args=[picture_obj.id])),
                    'title': picture_obj.title,
                    'likes': picture_obj.likes,
                    'dislikes': picture_obj.dislikes,
                })

            with open(picture_obj.filePath.path, 'rb') as fh:
                resp = HttpResponse(fh.read(), content_type='image/jpeg')
            return resp
        return HttpResponseNotFound()


class UploadPictureView(View):
    """
    View class for manual uploading of a picture
    """
    title = 'Bild hochladen'

    def get(self, request):
        context = {
            'title': self.title,
            'form': PictureUploadForm(),
        }
        return render(request, 'presenter/upload.html', context)

    def post(self, request):
        form = PictureUploadForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            response_class = HttpResponse
            notification = (True, 'Bild erfolgreich gespeichert.')
        else:
            notification = (False, 'Formular enthaelt fehlerhafte Eingaben. Bitte Eingaben pruefen.')
            response_class = HttpResponseBadRequest

        context = {
            'form': form,
            'title': self.title,
            'notification': notification,
        }
        template = loader.get_template('presenter/upload.html')
        return response_class(template.render(context, request))
