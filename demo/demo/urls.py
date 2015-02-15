from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
#    url(r'^$', 'demo.views.home', name='home'),
    url(r'^bookstore/', include('bookstore.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
