from bookstore.models import Book
from postgresql_restframework.serializers import PostgreSQLModelSerializer


class BookSerializer(PostgreSQLModelSerializer):
    class Meta(PostgreSQLModelSerializer.Meta):
        model = Book
        fields = ('title', 'author', 'genre', 'editor', 'store', 'price')
