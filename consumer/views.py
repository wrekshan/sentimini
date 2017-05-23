from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
import json
from datetime import datetime, timedelta, time, date
import pytz
from allauth.account.adapter import get_adapter, DefaultAccountAdapter
from sentimini.forms import SignupFormWithoutAutofocus
from allauth.account.forms import SignupForm

from sentimini.views import pause_text
from ent.models import ActualText, PossibleText, Timing, Carrier, UserSetting, Collection, Tag
from django.db.models import Q

import csv

def test_signup(request):
	context = {}
	# get_adapter()
	# print("test_signup pressed!")
	# username = "hahahha"
	# password = "1234567"

	# form_tmp = SignupForm()
	# form_tmp.username = "hahaha"
	# form_tmp.email = "Aa12345678@asdf.com"
	# form_tmp.password1 = "Aa12345678"
	# form_tmp.password2 = "Aa12345678"

	# print("CLEAN:", DefaultAccountAdapter.clean_username(form_tmp,form_tmp.username))

	# form_tmp.cleaned_data = []
	# form_tmp.cleaned_data.username = "hahaha"
	# form_tmp.cleaned_data.email = "Aa12345678@asdf.com"
	# form_tmp.cleaned_data.password1 = "Aa12345678"
	# form_tmp.cleaned_data.password2 = "Aa12345678"

	
	
	# print("CLEAN", SignupForm.clean(form_tmp))

	# print(form_tmp.clean())
	# print(form_tmp.cleaned_data)


	

	new_user_tmp = DefaultAccountAdapter.new_user(SignupForm,request)
	# print(new_user_tmp)
	# DefaultAccountAdapter.save_user(new_user_tmp,request,SignupForm,form_tmp)

	# save_user(self, request, user, form):
	# print("test_signup pressed!")
	return render(request,"SS_home.html",context)


# Create your views here.
def inspiration(request):	
	context = {}
	return render(request,"SS_inspiration.html",context)

def get_inspiration_display(request):
	main_context = {} # to build out the specific html stuff
	response_data = {} # to send back to the template

	key = 1
	collection_info = {}

	working_filters = Q()

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

	working_collection = Collection.objects.all().filter(working_filters)

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



def about(request):	
	context = {}
	return render(request,"SS_about.html",context)
			
		

# Create your views here.
def home(request):
	if request.user.is_authenticated():	
		if UserSetting.objects.all().filter(user=request.user).count() > 0:
			working_settings = UserSetting.objects.all().get(user=request.user)
			if working_settings.settings_complete == True:
				working_texts = PossibleText.objects.all().filter(user=request.user)
				
				context = {
					'working_texts': working_texts,
					}			
				return render(request,"SS_home.html",context)
			else:
				return HttpResponseRedirect('/consumer/settings/')
		else:
			return HttpResponseRedirect('/consumer/settings/')
	else:
		return HttpResponseRedirect('/consumer/about/')
			

def settings(request):
	if request.user.is_authenticated():	
		working_carrier = Carrier.objects.all()
		working_tz = pytz.country_timezones['us']
		
		if UserSetting.objects.all().filter(user=request.user).count()<1:
			working_settings = UserSetting(user=request.user,begin_date=pytz.utc.localize(datetime.now()))
			working_settings.save()
		else:
			working_settings = UserSetting.objects.all().get(user=request.user)

		

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

	working_text = PossibleText.objects.all().filter(user=request.user).get(id=int(request.POST['id']))
	working_texts = ActualText.objects.all().filter(user=request.user).filter(text=working_text)
	
	main_context['working_texts'] = working_texts
	main_context['text_content'] = working_text.text
	main_context['id'] = working_text.id


	# get the summary information 
	response_data["text_datatable_response"] = render_to_string('SS_text_datatable_response.html', main_context, request=request)
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

		headers = ["time_sent","time_response","response"]
		writer.writerow(headers)

		for tmp in working_texts:
			row = [tmp.time_sent,tmp.time_response,tmp.response]
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

	working_timing = get_timing_default(request)
	# working_timing = Timing.objects.all().filter(user=request.user).get(default_timing=True)
	main_context['timing_summary'] = working_timing.timing_summary
	main_context['text_message'] = request.POST['text_message']
	# main_context['timing_summary'] = working_timing.timing_summary

	response_data["text_input"] = render_to_string('SS_new_text.html', main_context, request=request)
	return HttpResponse(json.dumps(response_data),content_type="application/json")

# This is to just initialize the main datatable
def get_text_datatable(request):
	main_context = {} 
	response_data = {}

	main_context['working_texts'] = PossibleText.objects.all().filter(user=request.user).filter(tmp_save=False)
	
	response_data["text_datatable"] = render_to_string('SS_text_datatable.html', main_context, request=request)
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
		working_timing = Timing.objects.all().filter(user=request.user).get(default_timing=True)
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

def get_options_to_input(request):
	main_context = {} 
	response_data = {}

	working_text = PossibleText.objects.all().filter(user=request.user).get(id=int(request.POST['id']))
	default_timing = Timing.objects.all().filter(user=request.user).get(default_timing=True)
	
	main_context['id'] = working_text.id
	

	if working_text.tmp_save == True:
		main_context['working_text'] = working_text
		main_context['timing_summary'] = working_text.timing.timing_summary
	else:
		main_context['timing_summary'] = default_timing.timing_summary

	if 'text_message' in request.POST.keys():
		main_context['working_text'] = working_text
		main_context['timing_summary'] = working_text.timing.timing_summary
		main_context['text_message'] = request.POST['text_message']
	else:
		main_context['text_message'] = "Create New Text"


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

	working_text = PossibleText.objects.all().filter(user=request.user).get(id=int(request.POST['id']))
	if working_text.timing.default_timing == True:
		working_timing = Timing(user=request.user,default_timing=False, fuzzy=True, repeat=True, date_start=datetime.now(pytz.utc))
	else:
		working_timing = working_text.timing

	working_timing = save_timing_function(request,working_timing)
	working_text = PossibleText.objects.all().filter(user=request.user).get(id=int(request.POST['id']))
	working_text.timing = working_timing

	# print("SAVE TIMING", request.POST.keys())

	print(request.POST['save_type'])

	if request.POST['save_type'] == 'options_text_save':
		print("SAVE TIMING AND TEXST")
		working_text.tmp_save = False
		working_text.save()

	else:
		print("SAVE TIMING ONLY")
		working_text.tmp_save = True
		working_text.save()

		main_context['working_text'] = working_text
		main_context['id'] = working_text.id
		main_context['timing_summary'] = working_text.timing.timing_summary


	
	main_context['text_message'] = "Create New Text"

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
		main_context['text_message'] = "Create New Text"

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

