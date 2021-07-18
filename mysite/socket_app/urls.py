from django.urls import path
from django.conf.urls import url

from .views import *

urlpatterns = [
    path('index', index),
    path('home', home),
    path('second', second),
    url(r"^test", test),
]