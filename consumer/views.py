from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from random import random, triangular, randint, gauss
import json
from datetime import datetime, timedelta, time, date
import pytz
from allauth.account.adapter import get_adapter, DefaultAccountAdapter
from sentimini.forms import SignupFormWithoutAutofocus
from allauth.account.forms import SignupForm

from sentimini.views import pause_text
from ent.models import AlternateText, Quotation, QuickSuggestion, Beta, ActualText, PossibleText, Timing, Carrier, UserSetting, Collection, Tag
from django.db.models import Q

import time

import requests

import csv

def get_alternate(request):
	main_context = {} # to build out the specific html stuff
	response_data = {} # to send back to the template

	if "counter" in request.POST.keys():
		main_context['counter'] = request.POST['counter']


	response_data['alternate_form'] = render_to_string('SS_alternate.html', main_context, request=request)

	return HttpResponse(json.dumps(response_data),content_type="application/json")		


def change_nus(request):
	main_context = {} # to build out the specific html stuff
	response_data = {} # to send back to the template

	working_settings = UserSetting.objects.all().get(user=request.user)
	working_settings.new_user_step = 1
	working_settings.save()

	return HttpResponse(json.dumps(response_data),content_type="application/json")		


# pas {'phase': 'Last Quarter', 'time': '11:33', 'date': '2017 Jun 17'}
# pas {'phase': 'New Moon', 'time': '02:31', 'date': '2017 Jun 24'}
# pas {'phase': 'First Quarter', 'time': '00:51', 'date': '2017 Jul 01'}
# pas {'phase': 'Full Moon', 'time': '04:07', 'date': '2017 Jul 09'}

def get_moon_data():
	import requests
	print("GET MOON DATA")
	
	output = "NOT FOUND"
	try:
		print("GET MOON DATA --- IN TRY")
		date_now = str(datetime.now(pytz.utc).strftime('%-m/%-d/%Y'))
		# requests.get('s')
		data = requests.get('http://api.usno.navy.mil/moon/phase?date='+date_now+'&nump=4')
		dataj = data.json()
		output = dataj
		return output
	except:
		print("GET MOON DATA --- NOT TRY")
		return output
	

def get_sun_time(sundata,desired):
	for i in range(0,len(sundata)):
		if sundata[i]['phen'] == desired:
			return sundata[i]['time']

