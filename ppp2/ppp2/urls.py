from django.contrib import admin
from django.urls import include
from django.urls import path
from presenter.urls import urlpatterns as presenter_urls
from presenter import views as presenter_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('presenter/', include((presenter_urls, 'presenter'), namespace='presenter', )),
    path('', presenter_views.OverviewView.as_view()),  # URL for start page
]
