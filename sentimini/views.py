from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages

from datetime import datetime, timedelta, time, date
import pytz

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

from ent.models import PossibleText, Collection, Timing, Tag, ActualText, Carrier, UserSetting

def admin_panel(request):
	context = {
		}			

	return render(request,"admin_panel.html",context)

def delete_unsent_texts(request):
	response_data = {}
	working_texts = ActualText.objects.filter(time_to_send__lte=datetime.now(pytz.utc)).filter(time_sent=None)

	for text in working_texts:
		td = text.time_to_send - datetime.now(pytz.utc)
		if td.seconds/60 > 5:
			text.delete()

	return HttpResponse(json.dumps(response_data),content_type="application/json")					


def upload_text_csv(request):
	response_data = {}
	print("UPLOAD CSV")
	print(request.POST.keys())
	print(request.POST['file'])

	return HttpResponse(json.dumps(response_data),content_type="application/json")					



def fun_splash_description(request):
	response_data = {}
	context = {}
	context['working_collection'] = Collection.objects.all().get(id=int(request.POST['collection_id']))

	response_data["description"] = render_to_string('fun_splash_popout.html', context, request=request)
	

	return HttpResponse(json.dumps(response_data),content_type="application/json")					




def fun_splash(request):
	working_collections = Collection.objects.all().filter(publish=True)



	context = {
		'working_collections': working_collections

		}			

	return render(request,"fun_splash.html",context)


def app_home(request):
	if UserSetting.objects.all().filter(user=request.user).count()<1:
		return HttpResponseRedirect('/settings/')
	else:
		context = {

			}			

		return render(request,"app_home.html",context)



def delete_text(request):
	response_data ={}
	if request.user.is_authenticated():	
		print("ID TO DELETE",request.POST['id'])
		possible_text = PossibleText.objects.all().filter(user=request.user).get(id=request.POST['id'])
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


def tag_specific(request,id=None):
	if request.user.is_authenticated():	
		context = {}
		context['id'] = id

		# USE get_feed to edit feed stuff
		context = {

		}			

		return render(request,"feed_specific_scaffold.html",context)
	else:
		context = {
			
		}			

		return render(request,"feed_specific_scaffold.html",context)

def feed_specific(request,id=None):
	if request.user.is_authenticated():	
		context = {}
		context['id'] = id

		# USE get_feed to edit feed stuff
		context = {

		}			

		return render(request,"FEED_specific_scaffold.html",context)
	else:
		context = {
			
		}			

		return render(request,"FEED_specific_scaffold.html",context)




def get_feed_specific(request):
	main_context = {} # to build out the specific html stuff
	response_data = {} # to send back to the template
	
	# print("GETTING MAIN BAR")
	main_context['num_sent_texts'] =  ActualText.objects.all().filter(user=request.user).count()
	main_context['num_text_types'] =  PossibleText.objects.all().filter(user=request.user).count()

	working_filters = Q()

	##### DO THE CHECK TO SEE IF THERE ARE ANYTHING TO BE LOADED ON THE THING
	if request.POST['view_type'] == 'feed_specific':
		tmp_text = PossibleText.objects.all().get(id=int(request.POST['id']))
		working_filters.add(Q(text=tmp_text),Q.AND)
		main_context['searched_tags'] = str(PossibleText.objects.all().get(id=int(request.POST['id'])).text)
	else:
		tag = Tag.objects.all().get(id=int(request.POST['id']))
		working_filters.add(Q(tag=tag),Q.AND)
		main_context['searched_tags'] = str(Tag.objects.all().get(id=int(request.POST['id'])).tag)


	# working_texts = PossibleText.objects.all().filter(user=request.user).filter(working_filters)		
	working_texts = ActualText.objects.all().filter(user=request.user).filter(working_filters)
	


	main_context['text_present'] = working_texts.count()
	print("WORKING TEXT COUNT", working_texts.count())




	
	main_context['text_names'] = PossibleText.objects.all().filter(user=request.user).values('text').distinct()
	main_context['working_texts'] = working_texts


	# get the summary information 

	response_data["FEED"] = render_to_string('FEED_actual.html', main_context, request=request)

	print("main_context['searched_tags']",main_context['searched_tags'])
	
	if 'actual_switch' in request.POST.keys():
		if request.POST['actual_switch'] == 'true':
			main_context['actual_texts'] =  ActualText.objects.all().filter(user=request.user)
			response_data["FEED"] = render_to_string('FEED_actual.html', main_context, request=request)

	
	# else
	return HttpResponse(json.dumps(response_data),content_type="application/json")	





