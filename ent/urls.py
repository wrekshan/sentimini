from django.conf.urls import url


from .views import feeds_edit, respite_one_day, respite_three_day, respite_seven_day, respite_start_again, texter, new_user, add_texts, simulate_week, text_set, text_set_detail, new_user_help, text_set_alter, contact_settings

urlpatterns = [
	url(r'^contact_settings/$', contact_settings, name='contact_settings'),
	url(r'^texter/$', texter, name='texter'),
	url(r'^text_set/$', text_set, name='text_set'),
	url(r'^text_set_alter/(?P<id>[0-9]+)/$', text_set_alter, name='text_set_alter'),
	url(r'^text_set_detail/(?P<id>[0-9]+)/$', text_set_detail, name='text_set_detail'),
	url(r'^new_user/$', new_user, name='new_user'),
	url(r'^new_user_help/$', new_user_help, name='new_user_help'),
	url(r'^feeds_edit/$', feeds_edit, name='feeds_edit'),
	url(r'^simulate_week/$', simulate_week, name='simulate_week'),
	url(r'^feeds_edit/add_texts$', add_texts, name='add_texts'),
	url(r'^respite_one_day/$', respite_one_day, name='respite_one_day'),
	url(r'^respite_three_day/$', respite_three_day, name='respite_three_day'),
	url(r'^respite_seven_day/$', respite_seven_day, name='respite_seven_day'),
	url(r'^respite_start_again/$', respite_start_again, name='respite_start_again'),	
	# url(r'^$', EmotionOnotologyTable.as_view(),  name='EmotionOnotologyTable'),
]