# [{'time': '5:16 a.m. DT', 'phen': 'BC'}, {'time': '5:48 a.m. DT', 'phen': 'R'}, {'time': '1:11 p.m. DT', 'phen': 'U'}, {'time': '8:34 p.m. DT', 'phen': 'S'}, {'time': '9:06 p.m. DT', 'phen': 'EC'}]
def moon(request):
	context = {}
	# FOR THE TASKS FILLE
	date_now = str(datetime.now(pytz.utc).strftime('%-m/%-d/%Y'))
	distinct_users = PossibleText.objects.all().filter(tmp_save=False).filter(active=True).filter(text_type="sun").values('user').distinct()

	for user in distinct_users:
		working_settings = UserSetting.objects.all().get(user=user['user'])
		user_timezone = pytz.timezone(working_settings.timezone)

		try:
			data = requests.get('http://api.usno.navy.mil/rstt/oneday?date='+ date_now +'&loc=San Francisco, CA')
			dataj = data.json()
			output = dataj
		except:
			dataj = "NOT FOUND"
		
		if dataj != "NOT FOUND":	
			#Get the sun data
			working_texts = PossibleText.objects.all().filter(user=working_settings.user).filter(tmp_save=False).filter(active=True).filter(text_type="sun")
			for text in working_texts:
				if ActualText.objects.all().filter(user=text.user).filter(text=text).filter(time_sent__isnull=True).filter(time_to_send__gte=pytz.utc.localize(datetime.now())).count() < 1:
					if 'Sun Rise' in text.text:
						text_to_send = 'The sun is rising right now!'
						time_out = get_sun_time(dataj['sundata'],'R')
					elif 'Sun Set' in text.text: 
						text_to_send = 'The sun is setting right now!'
						time_out = get_sun_time(dataj['sundata'],'S')
					elif 'Upper Transit' in text.text:
						text_to_send = 'The sun is at the highest point in the sky today right now!'
						time_out = get_sun_time(dataj['sundata'],'U')
					
					# time_out 8:34 p.m. DT
					time_out_time = time_out.split(' ')[0]
					time_out_ampm = time_out.split(' ')[1]
					if time_out_ampm == "a.m.":
						time_out_ampm = "AM"
					else:
						time_out_ampm = "PM"

					date_out = str(str(datetime.now(pytz.utc).date()) + ' ' + time_out_time + ' ' + time_out_ampm)
					time_to_send = datetime.strptime(date_out, "%Y-%m-%d %I:%M %p")
					time_to_send = user_timezone.localize(time_to_send)
					time_to_send = time_to_send.astimezone(pytz.UTC)

					atext = ActualText(user=text.user,text=text,time_to_send=time_to_send,text_sent=text_to_send)
					atext.save()
				


				# time_out = 

				# Save the sun data
				# if ActualText.objects.all().filter(user=text.user).filter(text=text).filter(time_to_send__gte=pytz.utc.localize(datetime.now())).count() < 1:

			
					# user_timezone = pytz.timezone(working_settings.timezone)
					# moon_dt_user = moon_dt_utc.astimezone(user_timezone)

					# # #See if there is a text scheduled in the future for this phase.  if not, then schedule it.
					# if ActualText.objects.all().filter(user=text.user).filter(text=text).filter(time_to_send__gte=pytz.utc.localize(datetime.now())).count() < 1:
					# 	date_today = datetime.now(pytz.utc).astimezone(user_timezone)
					# 	time_window = user_timezone.localize(datetime.combine(date_today, text.timing.hour_end)) - user_timezone.localize(datetime.combine(date_today, text.timing.hour_start))

					# 	moon_dt_user = moon_dt_user - timedelta(1,0)
					# 	scheduled_date = user_timezone.localize(datetime.combine(moon_dt_user.date(), text.timing.hour_start))
					# 	scheduled_date = scheduled_date.astimezone(pytz.UTC)

					# 	time_to_send = scheduled_date + timedelta(0,randint(0,round(time_window.total_seconds())))
					# 	text_to_send = "The " + dataj['phasedata'][0]['phase'] + " will happen at "  + str(moon_dt_user.strftime('%-I:%M %p')) + " on " + str(moon_dt_user.strftime(' %B %d, %Y')) + "!"

					# 	atext = ActualText(user=text.user,text=text,time_to_send=time_to_send,text_sent=text_to_send)
					# 	atext.save()


		



		










	# # requests.get('s')
	# try:
	# 	data = requests.get('http://api.usno.navy.mil/rstt/oneday?date='+ date_now +'&loc=San Francisco, CA')
	# 	dataj = data.json()
	# 	output = dataj
	# except:
	# 	dataj = "NOT FOUND"

	# if dataj != "NOT FOUND":
	# 	print(dataj['sundata'])
	# 	print(len(dataj['sundata']))
	# 	for i in range(len(dataj['sundata'])):
	# 		print(i)
	# 		print("phen",dataj['sundata'][i]['phen'])
	# 		if dataj['sundata'][i]['phen'] == 'R':
	# 			working_texts = PossibleText.objects.all().filter(tmp_save=False).filter(active=True).filter(text_type="sun").filter(text="Sun Rise")
	# 		elif dataj['sundata'][i]['phen'] == 'U':
	# 			working_texts = PossibleText.objects.all().filter(tmp_save=False).filter(active=True).filter(text_type="sun").filter(text="Upper Transit")
	# 		elif dataj['sundata'][i]['phen'] == 'S':
	# 			working_texts = PossibleText.objects.all().filter(tmp_save=False).filter(active=True).filter(text_type="sun").filter(text="Sun Set")

	# 		if working_texts.count() > 0:
	# 			for text in working_texts:
	# 				working_settings = UserSetting.objects.all().get(user=text.user)

	# 				



	# 				user_timezone = pytz.timezone(working_settings.timezone)
	# 				moon_dt_user = moon_dt_utc.astimezone(user_timezone)

	# 				# #See if there is a text scheduled in the future for this phase.  if not, then schedule it.
	# 				if ActualText.objects.all().filter(user=text.user).filter(text=text).filter(time_to_send__gte=pytz.utc.localize(datetime.now())).count() < 1:
	# 					date_today = datetime.now(pytz.utc).astimezone(user_timezone)
	# 					time_window = user_timezone.localize(datetime.combine(date_today, text.timing.hour_end)) - user_timezone.localize(datetime.combine(date_today, text.timing.hour_start))

	# 					moon_dt_user = moon_dt_user - timedelta(1,0)
	# 					scheduled_date = user_timezone.localize(datetime.combine(moon_dt_user.date(), text.timing.hour_start))
	# 					scheduled_date = scheduled_date.astimezone(pytz.UTC)

	# 					time_to_send = scheduled_date + timedelta(0,randint(0,round(time_window.total_seconds())))
	# 					text_to_send = "The " + dataj['phasedata'][0]['phase'] + " will happen at "  + str(moon_dt_user.strftime('%-I:%M %p')) + " on " + str(moon_dt_user.strftime(' %B %d, %Y')) + "!"

	# 					atext = ActualText(user=text.user,text=text,time_to_send=time_to_send,text_sent=text_to_send)
	# 					atext.save()



				 





	
	return render(request,"SS_moon.html",context)


def test_signup(request):
	context = {}
	new_user_tmp = DefaultAccountAdapter.new_user(SignupForm,request)
	return render(request,"SS_home.html",context)

# create an inspiration
def create_inspiration(request, id=None):
	context={}
	return render(request,"SS_create_inspiration.html",context)

def get_create_inspiration(request):
	main_context = {} # to build out the specific html stuff
	response_data = {} # to send back to the template

	main_context['working_tags'] =  Tag.objects.all()

	if 'id' in request.POST.keys():
		print("ID HERE", request.POST['id'])
		if request.POST['id'] != None:
			if request.POST['id'] != '':
				main_context['editing_collection'] = Collection.objects.all().filter(user=request.user).get(id=int(request.POST['id']))


				tmp_tags = Collection.objects.all().filter(user=request.user).get(id=int(request.POST['id'])).tag

				tags = []
				for tag in tmp_tags.all():
					tags.append(tag.tag)

				main_context['tags'] = tags
			

	main_context['working_collection'] = Collection.objects.all()
	main_context['all_possible_texts'] = PossibleText.objects.all().filter(user=request.user).exclude(text__exact='')

	response_data["COLLECTION"] = render_to_string('SS_create_inspiration_content.html', main_context, request=request)
	
	# else
	return HttpResponse(json.dumps(response_data),content_type="application/json")		



