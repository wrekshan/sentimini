from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from timezonefinder import TimezoneFinder
from datetime import datetime, timedelta, time, date
import pytz
from geopy import geocoders
from .forms import SignupFormWithoutAutofocus
from allauth.account.views import SignupView

import json

from django.template.loader import render_to_string
from random import random, triangular, randint, gauss

import plotly.offline as opy
import plotly.graph_objs as go
from plotly.tools import FigureFactory as FF
import plotly.plotly as py
import numpy as np
from numpy import * 
from django.db.models import Avg
from django.db.models import Q

from ent.models import PossibleText, Program, Timing, Tag, ActualText, Carrier, UserSetting, IdealText, QuickSuggestion
from consumer.views import get_timing_default, save_timing_function


##########################
########### ACTUAL VIEWS
##########################
# This is just a way to play with the landing page
def get_nux_legend(request):
	main_context = {} 
	response_data = {}

	print("GETTING LEGEND") 

	if request.POST['location'] == 'text':
		main_context['legend_progress'] = "5"
		main_context['legend_message'] = "Next:</br>Schedule the text"
	elif request.POST['location'] == 'timing':
		main_context['legend_progress'] = "35"
		main_context['legend_message'] = "Next:</br>Phone number and timezone"
	elif request.POST['location'] == 'phone':
		main_context['legend_progress'] = "65"
		main_context['legend_message'] = "Next:</br>Username and password"
	elif request.POST['location'] == 'email':
		main_context['legend_progress'] = "95"
		main_context['legend_message'] = "You'll be all ready to go!"



	response_data['NUX_legend'] = render_to_string('NUX_legend.html', main_context, request=request)
	
	print("LEGEND")
	print(response_data['NUX_legend'])

	return HttpResponse(json.dumps(response_data),content_type="application/json")



def fun_splash(request):
	working_programs = Program.objects.all().filter(publish=True)
	# display_names = ("mindfulness","productivity","smoking","medication")
	display_names = ("mindfulness","productivity", "exploring emotions")
	context = {
		'working_programs': working_programs,
		'video_name': 'Cloudy_Road',
		'display_names': display_names,
		}			
	
	return render(request,"NUX_home.html",context)


def get_nux_home(request):
	main_context = {} 
	response_data = {} 

	main_context['display_names'] = ("mindfulness","productivity", "exploring emotions", 'remembering sunsets')

	response_data['NUX_selector'] = render_to_string('NUX_selector.html', main_context, request=request)
	response_data['NUX_examples'] = render_to_string('NUX_examples.html', main_context, request=request)
	response_data['NUX_footer'] = render_to_string('NUX_footer.html', main_context, request=request)
	return HttpResponse(json.dumps(response_data),content_type="application/json")



def get_nux_signup(request):
	main_context = {} 
	response_data = {} 


	main_context['text_content'] = request.POST['text_content']
	main_context['hour_start'] = request.POST['hour_start']
	main_context['date_start'] = request.POST['date_start']
	main_context['date_end'] = request.POST['date_end']
	main_context['hour_end'] = request.POST['hour_end']
	main_context['hour_start_value'] = request.POST['hour_start_value']
	main_context['hour_end_value'] = request.POST['hour_end_value']
	main_context['iti'] = request.POST['iti']
	main_context['iti_noise'] = request.POST['iti_noise']
	main_context['fuzzy_denomination'] = request.POST['fuzzy_denomination']
	main_context['fuzzy'] = request.POST['fuzzy']
	main_context['num_repeats'] = request.POST['num_repeats']
	main_context['weekdays'] = request.POST['weekdays']
	main_context['phone_input'] = request.POST['phone_input']
	main_context['carrier_search'] = request.POST['carrier_search']
	main_context['location'] = request.POST['location']


	

	response_data['NUX_signup'] = render_to_string('NUX_signup.html', main_context, request=request)
	return HttpResponse(json.dumps(response_data),content_type="application/json")


