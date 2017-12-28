import random

from django.shortcuts import render
from django.views import View
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

        return render(request,'presenter/overview.html',context)

class LiveModeView(View):
    """
    View class for the live presentation of the uploaded pictures
    """

    def get(self,request):
        """
        Handler method for incoming GET requests

        :param request:
        :return:
        """
        pictures = Picture.objects.all()
        context = {
            'picture': random.choice(list(pictures)) if len(pictures) > 0 else None
        }

        return render(request, 'presenter/live.html', context)