def transfer_alt_texts(system_text,user_text):
	print("TRANSER TEXTS")
	print("ALT ", system_text.alt_text.all())
	if system_text.alt_text.all().count()>0:
		print("GREATER THAN 1")
		for text in system_text.alt_text.all():
			print("TEXT", text.alt_text)
			tmp = AlternateText(user=user_text.user,alt_text=text.alt_text)
			tmp.save()
			user_text.alt_text.add(tmp)
		user_text.save()
			


def inspiration_indvidual_text(request):
	main_context = {} # to build out the specific html stuff
	response_data = {} # to send back to the template

	tmp = PossibleText.objects.all().get(id=int(request.POST['selected_texts'].split('_')[1]))
	# print("ALT ", tmp.alt_text.all())
	user_text = tmp
	if PossibleText.objects.all().filter(user=request.user).filter(text=tmp.text).count()<1:
		print("CREATING!")
		timing = Timing.objects.all().get(id=tmp.timing.id)

		timing.pk=None
		timing.intended_text_input=""
		timing.user=request.user
		user_text.default_timing=False
		timing.save()

		user_text.pk=None
		user_text.timing=timing
		user_text.user=request.user
		user_text.tmp_save=False

		user_text.quick_suggestion=False
		user_text.date_created=datetime.now(pytz.utc)
		user_text.input_text = ''
		user_text.save()

		transfer_alt_texts(PossibleText.objects.all().get(id=int(request.POST['selected_texts'].split('_')[1])),user_text)

		if 'quick_suggestion' in request.POST.keys():
			if request.user.is_authenticated():	
				qs = QuickSuggestion(user=request.user,date=datetime.now(pytz.utc),text=tmp,added=True)
				qs.save()

		response_data['save_type']="added"
		# html_out = '<div  id = "_" ' + request.POST['selected_texts'].split('_')[1] + ' " class = "waves-effect waves-red btn-flat chip add-text-inspiration-btn"><span class="add-text-inspiration-btn"> <i class="material-icons" >delete</i> </span></div>'

		

	else:
		print("REMOVING!")
		possible_texts = PossibleText.objects.all().filter(user=request.user).filter(text=tmp.text)
		for text in possible_texts:
			text.delete()
		response_data['save_type']="removed"
		# html_out = '<a href="#text_add_confirm" id = "_" ' + request.POST['selected_texts'].split('_')[1] + ' " class = "waves-effect waves-red btn-flat chip add-text-inspiration-btn"><span> <i class="material-icons" >plus</i> </span></a>'
		

	# response_data['html_out'] = html_out



	return HttpResponse(json.dumps(response_data),content_type="application/json")	



# Create your views here.
def text(request,id=None,slug=None):	
	if id == None:
		context = {}
		if request.user.is_authenticated():	
			if UserSetting.objects.all().filter(user=request.user).count() > 0:
				working_settings = UserSetting.objects.all().get(user=request.user)
				if working_settings.settings_complete == True:
					return render(request,"SS_text_specific.html",context)
				else:
					return HttpResponseRedirect('/consumer/settings/')
		else:
			return render(request,"SS_text_specific.html",context)
	
		return render(request,"SS_text_specific.html",context)
	else:
		context = {}
		working_text = PossibleText.objects.all().get(id=id)
		context['working_text'] = working_text

		if request.user.is_authenticated():	
			if PossibleText.objects.all().filter(user=request.user).filter(text=working_text.text).count()>0:
				user_text = PossibleText.objects.all().filter(user=request.user).filter(text=working_text.text).first()
				user_text = PossibleText.objects.all().filter(user=request.user).get(id=user_text.id)
				context['user_text'] = user_text		
	
		return render(request,"SS_text_specific.html",context)


def program(request,id=None,slug=None):	
	if id == None:
		print("COLLECTION NAME -----ID IS NON")
		context = {}
		if request.user.is_authenticated():	
			if UserSetting.objects.all().filter(user=request.user).count() > 0:
				working_settings = UserSetting.objects.all().get(user=request.user)
				if working_settings.settings_complete == True:
					return render(request,"SS_inspiration.html",context)
				else:
					return HttpResponseRedirect('/consumer/settings/')
		else:
			return render(request,"SS_inspiration.html",context)
	
		return render(request,"SS_inspiration.html",context)
	else:
		# print("COLLECTION NAME ----- ", working_collection.collection_name)
		working_collection = Collection.objects.all().get(id=id)
		key = 1
		collection_info = {}
		burden = float(0)
		for text in working_collection.texts.all():
			burden = burden + text.timing.timing_burden_number()
			if request.user.is_authenticated():	
				collection_list = {
					'text': text,
					'user': PossibleText.objects.all().filter(user=request.user).filter(text=text).count(),
				}
			else:
				collection_list = {
					'text': text,
					'user': 0,
				}
			
			
			collection_info[key]= collection_list
			key = key + 1


		collection_info = tuple(collection_info.items())
		number_of_texts = working_collection.texts.all().count()



		context = {
		'working_collection': working_collection,
		'collection_info': collection_info,
		'number_of_texts': number_of_texts,
		'burden': round(burden,2),
		}

		if working_collection.collection_name=='sun':
			return render(request,"SS_inspiration_specific_sun.html",context)
		else:
			return render(request,"SS_inspiration_specific.html",context)

	
		



