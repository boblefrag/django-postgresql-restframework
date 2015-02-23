from bookstore.models import Book, Editor
from bookstore.serializers import BookSerializer, EditorSerializer
from rest_framework import generics
from rest_framework import renderers
from rest_framework.utils import encoders
from django.db.models import F, Func
from django.db.models.functions import Concat
from django.db.models import Value as V, CharField
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

    def get_queryset(self):
        """
        Depending on the type of the self.serializer_class().fields we
        should construct the right qs with the needed annotate

        Obviously this work should take place in postgresql_restframework
        """

        for k, v in self.serializer_class().fields.iteritems():
            if hasattr(v, "postgresql_queryset"):
                self.queryset = getattr(v,
                                        "postgresql_queryset")(
                                            self.queryset,
                                            request=self.request)

        args = [k for k in self.serializer_class().fields.iterkeys()]
        return self.queryset.values(*args)


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    paginate_by = 20


class EditorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Editor.objects.all()
    serializer_class = EditorSerializer
    paginate_by = 20
