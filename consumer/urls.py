from django.conf.urls import url

from .views import home, moon, text, send_text_now, get_text_specific_overview, get_alternate, guided_tour, settings, change_nus, get_quick_suggestions, about, beta, get_create_program, submit_beta, program_indvidual_text, text_commands, program, create_program, get_program_display, get_csv, get_text_input, get_text_datatable, get_text_datatable_response, get_input_to_options, get_options_to_input, save_text, save_timing_default, save_timing

urlpatterns = [
	url(r'^home/$', home, name='home'),
	url(r'^get_alternate/$', get_alternate, name='get_alternate'),
	url(r'^guided_tour/$', guided_tour, name='guided_tour'),
	url(r'^settings/$', settings, name='settings'),
	url(r'^moon/$', moon, name='moon'),
	url(r'^about/$', about, name='about'),
	url(r'^beta/$', beta, name='beta'),
	url(r'^get_quick_suggestions/$', get_quick_suggestions, name='get_quick_suggestions'),
	url(r'^change_nus/$', change_nus, name='change_nus'),
	url(r'^submit_beta/$', submit_beta, name='submit_beta'),
	url(r'^text_commands/$', text_commands, name='text_commands'),
	url(r'^program/$', program, name='program'),
	url(r'^program/(?P<id>[0-9]+)/(?P<slug>[\w-]+)/$', program, name='program'),
	url(r'^text/(?P<id>[0-9]+)/(?P<slug>[\w-]+)/$', text, name='text'),
	url(r'^create_program/$', create_program, name='create_program'),
	url(r'^get_create_program/$', get_create_program, name='get_create_program'),
	url(r'^get_program_display/$', get_program_display, name='get_program_display'),
	url(r'^get_csv/$', get_csv, name='get_csv'),
	url(r'^get_csv/(?P<id>[0-9]+)/$', get_csv, name='get_csv'),
	url(r'^get_text_input/$', get_text_input, name='get_text_input'),
	url(r'^get_text_datatable/$', get_text_datatable, name='get_text_datatable'),
	url(r'^get_text_datatable_response/$', get_text_datatable_response, name='get_text_datatable_response'),
	url(r'^get_input_to_options/$', get_input_to_options, name='get_input_to_options'),
	url(r'^get_options_to_input/$', get_options_to_input, name='get_options_to_input'),
	url(r'^save_text/$', save_text, name='save_text'),
	url(r'^save_timing/$', save_timing, name='save_timing'),	
	url(r'^save_timing_default/$', save_timing_default, name='save_timing_default'),	
	url(r'^send_text_now/$', send_text_now, name='send_text_now'),
	url(r'^program_indvidual_text/$', program_indvidual_text, name='program_indvidual_text'),
	url(r'^get_text_specific_overview/$', get_text_specific_overview, name='get_text_specific_overview'),

	
]




