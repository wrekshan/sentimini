from django.conf.urls import url

from .views import home, settings, about, get_text_input, get_text_datatable, get_text_datatable_response, get_input_to_options, get_options_to_input, save_text, save_timing_default, save_timing, test_signup

urlpatterns = [
	url(r'^home/$', home, name='home'),
	url(r'^settings/$', settings, name='settings'),
	url(r'^about/$', about, name='about'),
	url(r'^get_text_input/$', get_text_input, name='get_text_input'),
	url(r'^get_text_datatable/$', get_text_datatable, name='get_text_datatable'),
	url(r'^get_text_datatable_response/$', get_text_datatable_response, name='get_text_datatable_response'),
	url(r'^get_input_to_options/$', get_input_to_options, name='get_input_to_options'),
	url(r'^get_options_to_input/$', get_options_to_input, name='get_options_to_input'),
	url(r'^save_text/$', save_text, name='save_text'),
	url(r'^save_timing/$', save_timing, name='save_timing'),	
	url(r'^save_timing_default/$', save_timing_default, name='save_timing_default'),	
	url(r'^test_signup/$', test_signup, name='test_signup'),
]




