from django.db.models import Avg, Count, F, Case, When
from django.shortcuts import render, render_to_response
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from datetime import datetime, timedelta
import pytz
from django import forms
from random import random, triangular, randint
from django.core import serializers

from django.forms import modelformset_factory
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse

from django.contrib.auth.models import User
from ent.models import IdealText, PossibleText, ActualText, Timing, UserSetting



# get the text specific visualization
def get_text_specific_vis(request):
	main_context = {} # to build out the specific html stuff
	response_data = {} # to send back to the template



	working_texts = ActualText.objects.all().filter(user=request.user)
	datz = [['', 'response']]


	for text in working_texts:
		if text.response == None:
			response = int(-1)
		else:
			response = int(text.response)
		# print(text.time_to_send.strftime('%d %b'))
		datz.append([text.time_to_send.strftime('%d %b'),int(response)])

	print("DATZ",datz)	


	# main_context['actual_texts_graph'] = json.dumps( [['date', o.time_to_send, 'response', o.response] for o in working_texts], cls=DjangoJSONEncoder)

	main_context['actual_texts_graph'] = json.dumps( datz, cls=DjangoJSONEncoder)
	


	response_data["text_vis"] = render_to_string('VIS_text_specific_vis.html', main_context, request=request)
	return HttpResponse(json.dumps(response_data),content_type="application/json")




############# SIMULATION TO 
def time_window_check(text,possible_date,date_today):
	working_settings = UserSetting.objects.all().get(user=text.user)
	user_timezone = pytz.timezone(working_settings.timezone)
	
	# This is new a should work

	starting_time = user_timezone.localize(datetime.combine(date_today, text.timing.hour_start))
	starting_time = starting_time.astimezone(pytz.UTC)

	ending_time = user_timezone.localize(datetime.combine(date_today, text.timing.hour_end))
	ending_time = ending_time.astimezone(pytz.UTC)

	if not starting_time < possible_date < ending_time:
		if possible_date < starting_time:
			# print("LESS THAN START TIME")
			window_diff = starting_time - possible_date
			possible_date = possible_date + timedelta(hours=0,minutes=0,seconds=window_diff.seconds*2)
		else:
			# print("MORE THAN START TIME")
			date_today = datetime.now(pytz.utc).astimezone(user_timezone)

			time_window = user_timezone.localize(datetime.combine(date_today, text.timing.hour_end)) - user_timezone.localize(datetime.combine(date_today, text.timing.hour_start))
			scheduled_date = starting_time + timedelta(hours=24) 
			if text.timing.iti > time_window.total_seconds():
				seconds_to_add = randint(0,time_window.total_seconds())
			else:
				seconds_to_add = randint(0,(60*text.timing.iti))
			

			possible_date = scheduled_date + timedelta(0,seconds_to_add)
			
	return(possible_date)




def simulate_texts(request):
	users = User.objects.all().exclude(username="admin")
	ideal_text = IdealText.objects.all().get(text="How happy are you right now (respond with a 0-10 rating)?")


	for user in users:
		if UserSetting.objects.all().filter(user=user).count()<1:
			working_settings = UserSetting.objects.all().first()
			new_settings = UserSetting(user=user,timezone=working_settings.timezone)
			new_settings.save()


		working_texts = PossibleText.objects.all().filter(user=user)
		for text in working_texts:
			text.delete()
		
		# create the possible text
		possible_text = PossibleText(user=user,timing=ideal_text.timing,text=ideal_text.text,ideal_text=ideal_text,text_type="simulated",tmp_save=False)
		possible_text.save()

	working_texts = PossibleText.objects.all().filter(text_type="simulated")

	num_texts = 100
	for text in working_texts:
		print("TEXT", text)
		working_settings = UserSetting.objects.all().get(user=text.user)
		user_timezone = pytz.timezone(working_settings.timezone)
		tmp_date = datetime.now(pytz.utc).astimezone(user_timezone)

		for i in range(0,num_texts):
			print("ACUAL", i)
			# Get the timing info
			# Hack to have discrete values in slider
			noise_tmp = 100
			if text.timing.iti_noise == 1:
				noise_tmp = 100
			if text.timing.iti_noise == 2:
				noise_tmp = 400
			if text.timing.iti_noise == 3:
				noise_tmp = 600
			if text.timing.iti_noise == 4:
				noise_tmp = 800	
			
			ITI_noise_tmp = noise_tmp/100
			ITI_mean = text.timing.iti
			max_minutes = ITI_mean + (ITI_mean*ITI_noise_tmp)
			min_minutes = ITI_mean - (ITI_mean*ITI_noise_tmp)

			# Add seconds
			seconds_to_add = 60 * int(triangular(min_minutes, max_minutes, ITI_mean))

			#Get today's date and end in UTC
			# date_today = datetime.now(pytz.utc).astimezone(user_timezone)
			possible_date = tmp_date + timedelta(0,seconds_to_add)
			possible_date = possible_date.astimezone(pytz.UTC)
					
			possible_date = time_window_check(text,possible_date,tmp_date)
			possible_date = possible_date.astimezone(pytz.UTC)
			atext = ActualText(user=text.user,text_sent=text.text,text=text,time_to_send=possible_date,time_sent=possible_date)

			##### Simulatie responses
			seconds_to_add = 60 * int(triangular(1, 120, 10))
			atext.time_response = possible_date + timedelta(0,seconds_to_add)
			if randint(0, 99) < 80:
				atext.response = randint(0, 10)

			atext.save()

			tmp_date = possible_date

	return redirect('/admin_panel/')


# Assign them a single possible text

# Make a bunch of actual texts for them

# Graph the responses (focus on 0-10)

# Make some fake demographics
	# Think it should be (compare with age (answer age), compare with gender (answer gender), etc)




