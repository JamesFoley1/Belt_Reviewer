from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^books$', views.books),
    url(r'^books/add$', views.add_books),
    url(r'^books/show/(?P<id>\d+)$', views.show_books),
    url(r'^users/(?P<id>\d+)$', views.users),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^review$', views.review),
    url(r'^destroy$', views.destroy),
    url(r'^addbook$', views.addbook),
]