def get_inspiration_display(request):
	main_context = {} # to build out the specific html stuff
	response_data = {} # to send back to the template

	key = 1
	collection_info = {}

	working_filters = Q()
	working_filters.add(Q(publish=True),Q.AND)

	if 'collection_switch' in request.POST.keys():
		if request.POST['collection_switch'] == "true":
			print("COLLECTION TRUE")
			working_filters.add(Q(user=request.user),Q.AND)
			# working_collection = Collection.objects.all().filter(user=request.user)
			main_context['collection_switch_check'] = "true"
		else:
			working_filters.add(Q(publish=True),Q.AND)
			# working_collection = Collection.objects.all().filter(publish=True)

	if 'collection_tags' in request.POST.keys():
		working_tags = request.POST['collection_tags'].split(',')
		main_context['searched_tags'] = request.POST['collection_tags']

		for tag in working_tags:
			print("TAG", tag)
			print("TAG", str(tag).split("_")[0] )
			if str(tag).split("_")[0] == "tag":
				tmp = Tag.objects.all().filter(tag=str(tag).split("_")[1])
				working_filters.add(Q(tag__in=tmp),Q.AND)
			else:
				print("NAME", tag.split("_"))
				working_filters.add(Q(collection=str(tag).split("_")[1]),Q.AND)

	working_collection = Collection.objects.all().filter(working_filters).order_by('ordering')

	for collection in working_collection:
		collection_list = {}
		collection_list = {
			"collection": collection,
			# "heatmap": get_collection_heatmap(request=request,collection=collection)
		}

		collection_info[key] = collection_list
		key = key + 1

	collection_info = tuple(collection_info.items())
	main_context['collection_info'] = collection_info

	#These are for the search bar
	main_context['collection_names'] = Collection.objects.all().filter(publish=True)
	main_context['working_tags'] = Tag.objects.all().filter(collection__in=Collection.objects.all().filter(publish=True)).distinct()



	response_data["inspiration_display"] = render_to_string('SS_inspiration_display.html', main_context, request=request)
	
	# else
	return HttpResponse(json.dumps(response_data),content_type="application/json")	

def submit_beta(request):	
	main_context = {} # to build out the specific html stuff
	response_data = {} # to send back to the template
	working_beta = Beta(user=request.user,content=request.POST['beta_content'],date_created=pytz.utc.localize(datetime.now()))
	working_beta.save()
	response_data["message"] = "Feedback Submitted!  Thank you for your help!"

	return HttpResponse(json.dumps(response_data),content_type="application/json")	

def submit_quotation(request):	
	main_context = {} # to build out the specific html stuff
	response_data = {} # to send back to the template
	if request.user.is_authenticated():	
		working_quotation = Quotation(user=request.user,content=request.POST['quotation_content'],source=request.POST['quotation_source'],date_created=pytz.utc.localize(datetime.now()))
	else:
		working_quotation = Quotation(email=request.POST['quotation_email'],content=request.POST['quotation_content'],source=request.POST['quotation_source'],date_created=pytz.utc.localize(datetime.now()))
	working_quotation.save()
	response_data["message"] = "Quotation Submitted!  Thank you for your help!"

	return HttpResponse(json.dumps(response_data),content_type="application/json")		

def quotation(request):	
	context = {}
	
	content_place = "What is a great quote that inspires you?"
	source_place = "Who wrote this?  Where did you find it?"



	context['quotation_content_place'] = content_place
	context['quotation_source_place'] = source_place




	return render(request,"SS_quotation.html",context)

def beta(request):	
	context = {}
	return render(request,"SS_beta.html",context)	

def about(request):	
	context = {}
	return render(request,"SS_about.html",context)

def text_commands(request):	
	context = {}
	return render(request,"SS_text_commands.html",context)	
			
		

# Create your views here.

def guided_tour(request):
	context = {}
	if request.user.is_authenticated():	
		if UserSetting.objects.all().filter(user=request.user).count() > 0:
			working_settings = UserSetting.objects.all().get(user=request.user)
			if working_settings.settings_complete == True:
				working_texts = PossibleText.objects.all().filter(user=request.user)
				
				context = {
					'working_texts': working_texts,
					'working_settings': working_settings,
					}
				return render(request,"SS_home.html",context)
			else:
				return HttpResponseRedirect('/consumer/settings/')
		else:
			return HttpResponseRedirect('/consumer/settings/')

	return render(request,"SS_home.html",context)

def home(request):
	context = {}
	if request.user.is_authenticated():	
		if UserSetting.objects.all().filter(user=request.user).count() > 0:
			working_settings = UserSetting.objects.all().get(user=request.user)
			if working_settings.settings_complete == True:
				working_texts = PossibleText.objects.all().filter(user=request.user)
				
				context = {
					'working_texts': working_texts,
					'working_settings': working_settings,
					}
				return render(request,"SS_home.html",context)
			else:
				return HttpResponseRedirect('/consumer/settings/')
		else:
			return HttpResponseRedirect('/consumer/settings/')

	return render(request,"SS_home.html",context)
	
	
			

