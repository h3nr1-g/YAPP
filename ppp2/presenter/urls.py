from django.conf.urls import url
from django.urls import path
from presenter.views import OverviewView, LiveModeView, PictureView

urlpatterns = [
    # URL for the live presentation mode
    path('pictures/<int:number>/', PictureView.as_view(), name='picture'),
    # URL for the overview page
    path('overview/', OverviewView.as_view(), name='overview'),
    # URL for the live presentation mode
    path('live/', LiveModeView.as_view(), name='live'),

]