def get_random_suggestion(request):
	main_context = {} 
	response_data = {} 

	quick_suggestions = ("Drink Water",
		"Stand up and strech!",
		"Just pay attention to your breath for 3 cycles.",
		"How happy are you right now (respond with 0-10)?",
		"Eat some veggies!",
		"I am good enough.  I am smart enough.  People like me.")

	response_data['suggestion'] = quick_suggestions[random.randint(0,len(quick_suggestions))]
	return HttpResponse(json.dumps(response_data),content_type="application/json")


def get_nux_texts(request):
	main_context = {} 
	response_data = {} 

	# This is an interim solution.  Should have a binary switch on ideal texts to select ones here.
	# Also, might consider having a quick screen before this to ask why.
	quick_suggestions = ("Drink Water",
		"Stand up and strech!",
		"Just pay attention to your breath for 3 cycles."
		"How happy are you right now (respond with 0-10)?",
		"Eat some veggies!",
		"I am good enough.  I am smart enough.  People like me.")

	quick_text = IdealText.objects.all().filter(quick_suggestion=True).order_by('?').first()
	# current_ids.append(quick_text.id)

	tmp_context = {'working_text': quick_text,
		'quick_suggestions': quick_suggestions,
	}

	# main_context["suggestion_1"] = render_to_string('SS_quick_suggestions.html', tmp_context, request=request)
	main_context["quick_suggestions"] = quick_suggestions

	

	response_data['NUX_texts'] = render_to_string('NUX_texts.html', main_context, request=request)
	return HttpResponse(json.dumps(response_data),content_type="application/json")

def get_nux_timing (request):
	main_context = {} 
	response_data = {} 

	# working_timing = get_timing_default(request)
	today = datetime.today()
	main_context['today_date'] = str(str(today.strftime('%d'))  + " " + str(today.strftime('%B')) + ", " + str(today.year))
	# main_context['working_timing'] = working_timing
	main_context['text_content'] = request.POST['text_content']
	
	response_data['NUX_timing'] = render_to_string('NUX_timing.html', main_context, request=request)
	return HttpResponse(json.dumps(response_data),content_type="application/json")


def get_nux_settings(request):
	main_context = {} 
	response_data = {} 
	main_context['working_carrier'] = Carrier.objects.all()

	main_context['text_content'] = request.POST['text_content']
	main_context['hour_start'] = request.POST['hour_start']
	main_context['date_start'] = request.POST['date_start']
	main_context['date_end'] = request.POST['date_end']
	main_context['hour_end'] = request.POST['hour_end']
	main_context['hour_start_value'] = request.POST['hour_start_value']
	main_context['hour_end_value'] = request.POST['hour_end_value']
	main_context['iti'] = request.POST['iti']
	main_context['iti_noise'] = request.POST['iti_noise']
	main_context['fuzzy_denomination'] = request.POST['fuzzy_denomination']
	main_context['fuzzy'] = request.POST['fuzzy']
	main_context['num_repeats'] = request.POST['num_repeats']
	main_context['weekdays'] = request.POST['weekdays']

	
	response_data['NUX_settings'] = render_to_string('NUX_settings.html', main_context, request=request)
	return HttpResponse(json.dumps(response_data),content_type="application/json")