def settings(request):
	if request.user.is_authenticated():	
		working_carrier = Carrier.objects.all()
		working_tz = pytz.country_timezones['us']
		
		if UserSetting.objects.all().filter(user=request.user).count()<1:
			working_settings = UserSetting(user=request.user,begin_date=pytz.utc.localize(datetime.now()))
			working_settings.save()
		else:
			working_settings = UserSetting.objects.all().get(user=request.user)
		print("CITY STATE", working_settings.city_state())
		

		context={
		'working_carrier': working_carrier,
		'working_tz': working_tz,
		'working_settings': working_settings,
		}

		if working_settings.settings_complete == False:
			context['message'] = "Please complete the settings before you can schedule texts"

		return render(request,"SS_settings.html",context)
	else:
		return HttpResponseRedirect('/consumer/about/')

# get text data
def get_text_datatable_response(request):
	main_context = {} # to build out the specific html stuff
	response_data = {} # to send back to the template

	if request.user.is_authenticated():	
		working_settings = UserSetting.objects.all().get(user=request.user)
		main_context['user_timezone'] = working_settings.timezone

		if 'find_user_text' in request.POST.keys():
			tmp_text = PossibleText.objects.all().get(id=int(request.POST['id']))
			if PossibleText.objects.all().filter(user=request.user).filter(text=tmp_text).count()>0:
				working_text = PossibleText.objects.all().filter(user=request.user).get(text=tmp_text)
				working_texts = ActualText.objects.all().filter(user=request.user).filter(text=working_text).filter(time_sent__isnull=False)
		
				main_context['working_texts'] = working_texts
				main_context['text_content'] = working_text.text
				main_context['id'] = working_text.id
				response_data["text_datatable_response"] = render_to_string('SS_text_datatable_response.html', main_context, request=request)
			else:
				response_data["text_datatable_response"] = ""
		else:
			working_text = PossibleText.objects.all().filter(user=request.user).get(id=int(request.POST['id']))
			working_texts = ActualText.objects.all().filter(user=request.user).filter(text=working_text).filter(time_sent__isnull=False)
		
			main_context['working_texts'] = working_texts
			main_context['text_content'] = working_text.text
			main_context['id'] = working_text.id
			response_data["text_datatable_response"] = render_to_string('SS_text_datatable_response.html', main_context, request=request)


	# get the summary information 
	
	# else
	return HttpResponse(json.dumps(response_data),content_type="application/json")

def get_csv(request,id=None):
	print("CSV ____======")
	main_context = {} # to build out the specific html stuff
	response_data = {} # to send back to the template

	if id != None:
		working_text = PossibleText.objects.all().filter(user=request.user).get(id=id)
		working_texts = ActualText.objects.all().filter(user=request.user).filter(text=working_text)
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="sentimini_data_' + working_text.text + '.csv"'
		writer = csv.writer(response)

		headers = ["text_sent","time_sent","time_response","response"]
		writer.writerow(headers)

		for tmp in working_texts:
			row = [tmp.text_sent, tmp.time_sent,tmp.time_response,tmp.response]
			writer.writerow(row)
	else:
		working_texts = ActualText.objects.all().filter(user=request.user)
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="sentimini_data_all.csv"'
		writer = csv.writer(response)

		headers = ["text", "time_sent","time_response","response"]
		writer.writerow(headers)

		for tmp in working_texts:
			row = [tmp.text,tmp.time_sent,tmp.time_response,tmp.response]
			writer.writerow(row)

	return response

	# response_data['save_message'] = ".csv downloaded!"
	

	# return HttpResponse(json.dumps(response_data),content_type="application/json")



# This is to just initialize the main text input box
def get_text_input(request):
	main_context = {} 
	response_data = {}
	main_context['text_message'] = "New Text"
	if request.user.is_authenticated():	
		working_timing = get_timing_default(request)
		# working_timing = Timing.objects.all().filter(user=request.user).get(default_timing=True)
		main_context['timing_summary'] = working_timing.timing_summary
		main_context['working_timing'] = working_timing
		main_context['text_message'] = request.POST['text_message']
		# main_context['timing_summary'] = working_timing.timing_summary

	response_data["text_input"] = render_to_string('SS_new_text.html', main_context, request=request)
	return HttpResponse(json.dumps(response_data),content_type="application/json")

# This is to just initialize the main datatable
def get_text_datatable(request):
	main_context = {} 
	response_data = {}
	if request.user.is_authenticated():	
		working_settings = UserSetting.objects.all().get(user=request.user)
		main_context['user_timezone'] = working_settings.timezone
		main_context['working_texts'] = PossibleText.objects.all().filter(user=request.user).filter(tmp_save=False)

	
	print("GETTING DATA TABLE -------- ")
	response_data["text_datatable"] = render_to_string('SS_text_datatable.html', main_context, request=request)
	return HttpResponse(json.dumps(response_data),content_type="application/json")	


