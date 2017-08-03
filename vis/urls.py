from django.conf.urls import url
from .views import simulate_texts, get_text_specific_vis

urlpatterns = [
	url(r'^simulate_texts/$', simulate_texts, name='simulate_texts'),
	url(r'^get_text_specific_vis/$', get_text_specific_vis, name='get_text_specific_vis'),
	
]