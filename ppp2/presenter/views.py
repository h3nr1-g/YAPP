import os
import random

from django.http import FileResponse
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views import View

from ppp2.settings import SECONDS_PER_PICTURE, BACKGROUND_COLOR, TITLE_FONT_COLOR, MAX_PICTURE_HEIGHT
from presenter.models import Picture
from presenter.tables import PictureTable


class OverviewView(View):
    """
    View controller for the overview page with the most popular and hated pictures
    """
    title = 'Overview'

    def get(self, request):
        """
        Handler method for incoming GET requests

        :param request:
        :return:
        """

        context = {
            'title': OverviewView.title,
            'table': PictureTable(Picture.objects.all().order_by('likes'))
        }

        return render(request, 'presenter/overview.html', context)


class LiveModeView(View):
    """
    View class for the live presentation of the uploaded pictures
    """

    def get(self, request):
        """
        Handler method for incoming GET requests

        :param request:
        :return:
        """
        pictures = Picture.objects.all()
        picture = random.choice(list(pictures)) if len(pictures) > 0 else None
        if len(pictures) > 0:
            title = picture.title + '  (Likes: %d \t Dislikes: %d)' % (picture.likes, picture.dislikes)
        else:
            title = None

        if request.GET.get('mode', None) == 'fullscreen':
            template = 'presenter/live_fullscreen.html'
        else:
            template = 'presenter/live.html'

        context = {
            'picture': picture,
            'title': 'Picture %d - %s' % (picture.id, title) if title is not None else None,
            'bg_color': BACKGROUND_COLOR,
            'title_color': TITLE_FONT_COLOR,
            'duration': SECONDS_PER_PICTURE,
            'max_height': MAX_PICTURE_HEIGHT,
        }

        return render(request, template, context)


class PictureView(View):
    """
    View class for the provision of the picture file
    """

    def get(self, request, number):
        """
        Handler method for incoming GET requests

        :param request:
        :param id:
        :return:
        """
        picture = get_object_or_404(Picture, pk=number)
        if not os.path.exists(picture.filePath.path):
            raise Http404()

        return FileResponse(open(picture.filePath.path, 'rb'), content_type='image/jpeg')
