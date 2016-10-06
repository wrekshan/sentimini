from django.conf.urls import url


from .views import edit_prompt_settings, respite_one_day, respite_three_day, respite_seven_day, respite_start_again, texter, new_user, add_texts, simulate_week

urlpatterns = [
	url(r'^texter/$', texter, name='texter'),
	url(r'^new_user/$', new_user, name='new_user'),
	url(r'^edit_prompt_settings/$', edit_prompt_settings, name='edit_prompt_settings'),
	url(r'^simulate_week/$', simulate_week, name='simulate_week'),
	url(r'^edit_prompt_settings/add_texts$', add_texts, name='add_texts'),
	url(r'^respite_one_day/$', respite_one_day, name='respite_one_day'),
	url(r'^respite_three_day/$', respite_three_day, name='respite_three_day'),
	url(r'^respite_seven_day/$', respite_seven_day, name='respite_seven_day'),
	url(r'^respite_start_again/$', respite_start_again, name='respite_start_again'),	
	# url(r'^$', EmotionOnotologyTable.as_view(),  name='EmotionOnotologyTable'),
]