def get_quick_suggestions(request):
	main_context = {} 
	response_data = {}


	object_id_list = []
	if request.user.is_authenticated():	
		working_texts = PossibleText.objects.all().filter(user=request.user).filter(tmp_save=False)
		rejected_list = QuickSuggestion.objects.all().filter(user=request.user).filter(rejected=True)

		for text in working_texts:
			object_id_list.append(text.text)
		for text in rejected_list:
			object_id_list.append(text.text)

	if 'current_suggestions[]' in request.POST.keys():
		current_ids = request.POST.getlist('current_suggestions[]')		
		# current_ids.replace("_",'')
		current_ids = [idz.replace('_','') for idz in current_ids]
		print("CURRENT IDS", current_ids)
	else:
		current_ids=[]

	
	if 'suggestion_1' in request.POST.keys():
		if request.POST['suggestion_1'] == "yes":
			quick_text = PossibleText.objects.all().filter(quick_suggestion=True).exclude(id__in=current_ids).exclude(text__in=object_id_list).order_by('?').first()
			current_ids.append(quick_text.id)

			tmp_context = {'working_text': quick_text,
			'suggestion_number': "1",
			}

			if quick_text != None:
				if request.user.is_authenticated():	
					if request.POST['save_suggestions'] == "yes":
						qs = QuickSuggestion(user=request.user,date=datetime.now(pytz.utc),text=quick_text)
						if 'rejected' in request.POST.keys():
							qs.rejected=True
						qs.save()

			response_data["suggestion_1"] = render_to_string('SS_quick_suggestions.html', tmp_context, request=request)
	
	if 'suggestion_2' in request.POST.keys():
		if request.POST['suggestion_2'] == "yes":
			quick_text = PossibleText.objects.all().filter(quick_suggestion=True).exclude(id__in=current_ids).exclude(text__in=object_id_list).order_by('?').first()
			current_ids.append(quick_text.id)

			tmp_context = {'working_text': quick_text,
			'suggestion_number': "2",}

			if quick_text != None:
				if request.user.is_authenticated():	
					if request.POST['save_suggestions'] == "yes":
						qs = QuickSuggestion(user=request.user,date=datetime.now(pytz.utc),text=quick_text)
						if 'rejected' in request.POST.keys():
							qs.rejected=True
						qs.save()

			response_data["suggestion_2"] = render_to_string('SS_quick_suggestions.html', tmp_context, request=request)

	if 'suggestion_3' in request.POST.keys():
		if request.POST['suggestion_3'] == "yes":
			quick_text = PossibleText.objects.all().filter(quick_suggestion=True).exclude(id__in=current_ids).exclude(text__in=object_id_list).order_by('?').first()
			current_ids.append(quick_text.id)
			
			tmp_context = {'working_text': quick_text,
			'suggestion_number': "3",}

			if quick_text != None:
				if request.user.is_authenticated():	
					if request.POST['save_suggestions'] == "yes":
						qs = QuickSuggestion(user=request.user,date=datetime.now(pytz.utc),text=quick_text)
						if 'rejected' in request.POST.keys():
							qs.rejected=True
						qs.save()

			response_data["suggestion_3"] = render_to_string('SS_quick_suggestions.html', tmp_context, request=request)		

	
	return HttpResponse(json.dumps(response_data),content_type="application/json")	




# This is to change the timing option
# 1.  Should be able to return to whatever text was being edited
# 2.  Should be able to load and change default timing options
def get_timing_option_input(request):
	main_context = {} 
	response_data = {}

	# GET THE DEFAULT TIMING OBJECT.  IF NOT THEN CREATE ONE
	if 'id' in request.POST.keys():
		if request.POST['id'] != None and request.POST['id'] != "":
			working_text = PossibleText.objects.all().filter(user=request.user).get(id=int(request.POST['id']))
			working_timing = working_text.timing
		else:
			working_timing = get_timing_default(request)
			

	#SAVE THE TEXT TEMPORARY
	if 'id' in request.POST.keys():
		print("ID IN KEYS")
		if request.POST['id'] != "None" and request.POST['id'] != "":
			print("ID", request.POST['id'])
			working_text = PossibleText.objects.all().filter(user=request.user).get(id=int(request.POST['id']))
		else:
			working_text = PossibleText(user=request.user,date_created=datetime.now(pytz.utc))
	else:
		working_text = PossibleText(user=request.user,date_created=datetime.now(pytz.utc))	

	if 'text_content' in request.POST.keys():
		main_context['text_content'] = request.POST['text_content']	
		working_text.text = request.POST['text_content']
	else:
		main_context['text_content'] =working_text.text

	
	working_text.timing = working_timing
	if request.POST['timing_message'] == "Timing":
		working_text.tmp_save = True
	working_text.save()

	main_context['working_text'] = working_text
	main_context['id'] = working_text.id
	main_context['working_timing'] = working_timing
	main_context['fuzzy_denomination'] = working_timing.fuzzy_denomination
	main_context['timing_message'] = request.POST['timing_message']
	print("HERE HERE HERE")

	

	# if fuzzy == True:
	response_data["timing_option_input"] = render_to_string('SS_timing_options_periodic.html', main_context, request=request)


