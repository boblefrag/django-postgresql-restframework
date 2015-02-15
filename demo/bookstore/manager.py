from django.db import models
from django.db import connection
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
