from django.conf.urls import url


from .views import about, save_collection_explicit, add_new_text, simulate, collection, get_display_collection, get_create_collection, save_collection, add_to_collection, collection_create_scaffold

urlpatterns = [
	url(r'^about/$', about, name='about'),
	url(r'^collection/$', collection, name='collection'),
	
	url(r'^get_create_collection/$', get_create_collection, name='get_create_collection'),
	url(r'^get_display_collection/$', get_display_collection, name='get_display_collection'),
	url(r'^save_collection/$', save_collection, name='save_collection'),
	url(r'^save_collection_explicit/$', save_collection_explicit, name='save_collection_explicit'),
	url(r'^add_to_collection/$', add_to_collection, name='add_to_collection'),

	url(r'^simulate/$', simulate, name='simulate'),

	url(r'^add_new_text/$', add_new_text, name='add_new_text'),
	url(r'^add_new_text/(?P<id>[0-9]+)/$', add_new_text, name='add_new_text'),


	url(r'^collection_create_scaffold/$', collection_create_scaffold, name='collection_create_scaffold'),
	url(r'^collection_create_scaffold/(?P<id>[0-9]+)/$', collection_create_scaffold, name='collection_create_scaffold'),	

]


