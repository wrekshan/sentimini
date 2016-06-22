from django.conf.urls import url

from .views import faq

urlpatterns = [
	url(r'^faq/$', faq, name='faq'),
]