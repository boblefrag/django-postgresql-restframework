from django.db import models
from django.db import connection
from psycopg2 import extras
from collections import OrderedDict
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
        print self.__dict__
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
