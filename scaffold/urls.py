from django.conf.urls import url

from .views import emotion, about, blog, blog_detail, business_model, open_data, power, sentimini_help, upload_feed_data

urlpatterns = [
	url(r'^sentimini_help/$', sentimini_help, name='sentimini_help'),
	url(r'^open_data/$', open_data, name='open_data'),
	url(r'^power/$', power, name='power'),
	url(r'^business_model/$', business_model, name='business_model'),
	url(r'^about/$', about, name='about'),
	url(r'^blog/$', blog, name='blog'),
	url(r'^blog/(?P<id>[0-9]+)/$', blog_detail, name='blog_detail'),
	url(r'^emotion/$', emotion, name='emotion'),
	url(r'^upload_feed_data/$', upload_feed_data, name='upload_feed_data'),
	
]