def get_feed(request):
	main_context = {} # to build out the specific html stuff
	response_data = {} # to send back to the template
	# print("GETTING MAIN BAR")
	main_context['num_sent_texts'] =  ActualText.objects.all().filter(user=request.user).count()
	main_context['num_text_types'] =  PossibleText.objects.all().filter(user=request.user).count()

	working_filters = Q()

	if 'all_possible_texts_search' in request.POST.keys():
		print("SEARCH: ", request.POST['all_possible_texts_search'])
		working_tags = request.POST['all_possible_texts_search'].split(',')

		print("WORKING TAGS IN FEED", len(working_tags))
		main_context['searched_tags'] = request.POST['all_possible_texts_search']

		for tag in working_tags:
			if str(tag).split("_")[0] == "tag":
				tmp = Tag.objects.all().filter(tag=str(tag).split("_")[1])
				working_filters.add(Q(tag__in=tmp),Q.AND)
			else:
				print("NAME", tag.split("_"))
				working_filters.add(Q(text=str(tag).split("_")[1]),Q.AND)
			



	working_texts = PossibleText.objects.all().filter(user=request.user).filter(working_filters)
	print("WORKING TEXT COUNT", working_texts.count())
	main_context['text_names'] = PossibleText.objects.all().filter(user=request.user).values('text').distinct()

	# get the summary information 
	key = 1
	text_info = {}
	for text in working_texts:
		actual_texts = ActualText.objects.all().filter(user=request.user).filter(text=text)
		
		if actual_texts.count() > 0:
			last_sent = actual_texts.last()
			first_sent = actual_texts.first()
		else:
			last_sent = ""
			first_sent = ""


		text_list = {}
		text_list = {
			"text": text,
			
			"date_last_sent": last_sent,
			"date_first_sent": first_sent,

			"number_sent": actual_texts.count(),
			"number_reply": ActualText.objects.all().filter(user=request.user).filter(text=text).filter(time_response__isnull=False).count()
		}

		text_info[key] = text_list
		key = key + 1

	main_context['text_info'] = tuple(text_info.items())
	main_context['text_present'] = 0
	if key > 1:
		main_context['text_present'] = 1
	response_data["FEED"] = render_to_string('FEED_possible.html', main_context, request=request)
	

	if 'actual_switch' in request.POST.keys():
		if request.POST['actual_switch'] == 'true':
			main_context['actual_texts'] =  ActualText.objects.all().filter(user=request.user)
			response_data["FEED"] = render_to_string('FEED_actual.html', main_context, request=request)

	
	# else
	return HttpResponse(json.dumps(response_data),content_type="application/json")	





def settings(request):
	if request.user.is_authenticated():	
		working_collections = Collection.objects.all().filter(publish=True)
		working_carrier = Carrier.objects.all()
		working_tz = pytz.country_timezones['us']
		if UserSetting.objects.all().filter(user=request.user).count()<1:
			working_settings = UserSetting(user=request.user,begin_date=pytz.utc.localize(datetime.now()))
			working_settings.save()
		else:
			working_settings = UserSetting.objects.all().get(user=request.user)

		context={
		'working_collections': working_collections,
		'working_carrier': working_carrier,
		'working_tz': working_tz,
		'working_settings': working_settings,
		}

		return render(request,"settings.html",context)
	
	else:
		return HttpResponseRedirect('/feed/')

def save_settings(request):
	response_data = {}
	if 'id' in request.POST.keys():
		working_settings = UserSetting.objects.all().get(id=int(request.POST['id']))
		working_settings.phone_input = request.POST['phone_input']
		working_carrier = Carrier.objects.all().get(carrier=request.POST['carrier_search'])


		
		if 'tz_search' in request.POST.keys():
			working_settings.timezone_search = request.POST['tz_search']

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
		if 'Eastern Standard Time' in request.POST['tz_search']:
			working_settings.timezone = 'America/New_York'
		elif 'Central Standard Time' in request.POST['tz_search']:
			working_settings.timezone = 'America/Chicago'
		elif 'Mountain Standard Time' in request.POST['tz_search']:
			working_settings.timezone = 'America/Denver'
		elif 'Pacific Standard Time' in request.POST['tz_search']:
			working_settings.timezone = 'America/Los_Angeles'
		else:
			working_settings.timezone = working_settings.timezone_search
		
		#set up the SMS address	
		working_settings.sms_address = working_settings.phone_input + working_carrier.sms_address
		working_settings.settings_complete = True
		working_settings.send_text_check = True
		working_settings.send_text = True

		working_settings.save()

	return HttpResponse(json.dumps(response_data),content_type="application/json")				

			
	
