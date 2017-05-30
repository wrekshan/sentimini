from django.conf.urls import url

from .views import home, get_overview_options, get_measure, get_output

urlpatterns = [
	url(r'^home/$', home, name='home'),
	url(r'^get_overview_options/$', get_overview_options, name='get_overview_options'),
	url(r'^get_measure/$', get_measure, name='get_measure'),
	url(r'^get_output/$', get_output, name='get_output'),
]




