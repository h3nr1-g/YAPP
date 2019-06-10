from django.urls import path

from presenter.views import LiveModeView, AllPicturesView, PlainPictureView, RandomPictureView, UploadPictureView, \
    PlainVideoView, RandomMediaObjectView

urlpatterns = [
    path('live/', LiveModeView.as_view(), name='live'),
    path('pictures/random', RandomPictureView.as_view(), name='random_picture'),
    path('pictures/<int:picture_id>/plain', PlainPictureView.as_view(), name='plain_picture'),
    path('pictures/', AllPicturesView.as_view(), name='all_pictures'),
    path('pictures/upload/', UploadPictureView.as_view(), name='upload_picture'),

    # path('videos/random/', RandomVideoView.as_view(), name='random_video'),
    path('videos/<int:video_id>/plain/', PlainVideoView.as_view(), name='plain_video'),
    # path('videos/', AllVideoView.as_view(), name='all_videos'),
    # path('videos/upload/', UploadVideoView.as_view(), name='upload_video'),
    #
    path('random/', RandomMediaObjectView.as_view(), name='random_media_object'),
]
