from django.urls import re_path
from presenter.views import OverviewView, LiveModeView

urlpatterns = [
    # URL for the overview page
    re_path('^overview/$', OverviewView.as_view(), name='overview'),
    # URL for the live presentation mode
    re_path('^live/$', LiveModeView.as_view(), name='live'),

]