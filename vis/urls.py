from django.conf.urls import url

from .views import text_data, text_data_detail, text_data_demo, text_data_detail_demo

urlpatterns = [
	url(r'^$', text_data, name='text_data'),
	url(r'^text_data_detail/(?P<prompt_id>[0-9]+)/$', text_data_detail, name='text_data_detail'),
	url(r'^text_data_demo/$', text_data_demo, name='text_data_demo'),
	url(r'^text_data_detail_demo/(?P<prompt_id>[0-9]+)/$', text_data_detail_demo, name='text_data_detail_demo'),
]