def slow_redirect(request):
	return HttpResponseRedirect('/consumer/about/')
		

def landing(request):
	if request.user.is_authenticated():	
		# return HttpResponseRedirect('/feed/')
		working_collections = Collection.objects.all().filter(publish=True)
		context={
		'working_collections': working_collections,
		}
	
	else:
		working_collections = Collection.objects.all().filter(publish=True)
		context={
		'working_collections': working_collections,
		}

	return render(request,"landing.html",context)




def test_page(request):
	context={}
	return render(request,"test_page.html",context)

def get_new_text_form(request):
	main_context = {} # to build out the specific html stuff
	response_data = {} # to send back to the template
	# print("GETTING MAIN BAR")

	main_context['working_texts'] =  PossibleText.objects.all()
	main_context['working_tags'] =  Tag.objects.all()
	# main_context['today_date'] = datetime.tod'yyyy-mm-dd',

	today = datetime.today()



	main_context['today_date'] = str(str(today.year) + "-" + str(today.strftime('%m')) + "-" + str(today.strftime('%d')))
	# print(main_context['today_date'])
	

	# response_data['today_date'] = datetime.today()
	
	# print("------- DT NOW",datetime.now().month())

	if 'id' in request.POST.keys():
		if request.POST['id'] != "None":
			# print(request.POST['id'])
			if request.user.is_authenticated():	
				main_context['editing_text'] = PossibleText.objects.all().filter(user=request.user).get(id=int(request.POST['id']))

				tmp_tags = PossibleText.objects.all().filter(user=request.user).get(id=int(request.POST['id'])).tag

				tags = []
				for tag in tmp_tags.all():
					tags.append(tag.tag)

				main_context['tags'] = tags
			
			# main_context['tag_vals'] = 
			# print("EDITING TEXTS")

	response_data["NEW_TEXT"] = render_to_string('NEW_TEXT.html', main_context, request=request)

	return HttpResponse(json.dumps(response_data),content_type="application/json")	


def get_side(request):
	side_context = {} # to build out the specific html stuff
	response_data = {} # to send back to the template
	if request.user.is_authenticated():	
		working_texts = PossibleText.objects.all().filter(user=request.user)

		# print("TAGS",PossibleText.objects.all().filter(user=request.user).values('tag').distinct())

		if 'side_switch' in request.POST.keys():
			if request.POST['side_switch'] == 'true':
				key = 1
				tag_info = {}
				working_tags = PossibleText.objects.all().filter(user=request.user).values('tag').distinct()
				for tag in working_tags:
					# print("TAG", tag)

					# if tag['tag'] is None:
					# 	# print("STRING NONE")
					# else:
					# 	print("KEEP GOING")

					if tag['tag'] is not None:
						tag_tmp = Tag.objects.all().get(id=tag['tag'])
						texts_tmp = PossibleText.objects.all().filter(user=request.user).filter(tag=tag_tmp)
						# unsorted_results = texts_tmp.all()
						# texts_tmp = sorted(unsorted_results, key= lambda t: t.burden())

						text_list = {
							"tag": tag_tmp,
							"num_texts": PossibleText.objects.all().filter(user=request.user).filter(tag=tag_tmp).count(),
							"texts": texts_tmp
						}
					else:
						texts_tmp = PossibleText.objects.all().filter(user=request.user).filter(tag__isnull=True)
						unsorted_results = texts_tmp.all()
						texts_tmp = sorted(unsorted_results, key= lambda t: t.burden())

						text_list = {
							"tag": "no tag",
							"texts": texts_tmp,
							"num_texts": PossibleText.objects.all().filter(user=request.user).filter(tag__isnull=True).count(),
						}


					tag_info[key] = text_list
					key = key + 1

				tag_info = tuple(tag_info.items())

				side_context['tag_info'] = tag_info
				side_context['working_user_texts'] =  PossibleText.objects.all().filter(user=request.user).order_by('feed')
				# side_context['working_feeds'] =  Feed.objects.all().filter(user=request.user)

				response_data["SIDE"] = render_to_string('SIDE_list_tags.html', side_context, request=request)
			else:
				side_context['working_texts'] = PossibleText.objects.all().filter(user=request.user)
				response_data["SIDE"] = render_to_string('SIDE_list_texts.html', side_context, request=request)


	return HttpResponse(json.dumps(response_data),content_type="application/json")




