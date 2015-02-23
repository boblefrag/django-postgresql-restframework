from bookstore.models import Book, Editor

from postgresql_restframework.serializers import (PostgreSQLModelSerializer,
                                                  PostgreSQLStringRelatedField,
                                                  PostgreSQLHyperLinkedField,
                                                  SingleNestedSerializer)


class BookSerializer(PostgreSQLModelSerializer):
    editor = PostgreSQLHyperLinkedField(view_name="editor-detail",
                                        queryset=Editor.objects.all())
    genre = PostgreSQLStringRelatedField(attr="name")
    author = SingleNestedSerializer(read_only=True,
                                    alias='author',
                                    rel='author',
                                    fields=("username",
                                            "first_name",
                                            "last_name"))

    class Meta(PostgreSQLModelSerializer.Meta):
        model = Book
        fields = ('genre', 'editor', 'author')


class EditorSerializer(PostgreSQLModelSerializer):

    class Meta:
        model = Editor
        fields = ("pk",)
