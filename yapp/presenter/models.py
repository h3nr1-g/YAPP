from django.db import models


class Picture(models.Model):
    """
    Model class for the uploaded/ submitted party pictures
    """

    filePath = models.ImageField()
    title = models.CharField(
        max_length=200,
        blank=True,
        default=None,
        null=True,
    )
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