def feed(request):
	if request.user.is_authenticated():	

		# USE get_feed to edit feed stuff
		

		context = {
		}			

		return render(request,"feed_scaffold.html",context)
	else:
		context = {
			
		}			

		return render(request,"feed_scaffold.html",context)


def save_new_text(request):
	print("SAVING TEXT")
	response_data = {}
	response_data["message"] = "This worked!"


	if 'id' in request.POST.keys():
		if request.POST['id'] != "None" and request.POST['id'] != "":
			# print("ID", request.POST['id'])
			working_text = PossibleText.objects.all().filter(user=request.user).get(id=int(request.POST['id']))
		else:
			working_text = PossibleText(user=request.user,date_created=datetime.now(pytz.utc))
	else:
		working_text = PossibleText(user=request.user,date_created=datetime.now(pytz.utc))
	
	working_text.save()

	# STILL HAVE TO FIGURE OUT HOW TO EDIT THE TIMING< BUT I"M GOING TO WORRY ABOUT THAT NOW!

	# PossibleText MODEL
	if 'text' in request.POST.keys():
		# determine if new or old (just starting new now)
		# print(request.POST['text'])
		working_text.text = request.POST['text']



	if 'active_text_checkbox' in request.POST.keys():
		if request.POST['active_text_checkbox'] == "true":
			working_text.active=True
		else:
			working_text.active=False
		
	# TIMING
	working_timing = Timing(user=request.user,timing='unspecified')

	# if 'timing_select' in request.POST.keys():
		# print("TIMING NAME FOR NO REPEAT", request.POST['timing_select'])
		# working_timing.timing = request.POST['timing_select']
	
	if 'timing_name' in request.POST.keys():
		if len(request.POST['timing_name']) > 0:
			working_timing.timing = request.POST['timing_name']
			working_timing.show_user = True #ideally, for the new texts

	if 'date_start' in request.POST.keys():
		if request.POST['date_start'] != "":
			working_timing.date_start = datetime.strptime(request.POST['date_start'], '%Y-%m-%d')
			working_timing.date_start_value = request.POST['date_start']

	if 'end_date' in request.POST.keys():
		if request.POST['end_date'] != "":
			working_timing.date_end = datetime.strptime(request.POST['end_date'], '%Y-%m-%d')
			working_timing.date_end_value = request.POST['end_date']

	if 'hour_start' in request.POST.keys():
		working_timing.hour_start = datetime.strptime(request.POST['hour_start'],'%I:%M %p')

	if 'hour_end' in request.POST.keys():
		working_timing.hour_end = datetime.strptime(request.POST['hour_end'],'%I:%M %p')

	if 'hour_start_value' in request.POST.keys():
		working_timing.hour_start_value = int(request.POST['hour_start_value'].split(".")[0])

	if 'hour_end_value' in request.POST.keys():
		working_timing.hour_end_value = int(request.POST['hour_end_value'].split(".")[0])

	if 'fuzzy' in request.POST.keys():
		if request.POST['fuzzy'] == "true":
			working_timing.fuzzy = True
		else:
			working_timing.fuzzy = False

	if 'iti' in request.POST.keys():
		demo = request.POST['fuzzy_denomination']
		iti = int(request.POST['iti'])

		working_timing.fuzzy_denomination = demo
		working_timing.iti_raw = iti

		if demo == "minutes":
			working_timing.iti = iti
		elif demo == "hours":
			working_timing.iti = iti * 60
		elif demo == "days":
			working_timing.iti = iti * 60 * 24 
		elif demo == "weeks":
			working_timing.iti = iti * 60 * 24 * 7
		elif demo == "months":
			working_timing.iti = iti * 60 * 24 * 7 *30

	if 'iti_noise' in request.POST.keys():
		working_timing.iti_noise = request.POST['iti_noise']

	if 'repeat_in_window' in request.POST.keys():
		working_timing.repeat_in_window = request.POST['repeat_in_window']

	if 'repeat_weeks' in request.POST.keys():
		working_timing.repeat_weeks = request.POST['repeat_weeks']

	if 'weekdays' in request.POST.keys():
		for weekday in request.POST['weekdays'].split(','):
			if weekday == " Sunday":
				working_timing.sunday=True
			if weekday == " Monday":
				working_timing.monday=True
			if weekday == " Tuesday":
				working_timing.tuesday=True
			if weekday == " Wednesday":
				working_timing.wednesday=True
			if weekday == " Thursday":
				working_timing.thursday=True
			if weekday == " Friday":
				working_timing.friday=True
			if weekday == " Saturday":
				working_timing.saturday=True
	
	if 'repeat_summary' in request.POST.keys():
		working_timing.repeat_summary = request.POST['repeat_summary']

	if 'repeat'	 in request.POST.keys():
		# print("REPEAT CHECK", request.POST['repeat'])
		if request.POST['repeat'] == "true":
			working_timing.repeat = True
		else:
			working_timing.repeat = False

	working_timing.save()
	working_text.timing = working_timing

	#TAGS
	if 'tag_vals' in request.POST.keys():
		working_tags = request.POST['tag_vals'].split(',')
		for tag in working_tags:
			if Tag.objects.all().filter(tag=tag).count()>0:
				working_tag = Tag.objects.all().get(tag=tag)
			else:
				working_tag = Tag(user=request.user, tag=tag)
				working_tag.save()

			working_text.tag.add(working_tag)

	working_text.save()

	

	return HttpResponse(json.dumps(response_data),content_type="application/json")	




