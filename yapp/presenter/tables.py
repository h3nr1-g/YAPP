from django_tables2 import tables, TemplateColumn, Column

from presenter.models import Picture

DELETE_BUTTON_TEMPLATE = '<button onclick=\'ajax_delete_and_reload("{}")\' class="btn btn-danger">Löschen</button>'
DETAILS_BUTTON_TEMPLATE = '<a href="{}"><button class="btn btn-info">Anzeigen</button></a>'


class PictureTable(tables.Table):
    timestamp = Column(verbose_name='Uploaddatum')

    filePath = TemplateColumn(
        '<a href="{% url "presenter:plain_picture" record.id %}">'
        '<img width="100" src="{% url "presenter:plain_picture" record.id %}">'
        '</a>',
        verbose_name='Vorschau'
    )

    class Meta:
        model = Picture
        template_name = 'django_tables2/bootstrap4.html'
        sequence = ('filePath', 'title', 'likes', 'dislikes', 'timestamp')
        exclude = ('id',)
        attrs = {
            'style': 'width:100%;'
        }
