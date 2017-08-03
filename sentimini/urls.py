"""sentimini URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

from django.views.generic import TemplateView

from .views import admin_panel, delete_unsent_texts, slow_redirect, fun_splash, landing, get_nux_legend, test_page, signup_view, get_nux_home, get_nux_signup, get_nux_texts, get_random_suggestion, get_nux_timing, delete_text, pause_text, get_nux_settings, save_settings, nux_finalize

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^admin_panel/$', admin_panel, name='admin_panel'),
    url(r'^delete_unsent_texts/$', delete_unsent_texts, name='delete_unsent_texts'),
    url(r'^fun_splash/$', fun_splash, name='fun_splash'),

    url(r'^get_nux_home/$', get_nux_home, name='get_nux_home'),
    url(r'^get_nux_signup/$', get_nux_signup, name='get_nux_signup'),
    url(r'^get_nux_texts/$', get_nux_texts, name='get_nux_texts'),
    url(r'^get_nux_timing/$', get_nux_timing, name='get_nux_timing'),
    url(r'^get_nux_settings/$', get_nux_settings, name='get_nux_settings'),
    url(r'^get_nux_legend/$', get_nux_legend, name='get_nux_legend'),
    url(r'^nux_finalize/$', nux_finalize, name='nux_finalize'),

    
    url(r'^get_random_suggestion/$', get_random_suggestion, name='get_random_suggestion'),

    url(r'^delete_text/$', delete_text, name='delete_text'),    
    url(r'^pause_text/$', pause_text, name='pause_text'),    
    url(r'^save_settings/$', save_settings, name='save_settings'),    


    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',{'next_page': '/'}),
    url(r'accounts/signup', 'sentimini.views.signup_view'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^ent/', include('ent.urls',namespace="ent")),
    url(r'^power/', include('power.urls',namespace="power")),
    url(r'^consumer/', include('consumer.urls',namespace="consumer")),
    url(r'^professional/', include('professional.urls',namespace="professional")),
    url(r'^vis/', include('vis.urls',namespace="vis")),

    url(r'^test_page/$', test_page, name='test_page'),
    
    
    url(r'^$', fun_splash, name='fun_splash'),
    url(r'^landing/$', landing, name='landing'),
    
]
