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

from .views import admin_panel, delete_unsent_texts, slow_redirect, upload_text_csv, fun_splash_description, fun_splash, app_home, delete_text, pause_text, tag_specific, feed_specific, get_feed_specific, save_settings, settings, landing, test_page, feed, signup_view, get_side, get_feed, get_new_text_form, get_new_text_hist, get_next_text_modal, get_new_text_basic_feed, save_new_text

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^admin_panel/$', admin_panel, name='admin_panel'),
    url(r'^delete_unsent_texts/$', delete_unsent_texts, name='delete_unsent_texts'),
    

    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',{'next_page': '/'}),
    url(r'accounts/signup', 'sentimini.views.signup_view'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^ent/', include('ent.urls',namespace="ent")),
    url(r'^consumer/', include('consumer.urls',namespace="consumer")),
    url(r'^vis/', include('vis.urls',namespace="vis")),

    url(r'^test_page/$', test_page, name='test_page'),
    url(r'^upload_text_csv/$', upload_text_csv, name='upload_text_csv'),
    url(r'^feed/$', feed, name='feed'),
    url(r'^app_home/$', app_home, name='app_home'),
    url(r'^fun_splash/$', fun_splash, name='fun_splash'),
    url(r'^fun_splash_description/$', fun_splash_description, name='fun_splash_description'),
    
    url(r'^get_feed_specific/$', get_feed_specific, name='get_feed_specific'),
    url(r'^feed_specific/(?P<id>[0-9]+)/$', feed_specific, name='feed_specific'),
    url(r'^tag_specific/(?P<id>[0-9]+)/$', tag_specific, name='tag_specific'),

    url(r'^pause_text/$', pause_text, name='pause_text'),
    url(r'^delete_text/$', delete_text, name='delete_text'),

    url(r'^$', slow_redirect, name='slow_redirect'),
    url(r'^landing/$', landing, name='landing'),

    url(r'^settings/$', settings, name='settings'),
    url(r'^save_settings/$', save_settings, name='save_settings'),

    url(r'^get_side/$', get_side, name='get_side'),
    url(r'^get_feed/$', get_feed, name='get_feed'),
    url(r'^get_next_text_modal/$', get_next_text_modal, name='get_next_text_modal'),
    url(r'^get_new_text_basic_feed/$', get_new_text_basic_feed, name='get_new_text_basic_feed'),
    url(r'^get_new_text_form/$', get_new_text_form, name='get_new_text_form'),
    url(r'^get_new_text_hist/$', get_new_text_hist, name='get_new_text_hist'),

    url(r'^save_new_text/$', save_new_text, name='save_new_text'),
    # url(r'^edit_text/(?P<id>[0-9]+)/$', edit_text, name='edit_text'),
    
]
