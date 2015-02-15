from rest_framework import serializers


class PostgreSQLListSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        return data.values(
            *(k for k in self.child.fields.iterkeys())
        ).to_json()


class PostgreSQLModelSerializer(serializers.ModelSerializer):
    class Meta:
        list_serializer_class = PostgreSQLListSerializer