def get_timing_default(request):
	if Timing.objects.all().filter(user=request.user).filter(default_timing=True).count()>0:
		# working_timing = Timing.objects.all().filter(user=request.user).get(default_timing=True)
		working_timing = Timing.objects.all().filter(user=request.user).filter(default_timing=True).last()
	else:
		working_timing = Timing(user=request.user,default_timing=True, repeat=True)
		working_timing.fuzzy = False
		working_timing.fuzzy_denomination = "days"
		working_timing.iti_raw = 3
		working_timing.iti_noise = 2
		working_timing.decay_check = True
		working_timing.private_check = False
		working_timing.hour_start_value = 540
		working_timing.hour_end_value = 1260
		working_timing.date_start = datetime.now(pytz.utc)
		working_timing.repeat_in_window = 1

		iti = working_timing.iti_raw
		demo = working_timing.fuzzy_denomination

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


		working_timing.save()

	return working_timing


def get_input_to_options(request):
	main_context = {} 
	response_data = {}
	main_context['timing_message'] = "Timing Options"

	if request.user.is_authenticated():	

		# GET THE DEFAULT TIMING OBJECT.  IF NOT THEN CREATE ONE
		if 'id' in request.POST.keys():
			if request.POST['id'] != None and request.POST['id'] != "":
				working_text = PossibleText.objects.all().filter(user=request.user).get(id=int(request.POST['id']))
				working_timing = working_text.timing
			else:
				working_timing = get_timing_default(request)
				

		#SAVE THE TEXT TEMPORARY
		if 'id' in request.POST.keys():
			print("ID IN KEYS")
			if request.POST['id'] != "None" and request.POST['id'] != "":
				print("ID", request.POST['id'])
				working_text = PossibleText.objects.all().filter(user=request.user).get(id=int(request.POST['id']))
			else:
				working_text = PossibleText(user=request.user,date_created=datetime.now(pytz.utc))
		else:
			working_text = PossibleText(user=request.user,date_created=datetime.now(pytz.utc))	

		if 'text_content' in request.POST.keys():
			main_context['text_content'] = request.POST['text_content']	
			working_text.text = request.POST['text_content']
		else:
			main_context['text_content'] =working_text.text

		
		working_text.timing = working_timing
		if request.POST['timing_message'] == "Timing":
			working_text.tmp_save = True
		working_text.save()

		main_context['working_text'] = working_text
		main_context['id'] = working_text.id
		main_context['working_timing'] = working_timing
		main_context['fuzzy_denomination'] = working_timing.fuzzy_denomination
		main_context['timing_message'] = request.POST['timing_message']

	response_data["text_input"] = render_to_string('SS_timing_options.html', main_context, request=request)

	return HttpResponse(json.dumps(response_data),content_type="application/json")


#for some reason this is how to get the edit thing
def get_options_to_input(request):
	main_context = {} 
	response_data = {}

	working_text = PossibleText.objects.all().filter(user=request.user).get(id=int(request.POST['id']))
	
	working_timing = Timing.objects.all().filter(user=request.user).filter(default_timing=True)[0]
	default_timing = Timing.objects.all().filter(user=request.user).get(id=working_timing.id)
	
	main_context['id'] = working_text.id
	

	if working_text.tmp_save == True:
		main_context['working_text'] = working_text
		main_context['working_timing'] = working_text.timing
	else:
		main_context['timing_summary'] = default_timing.timing_summary

	if 'text_message' in request.POST.keys():
		main_context['working_text'] = working_text
		main_context['working_timing'] = working_text.timing
		main_context['text_message'] = request.POST['text_message']
	else:
		main_context['text_message'] = "New Text"

	main_context['alternative_texts'] = working_text.alt_text.all()


	response_data["text_input"] = render_to_string('SS_new_text.html', main_context, request=request)
	return HttpResponse(json.dumps(response_data),content_type="application/json")


def save_timing_function(request,working_timing):
	# SAVE THE VALUES
	if 'hour_start' in request.POST.keys():
		working_timing.hour_start = datetime.strptime(request.POST['hour_start'],'%I:%M %p')
	if 'hour_end' in request.POST.keys():
		working_timing.hour_end = datetime.strptime(request.POST['hour_end'],'%I:%M %p')
	if 'hour_start_value' in request.POST.keys():
		working_timing.hour_start_value = int(request.POST['hour_start_value'].split(".")[0])
	if 'hour_end_value' in request.POST.keys():
		working_timing.hour_end_value = int(request.POST['hour_end_value'].split(".")[0])

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

	if 'weekdays' in request.POST.keys():
		print("HERE")
		print(request.POST['weekdays'])
		working_timing.sunday=False
		working_timing.monday=False
		working_timing.tuesday=False
		working_timing.wednesday=False
		working_timing.thursday=False
		working_timing.friday=False
		working_timing.saturday=False

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
				
	if 'fuzzy' in request.POST.keys():
		if request.POST['fuzzy'] == "true":
			working_timing.fuzzy = True
		else:
			working_timing.fuzzy = False

	if 'num_repeats' in request.POST.keys():
		working_timing.repeat_in_window = request.POST['num_repeats']		
		
	working_timing.save()
	return working_timing


