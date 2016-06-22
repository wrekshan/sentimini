from django.conf.urls import url

from .views import faq, detail

urlpatterns = [
	url(r'^faq/$', faq, name='faq'),
	url(r'^faq/(?P<question_id>[0-9]+)/$', detail, name='detail'),
]