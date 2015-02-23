from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from bookstore import views

urlpatterns = [
    url(r'^books/$', views.BookList.as_view()),
    url(r'^books/(?P<pk>[0-9]+)$', views.BookDetail.as_view()),
    url(r'^editors/(?P<pk>[0-9]+)$',
        views.EditorDetail.as_view(),
        name="editor-detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
