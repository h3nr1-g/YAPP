from django.db import models


class MediaObject(models.Model):
    """
    Base class for picture and video objects
    """

    filePath = models.FileField()
    title = models.CharField(
        max_length=200,
        blank=True,
        default=None,
        null=True,
    )
    mimeType= models.CharField(
        max_length=200,
        blank=True,
        default=None,
        null=True,
    )
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title if self.title else 'No Title'

    class Meta:
        abstract = True


class Picture(MediaObject):
    """
    Model class for the uploaded/ submitted party pictures
    """


class Video(MediaObject):
    """
    Model class for the uploaded/ submitted party pictures
    """