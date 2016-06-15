from django.conf.urls import url


from .views import edit_user_gen_prompt_settings, edit_prompt_settings, respite_one_day , respite_three_day , respite_seven_day, respite_start_again

urlpatterns = [
	url(r'^edit_prompt_settings/$', edit_prompt_settings, name='edit_prompt_settings'),
	url(r'^edit_user_gen_prompt_settings/$', edit_user_gen_prompt_settings, name='edit_user_gen_prompt_settings'),
	url(r'^respite_one_day/$', respite_one_day, name='respite_one_day'),
	url(r'^respite_three_day/$', respite_three_day, name='respite_three_day'),
	url(r'^respite_seven_day/$', respite_seven_day, name='respite_seven_day'),
	url(r'^respite_start_again/$', respite_start_again, name='respite_start_again'),
]