def nux_finalize(request):
	response_data = {}
	# print("SAVE SETTINGS")



	# CREATE USER SETTINGS
	working_settings = UserSetting(user=request.user,begin_date=pytz.utc.localize(datetime.now()))
	working_settings.save()

	working_settings.phone_input = request.POST['phone_input']
	working_settings.phone = request.POST['phone_input']
	
	working_carrier = Carrier.objects.all().get(carrier=request.POST['carrier_search'])

	if 'location' in request.POST.keys():
		working_settings.location = request.POST['location']

		# Figure out the TZ
		g = geocoders.GoogleV3()

		place, (lat, lng) = g.geocode(request.POST['location'])

		tf = TimezoneFinder()
		timeZoneStr = tf.closest_timezone_at(lng=lng, lat=lat)
		working_settings.timezone_search = timeZoneStr
		working_settings.timezone = timeZoneStr

		# working_settings.timezone_search = 

	if 'carrier_search' in request.POST.keys():
		working_settings.carrier = request.POST['carrier_search']

	#set up the SMS address	
	working_settings.sms_address = working_settings.phone_input + working_carrier.sms_address
	working_settings.settings_complete = True
	working_settings.send_text_check = True
	working_settings.send_text = True
	working_settings.text_request_stop = False
	working_settings.save()

	# Make the timing
	working_timing = Timing(user=request.user,default_timing=False, fuzzy=True, repeat=True)
	working_timing.save()
	working_timing = save_timing_function(request,working_timing)
	working_timing.save()
	
	

	# CREATE POSSIBLE TEXT
	working_text = PossibleText(user=request.user,text=request.POST['text_content'],date_created=datetime.now(pytz.utc))
	working_text.save()
	working_text.timing = working_timing
	working_text.tmp_save = False
	working_text.save()

	

	# SEND WELCOM TEXT
	wtc = "Welcome to Sentimini!  If you didn't just sign up, then just text 'stop'.  Otherwise schedule some texts!"
	if PossibleText.objects.all().filter(user=request.user).filter(text=wtc).count()<1:
		welcome_text_p = PossibleText(user=request.user,text=wtc,active=False,tmp_save=True)
		welcome_text_p.save()

	welcome_text_p = PossibleText.objects.all().filter(user=request.user).get(text=wtc)
	print("welcome_text_p",welcome_text_p)
	welcome_text_a = ActualText(user=request.user,text=welcome_text_p,time_to_send=datetime.now(pytz.utc))
	welcome_text_a.save()

		

	return HttpResponse(json.dumps(response_data),content_type="application/json")











def test_page(request):
	context={}
	return render(request,"test_page.html",context)	

# This just serves up a bunch of function
def admin_panel(request):
	context = {
		}			

	return render(request,"admin_panel.html",context)

# This is for the admin panel.  I don't really have to worry about this since it is baked into the task files
# you can also probably delete this as it isn't called in the task file either
def delete_unsent_texts(request):
	response_data = {}

	working_qs = QuickSuggestion.objects.all()
	for qs in working_qs:
		qs.delete()
		
	# working_texts = ActualText.objects.filter(time_to_send__lte=datetime.now(pytz.utc)).filter(time_sent=None)

	# for text in working_texts:
	# 	td = text.time_to_send - datetime.now(pytz.utc)
	# 	if td.seconds/60 > 5:
	# 		text.delete()

	return HttpResponse(json.dumps(response_data),content_type="application/json")					
		

def slow_redirect(request):
	if request.user.is_authenticated():	
		return HttpResponseRedirect('/consumer/home/')
	else:
		return HttpResponseRedirect('/consumer/about/')
		

def landing(request):
	if request.user.is_authenticated():	
		# return HttpResponseRedirect('/feed/')
		working_programs = Program.objects.all().filter(publish=True)
		context={
		'working_programs': working_programs,
		}
	
	else:
		working_programs = Program.objects.all().filter(publish=True)
		context={
		'working_programs': working_programs,
		}

	return render(request,"landing.html",context)


# I don't know what this is about
class SignupViewWithCustomForm(SignupView):
    form_class = SignupFormWithoutAutofocus
signup_view = SignupViewWithCustomForm.as_view()


####### PROBABLY SHOULD MOVE THESE TO A MORE SENSIBLE LOCATIONS
def delete_text(request):
	response_data ={}
	if request.user.is_authenticated():	
		print("ID TO DELETE",request.POST['id'])
		possible_text = PossibleText.objects.all().filter(user=request.user).get(id=request.POST['id'])
		if possible_text.alt_text.all().count()>0:
			for text in possible_text.alt_text.all():
				text.delete()
		print("possible text", possible_text.text)
		possible_text.delete()
	return HttpResponse(json.dumps(response_data),content_type="application/json")					


