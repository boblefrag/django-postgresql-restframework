from rest_framework import serializers
from rest_framework.relations import (StringRelatedField,
                                      HyperlinkedRelatedField)
from django.db.models import F, Func
from django.db.models import Value, CharField
from django.db.models.functions import Concat


class PostgreSQLListSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        return data.to_json()


class PostgreSQLModelSerializer(serializers.ModelSerializer):
    class Meta:
        list_serializer_class = PostgreSQLListSerializer


class PostgreSQLStringRelatedField(StringRelatedField):
    """
    Work exactly like StringRelatedField except it nicely create an
    annotate on the list qs for postgresql json export
    """
    def __init__(self, **kwargs):
        self.attr = kwargs.pop("attr")
        super(PostgreSQLStringRelatedField, self).__init__(**kwargs)

    def postgresql_queryset(self, queryset, **kwargs):
        print self.attr
        f = "{}__{}".format(self.source, self.attr)
        print f
        kwargs = {self.source: F(f)}
        print kwargs
        return queryset.annotate(**kwargs)


class PostgreSQLHyperLinkedField(HyperlinkedRelatedField):
    """
    Work exactly like StringRelatedField except it nicely create an
    annotate on the list qs for postgresql json export
    """
    def __init__(self, **kwargs):
        super(PostgreSQLHyperLinkedField, self).__init__(**kwargs)

    def postgresql_queryset(self, queryset, request=None):
        url = self.get_url(self.queryset.first(),
                           self.view_name,
                           request,
                           format='json')
        arg = getattr(self.queryset.first(), self.lookup_field)
        url_list = [Value(t) for t in url.split(str(arg))]
        f = F("{}__{}".format(self.source, self.lookup_field))
        url_list.insert(1, f)
        kwargs = {self.source: Concat(*url_list,
                                      output_field=CharField())
                  }
        return queryset.annotate(**kwargs)


class SingleNestedSerializer(StringRelatedField):
    """
    Nest a relation into the json response
    """
    def __init__(self, **kwargs):
        self.alias = kwargs.pop("alias")
        self.rel = kwargs.pop("rel")
        self.fields = kwargs.pop("fields")

        super(StringRelatedField, self).__init__(**kwargs)

    def postgresql_queryset(self, queryset, request=None):

        return queryset.nested_to_json(
            self.alias,
            self.fields,
            self.rel)
