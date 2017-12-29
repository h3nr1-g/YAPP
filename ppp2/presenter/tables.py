from django_tables2 import Column
from django_tables2 import TemplateColumn
from django_tables2 import tables

from presenter import models


class PictureTable(tables.Table):
    """
    Table class for displaying of all uploaded photos
    """

    filePath = TemplateColumn('<img src="{% url \"presenter:picture\" record.id %}" width="100", height="100">')
    title = Column('Title')
    likes = Column('Likes')
    dislikes = Column('Dislikes')
    timestamp = Column('Uploaded at')

    class Meta:
        attrs = {'class': 'table table-hover'}
        model = models.Picture
        fields = ('filePath', 'title', 'likes', 'dislikes', 'timestamp')
