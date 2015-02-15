from django.db import models
from django.contrib.auth.models import User
from bookstore.manager import PostgreSQLManager


class Location(models.Model):
    name = models.CharField(max_length=250)


class Store(models.Model):
    name = models.CharField(max_length=250)
    location = models.ForeignKey(Location)
    close_time = models.PositiveIntegerField(max_length=2)
    open_time = models.PositiveIntegerField(max_length=2)
    open_date = models.DateField()


class Genre(models.Model):
    name = models.CharField(max_length=250)


class Editor(models.Model):
    name = models.CharField(max_length=250)


class Book(models.Model):
    title = models.CharField(max_length=250)
    author = models.ForeignKey(User)
    genre = models.ForeignKey(Genre)
    editor = models.ForeignKey(Editor)
    store = models.ManyToManyField(Store)
    price = models.PositiveIntegerField(max_length=3)
    objects = PostgreSQLManager()
    

class Sale(models.Model):
    book = models.ForeignKey(Book)
    store = models.ForeignKey(Store)
    sale_date = models.DateTimeField()
    objects = PostgreSQLManager()
