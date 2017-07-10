from django.conf.urls import url

from .views import home, people_and_groups, texts_and_programs, group, person, program, text, create_fake_users, create_fake_texts, get_pro_feed, get_pro_filters, get_people_and_group_side, get_add_person, get_actual_text_feed

urlpatterns = [
	url(r'^home/$', home, name='home'),
	url(r'^people_and_groups/$', people_and_groups, name='people_and_groups'),
	url(r'^texts_and_programs/$', texts_and_programs, name='texts_and_programs'),
	url(r'^group/(?P<id>[0-9]+)/$', group, name='group'),
	url(r'^program/(?P<id>[0-9]+)/$', program, name='program'),
	url(r'^text/(?P<id>[0-9]+)/$', text, name='text'),
	url(r'^person/(?P<id>[0-9]+)/$', person, name='person'),




	url(r'^get_pro_feed/$', get_pro_feed, name='get_pro_feed'),
	url(r'^get_actual_text_feed/$', get_actual_text_feed, name='get_actual_text_feed'),
	url(r'^get_pro_filters/$', get_pro_filters, name='get_pro_filters'),

	url(r'^get_people_and_group_side/$', get_people_and_group_side, name='get_people_and_group_side'),
	url(r'^get_add_person/$', get_add_person, name='get_add_person'),

	url(r'^create_fake_users/$', create_fake_users, name='create_fake_users'),
	url(r'^create_fake_texts/$', create_fake_texts, name='create_fake_texts'),
]