def save_timing(request):
	main_context = {} 
	response_data = {}

	if 'id' in request.POST.keys():
		print("ID", request.POST['id'])
		print("CONDITIONS", request.POST['id']=="")
		if request.POST['id'] != "None" and request.POST['id'] != "" and request.POST['id'] is not None:
			working_text = PossibleText.objects.all().filter(user=request.user).get(id=int(request.POST['id']))
		else:
			working_text = PossibleText(user=request.user,date_created=datetime.now(pytz.utc))
	else:
		working_text = PossibleText(user=request.user,date_created=datetime.now(pytz.utc))

	working_text.save()



	if 'alt_texts[]' in request.POST.keys():
		alt_ids = request.POST.getlist('alt_texts_ids[]')
		# alt_ids = request.POST['alt_texts_ids'].split,
		alt_texts = request.POST.getlist('alt_texts[]')

		print("alt_ids",alt_ids)
		print("alt_texts",alt_texts)


		# Remove any of the deleted alt texts
		for alt in working_text.alt_text.all():
			if not str(alt.id) in str(alt_ids):
				alt.delete()

		#Update or create any new alts
		i = 0
		for alt in alt_texts:
			if i < len(alt_ids):
				if alt_ids[int(i)] != None:
					print("update old")
					working_alt = working_text.alt_text.all().get(id=alt_ids[int(i)])
					working_alt.alt_text = str(alt)
					working_alt.save()
				else:
					print("create new")
					if str(alt) != '' and str(alt) != None:
						print("ALT", str(alt))
						working_alt = AlternateText(user=request.user,alt_text=str(alt))
						working_alt.save()
						working_text.alt_text.add(working_alt)
			else:
				print("create new")
				if str(alt) != '' and str(alt) != None:
					working_alt = AlternateText(user=request.user,alt_text=str(alt))
					working_alt.save()
					working_text.alt_text.add(working_alt)



			i = i + 1
		
		working_text.save()


	#See if there is a timing associated with it, if not assign the default
	if working_text.timing == None:
		working_timing = Timing(user=request.user,default_timing=False, fuzzy=True, repeat=True, date_start=datetime.now(pytz.utc))
		working_text.timing = working_timing
	else:
		working_timing = working_text.timing

	working_text.text = request.POST['text_content']
	working_timing = save_timing_function(request,working_timing)
	working_text.timing = working_timing

	# print("SAVE TIMING", request.POST.keys())

	print(request.POST['save_type'])

	if request.POST['save_type'] == 'options_text_save':
		print("SAVE TIMING AND TEXST")
		working_text.tmp_save = False
		working_text.save()
		working_timing = get_timing_default(request)
		main_context['working_timing'] = working_timing

	else:
		print("SAVE TIMING ONLY")
		working_text.tmp_save = True
		working_text.save()

		main_context['working_text'] = working_text
		main_context['id'] = working_text.id
		main_context['working_timing'] = working_text.timing


	
	main_context['text_message'] = "New Text"

	response_data["text_input"] = render_to_string('SS_new_text.html', main_context, request=request)
	return HttpResponse(json.dumps(response_data),content_type="application/json")	

# THESE WILL BE FOR SAVING
def save_text(request):
	main_context = {} 
	response_data = {}

	if 'id' in request.POST.keys():
		print("ID IN KEYS")
		if request.POST['id'] != "None" and request.POST['id'] != "":
			print("ID", request.POST['id'])
			working_text = PossibleText.objects.all().filter(user=request.user).get(id=int(request.POST['id']))
		else:
			print("ID IS NONE")
			working_text = PossibleText(user=request.user,date_created=datetime.now(pytz.utc))
	else:
		print("ID NOT IN KEYS")
		working_text = PossibleText(user=request.user,date_created=datetime.now(pytz.utc))
	
	working_text.text=request.POST['text_content']

	#See if there is a timing associated with it, if not assign the default
	
	if working_text.timing == None:
		working_timing = get_timing_default(request)
		working_text.timing = working_timing

	working_text.tmp_save = False
	working_text.save()

	if 'text_message' in request.POST.keys():
		main_context['text_message'] = request.POST['text_message']
	else:
		main_context['text_message'] = "New Text"

	working_timing = get_timing_default(request)
	# main_context['timing_summary'] = working_timing.timing_summary
	main_context['working_timing'] = working_timing

	#If there are default options then get t

	response_data["text_input"] = render_to_string('SS_new_text.html', main_context, request=request)
	return HttpResponse(json.dumps(response_data),content_type="application/json")

def save_timing_default(request):
	main_context = {} 
	response_data = {}

	if Timing.objects.all().filter(user=request.user).filter(default_timing=True).count()>0:
		working_timing = Timing.objects.all().filter(user=request.user).get(default_timing=True)
	else:
		working_timing = Timing(user=request.user,default_timing=True, fuzzy=True, repeat=True)

	working_timing = save_timing_function(request,working_timing)
	working_timing.save()

	response_data['message'] = "defaults saved!"
	return HttpResponse(json.dumps(response_data),content_type="application/json")




	# 'hour_start': start_time,
 #      'hour_end': end_time,
 #      'hour_start_value': slider.noUiSlider.get()[0],
 #      'hour_end_value': slider.noUiSlider.get()[1],
 #      'iti': ITI_mean,
 #      'iti_noise': ITI_noise,
 #      'fuzzy_denomination': $('#fuzzy_denomination').val(),
 #      'decay': $('#decay_check').is(':checked'),
 #      'private': $('#private_check').is(':checked'),

