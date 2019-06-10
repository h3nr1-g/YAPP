from django.utils.translation import gettext
from django_tables2 import tables, TemplateColumn, Column

from presenter.models import MediaObject


class PictureTable(tables.Table):
    timestamp = Column(verbose_name=gettext('Timestamp'))

    filePath = TemplateColumn(
        '<a href="{% url "presenter:plain_picture" record.id %}">'
        '<img width="100" src="{% url "presenter:plain_picture" record.id %}">'
        '</a>',
        verbose_name=gettext('Preview')
    )

    class Meta:
        model = MediaObject
        template_name = 'django_tables2/bootstrap4.html'
        sequence = ('filePath', 'title', 'likes', 'dislikes', 'timestamp')
        exclude = ('id','mimeType')
        attrs = {
            'style': 'width:100%;'
        }
