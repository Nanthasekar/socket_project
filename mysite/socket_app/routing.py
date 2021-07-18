from django.urls import path
from django.conf.urls import url

from .consumers import WSConsumer

ws_urlpatterns = [
	url(r"^ws/test_url/(?P<user_id>[0-9]+)/(?P<cohort_id>[0-9]+)/", WSConsumer.as_asgi())
]