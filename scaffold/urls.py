from django.conf.urls import url

from .views import emotion, emotion_detail, about, blog, blog_detail, business_model, open_data, power, sentimini_help

urlpatterns = [
	url(r'^sentimini_help/$', sentimini_help, name='sentimini_help'),
	url(r'^open_data/$', open_data, name='open_data'),
	url(r'^power/$', power, name='power'),
	url(r'^business_model/$', business_model, name='business_model'),
	url(r'^about/$', about, name='about'),
	url(r'^blog/$', blog, name='blog'),
	url(r'^blog/(?P<id>[0-9]+)/$', blog_detail, name='blog_detail'),
	url(r'^emotion/$', emotion, name='emotion'),
	url(r'^emotion/(?P<prompt_id>[0-9]+)/$', emotion_detail, name='emotion_detail'),
]