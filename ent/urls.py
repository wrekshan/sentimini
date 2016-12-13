from django.conf.urls import url


from .views import advanced_uses, text_set_detail_descriptions, text_edit, create_new_feed_page, group_detail, kt_group, group_edit_detail, groups_edit, text_delete, text_activate, feeds_edit, respite_one_day, respite_three_day, respite_seven_day, respite_start_again, texter, new_user, add_texts, simulate_week, text_set, text_set_detail, new_user_help, text_set_alter, contact_settings

urlpatterns = [
	url(r'^kt_group/$', kt_group, name='kt_group'),
	url(r'^advanced_uses/$', advanced_uses, name='advanced_uses'),
	url(r'^contact_settings/$', contact_settings, name='contact_settings'),
	url(r'^texter/$', texter, name='texter'),
	url(r'^text_set/$', text_set, name='text_set'),
	url(r'^text_delete/(?P<id>[0-9]+)/$', text_delete, name='text_delete'),
	url(r'^text_set_detail_descriptions/(?P<id>[0-9]+)/$', text_set_detail_descriptions, name='text_set_detail_descriptions'),
	url(r'^text_activate/(?P<id>[0-9]+)/$', text_activate, name='text_activate'),
	url(r'^text_set_alter/(?P<id>[0-9]+)/$', text_set_alter, name='text_set_alter'),
	url(r'^text_set_detail/(?P<feed_id>[0-9]+)/(?P<group_id>[0-9]+)/$', text_set_detail, name='text_set_detail'),
	url(r'^new_user/$', new_user, name='new_user'),
	url(r'^new_user_help/$', new_user_help, name='new_user_help'),
	url(r'^feeds_edit/$', feeds_edit, name='feeds_edit'),
	# url(r'^create_new_feed_page/$', create_new_feed_page, name='create_new_feed_page'),
	url(r'^create_new_feed_page/(?P<group_id>[0-9]+)/$', create_new_feed_page, name='create_new_feed_page'),
	url(r'^create_new_feed_page/$', create_new_feed_page, name='create_new_feed_page'),
	url(r'^groups_edit/$', groups_edit, name='groups_edit'),
	# url(r'^group_delete/(?P<id>[0-9]+)/$', group_delete, name='group_delete'),
	url(r'^group_detail/(?P<id>[0-9]+)/$', group_detail, name='group_detail'),
	url(r'^group_edit_detail/$', group_edit_detail, name='group_edit_detail'),
	url(r'^group_edit_detail/(?P<id>[0-9]+)/$', group_edit_detail, name='group_edit_detail'),
	url(r'^simulate_week/$', simulate_week, name='simulate_week'),
	# url(r'^add_texts/(?P<feed_id>[0-9]+)/$', add_texts, name='add_texts'),
	url(r'^add_texts/(?P<feed_id>[0-9]+)/(?P<group_id>[0-9]+)/$', add_texts, name='add_texts'),
	url(r'^text_edit/(?P<id>[0-9]+)/$', text_edit, name='text_edit'),
	url(r'^respite_one_day/$', respite_one_day, name='respite_one_day'),
	url(r'^respite_three_day/$', respite_three_day, name='respite_three_day'),
	url(r'^respite_seven_day/$', respite_seven_day, name='respite_seven_day'),
	url(r'^respite_start_again/$', respite_start_again, name='respite_start_again'),	
	# url(r'^$', EmotionOnotologyTable.as_view(),  name='EmotionOnotologyTable'),
]


