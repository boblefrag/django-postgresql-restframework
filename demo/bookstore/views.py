from bookstore.models import Book
from bookstore.serializers import BookSerializer
from rest_framework import generics
from rest_framework import renderers
from rest_framework.utils import encoders
import json


class PostgreSQLRenderer(renderers.BaseRenderer):
    media_type = 'application/json'
    format = 'json'
    encoder_class = encoders.JSONEncoder

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Render `data` into JSON, returning a bytestring.
        """
        if data is None:
            return bytes()

        renderer_context = renderer_context or {}
        results = data.pop("results")
        data["results"] = {}
        ret = json.dumps(
            data, cls=self.encoder_class
        ).replace("{}", results)
        return ret


class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    renderer_classes = (PostgreSQLRenderer,)


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    paginate_by = 20
