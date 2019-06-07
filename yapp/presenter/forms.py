from django import forms

from presenter.models import Picture


class PictureUploadForm(forms.ModelForm):
    """
    Model form for uploading pictures
    """

    filePath = forms.ImageField(
        label='Datei',
    )
    title = forms.CharField(
        required=False,
        label='Titel'
    )
    likes = forms.HiddenInput()
    dislikes = forms.HiddenInput()
    timestamp = forms.HiddenInput()

    class Meta:
        model = Picture
        fields = ('title', 'filePath',)
