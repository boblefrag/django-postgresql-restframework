from rest_framework import serializers
from rest_framework.relations import StringRelatedField
from django.db.models import F, Func


class PostgreSQLListSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        return data.to_json()


class PostgreSQLModelSerializer(serializers.ModelSerializer):
    class Meta:
        list_serializer_class = PostgreSQLListSerializer


class PostgreSQLStringRelatedField(StringRelatedField):

    def __init__(self, **kwargs):
        self.attr = kwargs.pop("attr")
        print "POEUT"
        super(PostgreSQLStringRelatedField, self).__init__(**kwargs)

    def postgresql_queryset(self, queryset):
        f = "{}__{}".format(self.source, self.attr)
        kwargs = {self.source: F(f)}
        return queryset.annotate(**kwargs)