class SignupViewWithCustomForm(SignupView):
    form_class = SignupFormWithoutAutofocus
signup_view = SignupViewWithCustomForm.as_view()







def get_next_text_modal(request):
	# YOU EVENTUALLY DO A SWITCH HERE
	# print("get_next_text_modal")
	response_data = {} # to send back to the template

	if 'timing_switch' in request.POST.keys():

		if request.POST['timing_switch'] == 'false':
			response_data["model_content_for_switch"] = render_to_string('NEW_TEXT_modal_specific.html', request=request)
		else:
			response_data["model_content_for_switch"] = render_to_string('NEW_TEXT_modal_fuzzy.html', request=request)
	
	
	return HttpResponse(json.dumps(response_data),content_type="application/json")	



def get_new_text_basic_feed(request):
	main_context = {} # to build out the specific html stuff
	main_context['working_timings'] =  Timing.objects.all().filter(user=request.user).filter(system_time=True)


	response_data = {} # to send back to the template
	response_data["NEW_TEXT_basic_feed"] = render_to_string('NEW_TEXT_basic_feed.html', main_context, request=request)
	return HttpResponse(json.dumps(response_data),content_type="application/json")	





def get_new_text_hist(request):
	# print("get_new_text_hist")
	response_data={}
	if 'ITI_mean' in request.POST.keys():
		response_data['new_text_histogram'] = generate_histogram(int(request.POST['ITI_mean']),int(request.POST['ITI_noise']),request.POST['time_denomination'])

	return HttpResponse(json.dumps(response_data),content_type="application/json")	



def generate_histogram(ITI_mean,ITI_noise,time_denomination):
	#Generate 100 values
	ITI_noise_tmp = ITI_noise/100
	x = []
	for i in range(0,500):
		max_minutes = ITI_mean + (ITI_mean*ITI_noise_tmp)
		min_minutes = ITI_mean - (ITI_mean*ITI_noise_tmp)

		if min_minutes < 0:
			min_minutes = 0

		num_out = int(triangular(min_minutes, max_minutes, ITI_mean))
		if num_out < 0:
			num_out = 15
		x.append(num_out)

	#V2
	# number_here = int(triangular(exp.text_interval_minute_min, exp.text_interval_minute_max, exp.text_interval_minute_avg))
	data = [
		go.Histogram(x=x,
			
			autobinx=True,
		    xbins=dict(
		    ),
		    # marker = dict(color='rgba(0,188,212,1.0)',)
		    # marker = dict(color='rgba(255,193,7,1.0)',)
		    # marker = dict(color='rgba(229,57,53,1.0)',)
		    marker = dict(color='#e57373',)
		)
	]	

	title = time_denomination + " between texts"
	
    
	layout = go.Layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',margin={'b':35,'t': 10,'l': 30, 'r':10},height=150,showlegend=False, bargap=0.25,xaxis={ 'title':""},yaxis={'title': ""})
	
	figure=go.Figure(data=data,layout=layout)
	div = opy.plot(figure, auto_open=False, output_type='div',show_link=False)

	#work around to remove modebar stuff
	div = div.replace('displaylogo:!0', 'displaylogo:!1')
	div = div.replace('modeBarButtonsToRemove:[]', 'modeBarButtonsToRemove:["sendDataToCloud","hoverCompareCartesian"]')
	return div



