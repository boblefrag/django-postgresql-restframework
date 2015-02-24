from collections import OrderedDict

from django.db import models, connection
from django.db.models.fields.related import ForeignKey
from psycopg2 import extras


extras.register_default_json(loads=lambda x: x)


class PostgreSQLManager(models.Manager):

    def get_queryset(self):
        return PostgreSQLQuerySet(self.model, using=self._db)

    def to_json(self):
        return self.get_queryset().to_json()


class PostgreSQLQuerySet(models.QuerySet):

    def to_json(self):
        template = """
        select array_to_json(array_agg(row_to_json(t)))
        FROM({}) t"""
        sql = self.query.sql_with_params()
        args = (template.format(sql[0]),
                sql[1])

        with connection.cursor() as c:
            c.execute(*args)
            result = c.fetchone()[0]
        return result

    def annotate(self, *args, **kwargs):
        """
        Override Django annotate to allow annotate alias be a model field name
        """
        annotations = OrderedDict()  # To preserve ordering of args
        for arg in args:
            try:
                # we can't do an hasattr here because py2 returns False
                # if default_alias exists but throws a TypeError
                if arg.default_alias in kwargs:
                    raise ValueError(
                        "The named annotation '%s' conflicts with the "
                        "default name for another annotation."
                        % arg.default_alias)
            except AttributeError:  # default_alias
                raise TypeError("Complex annotations require an alias")
            annotations[arg.default_alias] = arg
        annotations.update(kwargs)

        obj = self._clone()
        names = getattr(self, '_fields', None)
        if names is None:
            names = {f.name for f in self.model._meta.get_fields()}

        # Add the annotations to the query
        for alias, annotation in annotations.items():
            obj.query.add_annotation(annotation, alias, is_summary=False)
        # expressions need to be added to the query before we know if
        # they contain aggregates
        added_aggregates = []
        for alias, annotation in obj.query.annotations.items():
            if alias in annotations and annotation.contains_aggregate:
                added_aggregates.append(alias)
        if added_aggregates:
            obj._setup_aggregate_query(list(added_aggregates))

        return obj

    def nested_to_json(self, alias, fields, rel):
        """return the queryset with a single related model nested.

        alias: the key used to annotate the queryset, will be the key
               of the resulting json object

        fields: list of fields to use to represent the nested object

        rel: the related field on the base model. Must be a ForeignKey
        """

        rel_field = self.model._meta.get_field(rel)
        if not isinstance(rel_field, ForeignKey):
            raise ValueError("{} is not a ForeignKey".format(rel))
        select = ", ".join(['"{}"."{}"'.format(
            rel_field.rel.to._meta.db_table,
            f)for f in fields])

        template = 'select row_to_json({0}) from (select {4} from "{1}" \
where "{2}"."{3}" = "{1}"."id"){0}'.format(
            alias,
            rel_field.rel.to._meta.db_table,
            self.model._meta.db_table,
            rel_field.attname,
            select)
        return self.extra({'{}'.format(alias): template})
