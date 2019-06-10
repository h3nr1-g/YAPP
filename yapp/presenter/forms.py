from django import forms
from django.utils.translation import gettext

from presenter.models import Picture


class PictureUploadForm(forms.ModelForm):
    """
    Model form for uploading pictures
    """

    filePath = forms.ImageField(
        label=gettext('File'),
    )
    title = forms.CharField(
        required=False,
        label=gettext('Title')
    )
    likes = forms.HiddenInput()
    dislikes = forms.HiddenInput()
    timestamp = forms.HiddenInput()
    mimeType = forms.HiddenInput()

    class Meta:
        model = Picture
        fields = ('title', 'filePath',)
