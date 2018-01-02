import os
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from django.urls import reverse_lazy
from presenter.models import Picture
from omnibus.api import publish


@receiver(pre_delete, sender=Picture)
def delete_obsolete_file(sender, **kwargs):
    if os.path.exists(kwargs['instance'].filePath.path):
        os.remove(kwargs['instance'].filePath.path)


@receiver(post_save, sender=Picture)
def publish_picture(sender, **kwargs):
    data = {
        'url': str(reverse_lazy('presenter:picture', args=[kwargs['instance'].id])),
        'number': kwargs['instance'].id,
    }
    publish('updates', 'pictures', data)
