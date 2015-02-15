# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.PositiveIntegerField(max_length=3)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Editor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sale_date', models.DateTimeField()),
                ('book', models.ForeignKey(to='bookstore.Book')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('close_time', models.PositiveIntegerField(max_length=2)),
                ('open_time', models.PositiveIntegerField(max_length=2)),
                ('open_date', models.DateField()),
                ('location', models.ForeignKey(to='bookstore.Location')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='sale',
            name='store',
            field=models.ForeignKey(to='bookstore.Store'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='book',
            name='editor',
            field=models.ForeignKey(to='bookstore.Editor'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='book',
            name='genre',
            field=models.ForeignKey(to='bookstore.Genre'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='book',
            name='store',
            field=models.ManyToManyField(to='bookstore.Store'),
            preserve_default=True,
        ),
    ]
