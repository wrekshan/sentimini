from django.conf.urls import url


from .views import reset_settings_complete, pause_all_users, restore_all_users, update_db_after_import, about, save_program_explicit, add_new_text, simulate, program, get_display_program, get_create_program, save_program, add_to_program, program_create_scaffold

urlpatterns = [
	url(r'^about/$', about, name='about'),
	
	url(r'^program/$', program, name='program'),
	url(r'^reset_settings_complete/$', reset_settings_complete, name='reset_settings_complete'),
	
	url(r'^update_db_after_import/$', update_db_after_import, name='update_db_after_import'),

	url(r'^pause_all_users/$', pause_all_users, name='pause_all_users'),
	url(r'^restore_all_users/$', restore_all_users, name='restore_all_users'),
	
	url(r'^get_create_program/$', get_create_program, name='get_create_program'),
	url(r'^get_display_program/$', get_display_program, name='get_display_program'),
	url(r'^save_program/$', save_program, name='save_program'),
	url(r'^save_program_explicit/$', save_program_explicit, name='save_program_explicit'),
	url(r'^add_to_program/$', add_to_program, name='add_to_program'),
	url(r'^simulate/$', simulate, name='simulate'),

	url(r'^add_new_text/$', add_new_text, name='add_new_text'),
	url(r'^add_new_text/(?P<id>[0-9]+)/$', add_new_text, name='add_new_text'),

	url(r'^program_create_scaffold/$', program_create_scaffold, name='program_create_scaffold'),
	url(r'^program_create_scaffold/(?P<id>[0-9]+)/$', program_create_scaffold, name='program_create_scaffold'),	

]


