from django.urls import path

from presenter.views import LiveModeView, AllPicturesView, PlainPictureView, RandomPictureView, UploadPictureView

urlpatterns = [
    path('live/', LiveModeView.as_view(), name='live'),
    path('pictures/random', RandomPictureView.as_view(), name='random_picture'),
    path('pictures/<int:picture_id>/plain', PlainPictureView.as_view(), name='plain_picture'),
    path('pictures/', AllPicturesView.as_view(), name='all_pictures'),
    path('pictures/upload', UploadPictureView.as_view(), name='upload_picture'),
]
