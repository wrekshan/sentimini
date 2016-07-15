from django.conf.urls import url

from .views import faq, detail, working_with_others, experiences

urlpatterns = [
	url(r'^working_with_others/$', working_with_others, name='working_with_others'),
	url(r'^experiences/$', experiences, name='experiences'),
	url(r'^faq/$', faq, name='faq'),
	url(r'^faq/(?P<question_id>[0-9]+)/$', detail, name='detail'),
]