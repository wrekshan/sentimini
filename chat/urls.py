from django.conf.urls import url

from .views import chat

urlpatterns = [
	url(r'^$', chat, name='chat'),
]