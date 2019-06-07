

from django.contrib import admin
from django.urls import path, include

from presenter.views import LiveModeView

urlpatterns = [
    path('', LiveModeView.as_view()),
    path('admin/', admin.site.urls),
    path('presenter/', include(('presenter.urls', 'presenter'), namespace='presenter')),
]