def pause_text(request):
	response_data ={}
	if request.user.is_authenticated():	
		print(request.POST.keys())
		possible_text = PossibleText.objects.all().filter(user=request.user).get(id=request.POST['id'])
		if possible_text.active == True:
			possible_text.active = False
			response_data['pause_type'] = "paused"
		else:
			possible_text.active = True
			response_data['pause_type'] = "started"

		possible_text.save()
	return HttpResponse(json.dumps(response_data),content_type="application/json")			

def save_settings(request):
	response_data = {}
	# print("SAVE SETTINGS")
	if 'id' in request.POST.keys():
		if request.POST['save_type'] == "save_settings_button":
			working_settings = UserSetting.objects.all().get(id=int(request.POST['id']))
			working_settings.phone_input = request.POST['phone_input']
			working_settings.phone = request.POST['phone_input']
			working_carrier = Carrier.objects.all().get(carrier=request.POST['carrier_search'])

			if 'location' in request.POST.keys():
				working_settings.location = request.POST['location']
				print("LOCATION", request.POST['location'])

				# Figure out the TZ
				g = geocoders.GoogleV3()
				

				place, (lat, lng) = g.geocode(request.POST['location'])
				print("place", place)
				print("lat", lat)
				print("lng", lng)

				tf = TimezoneFinder()
				timeZoneStr = tf.closest_timezone_at(lng=lng, lat=lat)
				print("timeZoneStr", timeZoneStr)
				working_settings.timezone_search = timeZoneStr
				working_settings.timezone = timeZoneStr

				# working_settings.timezone_search = 

			if 'carrier_search' in request.POST.keys():
				working_settings.carrier = request.POST['carrier_search']

			if request.POST['email_checkbox'] == 'true':
				working_settings.send_email_check = True
			else:
				working_settings.send_email_check = False

			if request.POST['text_checkbox'] == 'true':
				working_settings.send_text_check = True
			else:
				working_settings.send_text_check = False	

			if request.POST['research_check'] == 'true':
				working_settings.research_check = True
			else:
				working_settings.research_check = False		

			if request.POST['pause_text_checkbox'] == 'true':
				working_settings.pause_text_checkbox = True
			else:
				working_settings.pause_text_checkbox = False	

			##### DO THE PROCESS
			#set up the timezone
			# if 'Eastern Standard Time' in request.POST['tz_search']:
			# 	working_settings.timezone = 'America/New_York'
			# elif 'Central Standard Time' in request.POST['tz_search']:
			# 	working_settings.timezone = 'America/Chicago'
			# elif 'Mountain Standard Time' in request.POST['tz_search']:
			# 	working_settings.timezone = 'America/Denver'
			# elif 'Pacific Standard Time' in request.POST['tz_search']:
			# 	working_settings.timezone = 'America/Los_Angeles'
			# else:
			# 	working_settings.timezone = working_settings.timezone_search
			
			#set up the SMS address	
			working_settings.sms_address = working_settings.phone_input + working_carrier.sms_address
			working_settings.settings_complete = True
			working_settings.send_text_check = True
			working_settings.send_text = True
			working_settings.text_request_stop = False

			working_settings.save()

			wtc = "Welcome to Sentimini!  If you didn't just sign up, then just text 'stop'.  Otherwise schedule some texts!"
			if PossibleText.objects.all().filter(user=request.user).filter(text=wtc).count()<1:
				welcome_text_p = PossibleText(user=request.user,text=wtc,active=False,tmp_save=True)
				welcome_text_p.save()
		


			welcome_text_p = PossibleText.objects.all().filter(user=request.user).get(text=wtc)
			print("welcome_text_p",welcome_text_p)
			welcome_text_a = ActualText(user=request.user,text=welcome_text_p,time_to_send=datetime.now(pytz.utc))
			welcome_text_a.save()

		else:
			print("REJECT SETTINGS")
			working_settings = UserSetting.objects.all().get(id=int(request.POST['id']))
			working_settings.settings_complete = True
			working_settings.send_text_check = False
			working_settings.send_text = False
			working_settings.text_request_stop = True
			working_settings.save()
		

	return HttpResponse(json.dumps(response_data),content_type="application/json")			