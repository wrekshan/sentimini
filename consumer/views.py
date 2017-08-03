from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from random import random, triangular, randint, gauss
from django.core.mail import send_mail
import json
from datetime import datetime, timedelta, time, date
import pytz
from allauth.account.adapter import get_adapter, DefaultAccountAdapter
from sentimini.forms import SignupFormWithoutAutofocus
from allauth.account.forms import SignupForm
from ent.models import AlternateText, Quotation, QuickSuggestion, Beta, ActualText, IdealText, PossibleText, Timing, Carrier, UserSetting, Program, Tag
from django.db.models import Q

import time
import requests
import csv

from sentimini.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, use_gmail

#######################################
####### ACTUAL VIEWS
#######################################
def beta(request):	
	context = {}
	return render(request,"SS_beta.html",context)	

def about(request):	
	context = {}
	return render(request,"SS_about.html",context)

def text_commands(request):	
	context = {}
	return render(request,"SS_text_commands.html",context)	
			
# This is so that one can click a link to the guided tour from the about page 
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

# caneval - i don't really know what's going on with the TZ....thought I switch to geographic locations	
def settings(request):
	if request.user.is_authenticated():	
		working_carrier = Carrier.objects.all()
		working_tz = pytz.country_timezones['us']
		
		if UserSetting.objects.all().filter(user=request.user).count()<1:
			working_settings = UserSetting(user=request.user,begin_date=pytz.utc.localize(datetime.now()))
			working_settings.save()
		else:
			working_settings = UserSetting.objects.all().get(user=request.user)
		# print("CITY STATE", working_settings.city_state())
		

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

# cankeep
# Display the specific view for the text
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

		if request.user.is_authenticated():	
			if PossibleText.objects.all().filter(user=request.user).filter(id=id).count()>0:
				user_text = PossibleText.objects.all().get(id=id)
				working_text = user_text.ideal_text
				context['user_text'] = user_text
			else:
				working_text = IdealText.objects.all().get(id=id)
		else:
			working_text = IdealText.objects.all().get(id=id)


		context['working_text'] = working_text
		return render(request,"SS_text_specific.html",context)		


# caneval - will probably hit a problem when going to IdealText

#this is to parse if it needs to check for the ideal text or the possible text
# def get_working_text(request,id):



def get_text_specific_overview(request):
	main_context = {} 
	response_data = {} 

	if request.user.is_authenticated():	
		if PossibleText.objects.all().filter(user=request.user).filter(id=int(request.POST['id'])).count()>0:
			user_text = PossibleText.objects.all().get(id=int(request.POST['id']))
			# working_text = user_text.ideal_text
			main_context['user_text'] = user_text 
			main_context['working_text'] = user_text
		else:
			working_text = IdealText.objects.all().get(id=int(request.POST['id']))
			main_context['working_text'] = working_text 
	else:
		working_text = IdealText.objects.all().get(id=int(request.POST['id']))
		main_context['working_text'] = working_text 
	
	# working_text = IdealText.objects.all().get(id=request.POST['id'])
	
	# if request.user.is_authenticated():	
	# 	if PossibleText.objects.all().filter(user=request.user).filter(text=working_text.text).count()>0:
	# 		user_text = PossibleText.objects.all().filter(user=request.user).filter(text=working_text.text).first()
	# 		user_text = PossibleText.objects.all().filter(user=request.user).get(id=user_text.id)
	# 		main_context['user_text'] = user_text

	
	response_data["text_specific_overview"] = render_to_string('SS_text_specific_overview.html', main_context, request=request)

	return HttpResponse(json.dumps(response_data),content_type="application/json")	


# cankeep
# Display the specific view for the program
# can the burden to use the model methods instead of this.
def program(request,id=None,slug=None):	
	# Display the program overivew if the specific page doesn't exist - I can probably remove this
	if id == None:
		context = {}
		if request.user.is_authenticated():	
			if UserSetting.objects.all().filter(user=request.user).count() > 0:
				working_settings = UserSetting.objects.all().get(user=request.user)
				if working_settings.settings_complete == True:
					return render(request,"SS_program.html",context)
				else:
					return HttpResponseRedirect('/consumer/settings/')
		else:
			return render(request,"SS_program.html",context)
	
		return render(request,"SS_program.html",context)
	else:
		working_program = Program.objects.all().get(id=id)
		key = 1
		program_info = {}
		
		for text in working_program.ideal_texts.all():
			if request.user.is_authenticated():	
				program_list = {
					'text': text,
					'user': PossibleText.objects.all().filter(user=request.user).filter(text=text).count(),
				}
			else:
				program_list = {
					'text': text,
					'user': 0,
				}
			
			
			program_info[key]= program_list
			key = key + 1


		program_info = tuple(program_info.items())

		context = {
		'working_program': working_program,
		'program_info': program_info,
		}

		if working_program.program_name=='sun':
			return render(request,"SS_program_specific_sun.html",context)
		else:
			return render(request,"SS_program_specific.html",context)



#######################################
####### SIMPLE ONE OFF COMMANDS
#######################################
# This is just to save the beta feedback
def submit_beta(request):	
	main_context = {} 
	response_data = {} 
	working_beta = Beta(user=request.user,content=request.POST['beta_content'],date_created=pytz.utc.localize(datetime.now()))
	working_beta.save()

	response_data["message"] = "Feedback Submitted!  Thank you for your help!"
	return HttpResponse(json.dumps(response_data),content_type="application/json")	

# This just sends the text now.  Intention is to make for a more trustable experience
# caneval - also need to fix so a bunch aren't sent at once
def send_text_now(request):
	main_context = {} 
	response_data = {} 

	# caneval - might need to have more logic to prevent failures (i.e. are the settings correct?)
	addressee = UserSetting.objects.all().get(user=request.user).sms_address
	send_mail('',str(request.POST['text']), str(EMAIL_HOST_USER), [addressee], fail_silently=False)
	return HttpResponse(json.dumps(response_data),content_type="application/json")	

# This is to add the alternate text form when user is adding/editing new text
def get_alternate(request):
	main_context = {} 
	response_data = {} 

	if "counter" in request.POST.keys():
		main_context['counter'] = request.POST['counter']

	response_data['alternate_form'] = render_to_string('SS_alternate.html', main_context, request=request)
	return HttpResponse(json.dumps(response_data),content_type="application/json")		

# This is part of the New User Steps, so that info can be displayed to new users.
# caneval - I know why this is call from the home page...I don't know why it is call from the text specific page
def change_nus(request):
	main_context = {} 
	response_data = {} 

	working_settings = UserSetting.objects.all().get(user=request.user)
	working_settings.new_user_step = 1
	working_settings.save()

	return HttpResponse(json.dumps(response_data),content_type="application/json")		



#######################################
########## CORE FUNCTIONS
#######################################
# This gets the default timing OR creates it if it isn't present
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
		# working_timing.date_start = datetime.now(pytz.utc)
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

# This gets the csv of any replies will download them all if no id is present
def get_csv(request,id=None):
	main_context = {}
	response_data = {} 

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


# This transfers alt texts to the user text
# caneval - I feel like there should be an easier way to do this....like out of the box many for many operation
def transfer_alt_texts(system_text,user_text):
	if system_text.alt_text.all().count()>0:
		for text in system_text.alt_text.all():
			tmp = AlternateText(user=user_text.user,alt_text=text.alt_text)
			tmp.save()
			user_text.alt_text.add(tmp)
		user_text.save()
			

# cankeep
# This add/removes
# This also is from the Quick Suggestions, so change the name of the function
# This signs up an indvidual text from the program specific pages (i.e. when user clicks on plus button.)
def program_indvidual_text(request):
	main_context = {} 
	response_data = {}
	
	ideal_text = IdealText.objects.all().filter(id=int(request.POST['selected_texts'].split('_')[1]))

	if PossibleText.objects.all().filter(user=request.user).filter(ideal_text=ideal_text).count()<1:
		tmp = IdealText.objects.all().get(id=int(request.POST['selected_texts'].split('_')[1]))
		user_text = PossibleText(user=request.user)
		user_text.timing = tmp.timing
		user_text.text = tmp.text
		user_text.ideal_text = tmp

		# Add text to user
		# if PossibleText.objects.all().filter(user=request.user).filter(ideal_text=tmp).count()<1:
		# canfun - saving text
		timing = Timing.objects.all().get(id=tmp.timing.id)

		timing.pk=None
		timing.intended_text_input=""
		timing.user=request.user
		user_text.default_timing=False
		timing.save() #caneval - does this add a new timing?  What it doing?

		user_text.pk=None
		user_text.timing=timing
		user_text.user=request.user
		user_text.tmp_save=False

		user_text.quick_suggestion=False
		user_text.date_created=datetime.now(pytz.utc)
		user_text.input_text = ''
		
		user_text.save()

		transfer_alt_texts(IdealText.objects.all().get(id=int(request.POST['selected_texts'].split('_')[1])),user_text)

		if 'quick_suggestion' in request.POST.keys():
			if request.user.is_authenticated():	
				qs = QuickSuggestion(user=request.user,date=datetime.now(pytz.utc),text=tmp,added=True)
				qs.save()

		response_data['save_type']="added"
		response_data['redirect'] = '/consumer/text/' + str(user_text.id) + '/' + str(user_text.slug())

	else:
		#remove text from user
		possible_texts = PossibleText.objects.all().filter(user=request.user).filter(id=int(request.POST['selected_texts'].split('_')[1]))
		
		for text in possible_texts:
			text.delete()
		response_data['save_type']="removed"
		
	return HttpResponse(json.dumps(response_data),content_type="application/json")	





# get text data
# This is the DT of responses accessed through the text specific
def get_text_datatable_response(request):
	main_context = {} # to build out the specific html stuff
	response_data = {} # to send back to the template

	if request.user.is_authenticated():	
		working_settings = UserSetting.objects.all().get(user=request.user)
		main_context['user_timezone'] = working_settings.timezone

		# caneval - this doesn't really makes sense because i will almost always try to find user textzs
		if PossibleText.objects.all().filter(user=request.user).filter(id=int(request.POST['id'])).count() > 0:
			tmp_text = PossibleText.objects.all().get(id=int(request.POST['id']))
			working_text = PossibleText.objects.all().filter(user=request.user).get(text=tmp_text)
			working_texts = ActualText.objects.all().filter(user=request.user).filter(text=working_text).filter(time_sent__isnull=False)
	
			main_context['working_texts'] = working_texts
			main_context['text_content'] = working_text.text
			main_context['id'] = working_text.id
			response_data["text_datatable_response"] = render_to_string('SS_text_datatable_response.html', main_context, request=request)
		else:
			response_data["text_datatable_response"] = ""

	return HttpResponse(json.dumps(response_data),content_type="application/json")


# This is to just initialize the main datatable
def get_text_datatable(request):
	main_context = {} 
	response_data = {}
	if request.user.is_authenticated():	
		working_settings = UserSetting.objects.all().get(user=request.user)
		main_context['user_timezone'] = working_settings.timezone
		main_context['working_texts'] = PossibleText.objects.all().filter(user=request.user).filter(tmp_save=False)

	response_data["text_datatable"] = render_to_string('SS_text_datatable.html', main_context, request=request)
	return HttpResponse(json.dumps(response_data),content_type="application/json")	

# This gets the quick suggestions
# you can obviously dry this up (as there are three repetitions)
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
			quick_text = IdealText.objects.all().filter(quick_suggestion=True).exclude(id__in=current_ids).exclude(text__in=object_id_list).order_by('?').first()
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
			quick_text = IdealText.objects.all().filter(quick_suggestion=True).exclude(id__in=current_ids).exclude(text__in=object_id_list).order_by('?').first()
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
			quick_text = IdealText.objects.all().filter(quick_suggestion=True).exclude(id__in=current_ids).exclude(text__in=object_id_list).order_by('?').first()
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


#######################################
########### UNDER DEVELOPMENT
#######################################

# cankeep	
# This is the major function for the search/filter/display of the progams page
# Still under development
def get_program_display(request):
	print("GET PROGRAM DISPLAY")
	main_context = {} # to build out the specific html stuff
	search_context = {} # to build out the specific html stuff
	filter_context = {} # to build out the specific html stuff
	response_data = {} # to send back to the template

	key = 1
	program_info = {}

	working_filters = Q()
	working_filters.add(Q(publish=True),Q.AND)

	if 'program_tags' in request.POST.keys():
		working_tags = request.POST['program_tags'].split(',')
		main_context['searched_tags'] = request.POST['program_tags']

		for tag in working_tags:
			if str(tag).split("_")[0] == "tag":
				tmp = Tag.objects.all().filter(tag=str(tag).split("_")[1])
				working_filters.add(Q(tag__in=tmp),Q.AND)
			else:
				print("NAME", tag.split("_"))
				working_filters.add(Q(program=str(tag).split("_")[1]),Q.AND)

	if 'filter_tags[]' in request.POST.keys():
		filter_tags = request.POST.getlist('filter_tags[]')
		working_filters.add(Q(tag__in=filter_tags),Q.AND)
		


	working_program = Program.objects.all().filter(working_filters).distinct().order_by('ordering')

	for program in working_program:
		program_list = {}
		program_list = {
			"program": program,
			# "heatmap": get_program_heatmap(request=request,program=program)
		}

		program_info[key] = program_list
		key = key + 1

	program_info = tuple(program_info.items())
	main_context['program_info'] = program_info
	main_context['number_of_programs'] = working_program.count()


	#These are for the search bar
	search_context['program_names'] = Program.objects.all().filter(publish=True)
	search_context['working_tags'] = Tag.objects.all().filter(program__in=Program.objects.all().filter(publish=True)).distinct()
	filter_context['working_tags'] = Tag.objects.all().filter(program__in=Program.objects.all().filter(publish=True)).distinct()


	response_data["program_filters"] = render_to_string('SS_program_filters.html', filter_context, request=request)
	response_data["program_search"] = render_to_string('SS_program_search.html', search_context, request=request)
	response_data["program_display"] = render_to_string('SS_program_display.html', main_context, request=request)
	
	# else
	return HttpResponse(json.dumps(response_data),content_type="application/json")	

# caneval - I don't know the best place for this, even if it is needed
# This is to save beta feedback


# canevaluate
def create_program(request, id=None):
	context={}
	return render(request,"SS_create_program.html",context)

# canevaluate
def get_create_program(request):
	main_context = {} # to build out the specific html stuff
	response_data = {} # to send back to the template

	main_context['working_tags'] =  Tag.objects.all()

	if 'id' in request.POST.keys():
		print("ID HERE", request.POST['id'])
		if request.POST['id'] != None:
			if request.POST['id'] != '':
				main_context['editing_program'] = Program.objects.all().filter(user=request.user).get(id=int(request.POST['id']))


				tmp_tags = Program.objects.all().filter(user=request.user).get(id=int(request.POST['id'])).tag

				tags = []
				for tag in tmp_tags.all():
					tags.append(tag.tag)

				main_context['tags'] = tags
			

	main_context['working_program'] = Program.objects.all()
	main_context['all_possible_texts'] = PossibleText.objects.all().filter(user=request.user).exclude(text__exact='')

	response_data["program"] = render_to_string('SS_create_program_content.html', main_context, request=request)
	
	# else
	return HttpResponse(json.dumps(response_data),content_type="application/json")		






	# response_data['save_message'] = ".csv downloaded!"
	

	# return HttpResponse(json.dumps(response_data),content_type="application/json")



# This is to just initialize the main text input box
# caneval - fix the template so it doesn't need the 'timing summary, but can just work off of the working timing'
# also, I'm feeling that there will be another function to get the edicing one, so work out these too things
# change to "get_new_text"
def get_text_input(request):
	main_context = {} 
	response_data = {}
	main_context['text_message'] = "New Text"
	# main_context['today_date'] = datetime.now()
	today = datetime.today()
	main_context['today_date'] = str(str(today.strftime('%d'))  + " " + str(today.strftime('%B')) + ", " + str(today.year))
	if request.user.is_authenticated():	
		working_timing = get_timing_default(request)
		main_context['timing_summary'] = working_timing.timing_summary
		main_context['working_timing'] = working_timing
		main_context['text_message'] = request.POST['text_message']

	response_data["text_input"] = render_to_string('SS_new_text.html', main_context, request=request)
	return HttpResponse(json.dumps(response_data),content_type="application/json")

#for some reason this is how to get the edit thing
# change to "get_edit_text"
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

#This will show the timing optiosn.  You should change the name because it is confusing.
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


# This is just the fuction that saves the timing because there is so much stuff in it
# It isn't called directly from templates or anything
def save_timing_function(request,working_timing):
	# SAVE THE VALUES
	if 'date_start' in request.POST.keys():
		working_timing.date_start = datetime.strptime(request.POST['date_start'], '%d %B, %Y')
		working_timing.date_start_value = request.POST['date_start']
	# else:

	# 	datetime.strptime(request.POST['date_start'], '%d %B, %Y')
	# 	working_timing.date_start_value = request.POST['date_start']

	if 'date_end' in request.POST.keys():
		print("DATE END", request.POST['date_end'])
		if request.POST['date_end'] != '':
			working_timing.date_end = datetime.strptime(request.POST['date_end'], '%d %B, %Y')
			working_timing.date_end_value = request.POST['date_end']

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

	#figure out which text it belongs with
	if 'id' in request.POST.keys():
		if request.POST['id'] != "None" and request.POST['id'] != "" and request.POST['id'] is not None:
			working_text = PossibleText.objects.all().filter(user=request.user).get(id=int(request.POST['id']))
		else:
			working_text = PossibleText(user=request.user,date_created=datetime.now(pytz.utc))
	else:
		working_text = PossibleText(user=request.user,date_created=datetime.now(pytz.utc))
	working_text.save()

	#deal with the alt texts
	if 'alt_texts[]' in request.POST.keys():
		alt_ids = request.POST.getlist('alt_texts_ids[]')
		alt_texts = request.POST.getlist('alt_texts[]')

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

	# I'm pretty sure that this conditional doesn't apply
	# caneval - remove this save_time and thigns.  
	if request.POST['save_type'] == 'options_text_save':
		working_text.tmp_save = False
		working_text.save()
		working_timing = get_timing_default(request)
		main_context['working_timing'] = working_timing

	else:
		working_text.tmp_save = True
		working_text.save()
		main_context['working_text'] = working_text
		main_context['id'] = working_text.id
		main_context['working_timing'] = working_text.timing
	
	main_context['text_message'] = "New Text"
	response_data["text_input"] = render_to_string('SS_new_text.html', main_context, request=request)
	return HttpResponse(json.dumps(response_data),content_type="application/json")	

# Save the text
def save_text(request):
	print("SAVE TEXT HERE HERE")
	main_context = {} 
	response_data = {}

	#Get the text or create new
	if 'id' in request.POST.keys():
		if request.POST['id'] != "None" and request.POST['id'] != "":
			working_text = PossibleText.objects.all().filter(user=request.user).get(id=int(request.POST['id']))
		else:
			working_text = PossibleText(user=request.user,date_created=datetime.now(pytz.utc))
	else:
		working_text = PossibleText(user=request.user,date_created=datetime.now(pytz.utc))

	working_text.text=request.POST['text_content']

	#See if there is a timing associated with it, if not assign the default
	if working_text.timing == None:
		working_timing = get_timing_default(request)
		working_text.timing = working_timing

	working_text.tmp_save = False
	working_text.save()


	# Remove any unsent but scheduled texts and reset the schedule tracker
	if 'id' in request.POST.keys():
		if request.POST['id'] != "None" and request.POST['id'] != "":
			#clear out the actual texts so it gets rescheduled
			unsent_texts = ActualText.objects.all().filter(user=request.user).filter(text=working_text).filter(time_sent__isnull=True)
			for text in unsent_texts:
				text.delete()

			#The time scheduled might have to be reset in the possibletext 	
			working_text.date_scheduled = None
			working_text.save()

	if 'text_message' in request.POST.keys():
		main_context['text_message'] = request.POST['text_message']
	else:
		main_context['text_message'] = "New Text"

	main_context['working_timing'] = get_timing_default(request)
	response_data["text_input"] = render_to_string('SS_new_text.html', main_context, request=request)

	return HttpResponse(json.dumps(response_data),content_type="application/json")

# This sets the default timing
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



# This is fine, but doesn't have to live here
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
	response_data = {} # to send back to the template
	# if request.user.is_superuser:
	print("SUUUUUUUUNNNNNNN")
	date_now = str(datetime.now(pytz.utc).strftime('%-m/%-d/%Y'))
	distinct_users = PossibleText.objects.all().filter(tmp_save=False).filter(active=True).filter(text_type="sun").values('user').distinct()

	for user in distinct_users:
		working_settings = UserSetting.objects.all().get(user=user['user'])
		user_timezone = pytz.timezone(working_settings.timezone)
		user_location = working_settings.city_state()

		print("date_now", date_now)
		print("user_location", user_location)

		dataj = "NONE" 

		#Get the sun data
		working_texts = PossibleText.objects.all().filter(user=working_settings.user).filter(tmp_save=False).filter(active=True).filter(text_type="sun")
		for text in working_texts:
			if ActualText.objects.all().filter(user=text.user).filter(text=text).filter(time_sent__isnull=True).filter(time_to_send__gte=pytz.utc.localize(datetime.now())).count() < 1:
				if dataj == "NONE":
					data = requests.get(str('http://api.usno.navy.mil/rstt/oneday?date='+ date_now +'&loc=' + user_location))
					dataj = data.json()

				if 'Sun Rise' in text.text:
					text_to_send = 'The sun is rising right now!'
					time_out = get_sun_time(dataj['sundata'],'R')
				elif 'Sun Set' in text.text: 
					text_to_send = 'The sun is setting right now!'
					time_out = get_sun_time(dataj['sundata'],'S')
				elif 'Solar Noon' in text.text:
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

				print("time_to_send",time_to_send)
				print("datetime.now(pytz.utc)",datetime.now(pytz.utc))

				if datetime.now(pytz.utc) < time_to_send:
					atext = ActualText(user=text.user,text=text,time_to_send=time_to_send,text_sent=text_to_send)
					atext.save()

	print("MOOOOOOOOON")
	date_now = str(datetime.now(pytz.utc).strftime('%-m/%-d/%Y'))
	dataj = "NONE" 
	
	data = requests.get(str('http://api.usno.navy.mil/moon/phase?date='+date_now+'&nump=4'))
	dataj = data.json()
	# print("dataj", dataj)
	
	next_phase = dataj['phasedata'][0]
	moon_dt = datetime.strptime(str(dataj['phasedata'][0]['date'])+' '+dataj['phasedata'][0]['time'], '%Y %b %d %H:%M')
	moon_dt_utc = pytz.utc.localize(moon_dt)

	working_texts = PossibleText.objects.all().filter(tmp_save=False).filter(active=True).filter(text_type="moon")
	for text in working_texts:
		if str(next_phase['phase']) in str(text.text):
			working_settings = UserSetting.objects.all().get(user=text.user)
			user_timezone = pytz.timezone(working_settings.timezone)
			moon_dt_user = moon_dt_utc.astimezone(user_timezone)

			# #See if there is a text scheduled in the future for this phase.  if not, then schedule it.
			if ActualText.objects.all().filter(user=text.user).filter(text=text).filter(time_sent__isnull=True).filter(time_to_send__gte=pytz.utc.localize(datetime.now())).count() < 1:
				date_today = datetime.now(pytz.utc).astimezone(user_timezone)
				time_window = user_timezone.localize(datetime.combine(date_today, text.timing.hour_end)) - user_timezone.localize(datetime.combine(date_today, text.timing.hour_start))

				moon_dt_user = moon_dt_user - timedelta(1,0)
				scheduled_date = user_timezone.localize(datetime.combine(moon_dt_user.date(), text.timing.hour_start))
				scheduled_date = scheduled_date.astimezone(pytz.UTC)

				time_to_send = scheduled_date + timedelta(0,randint(0,round(time_window.total_seconds())))
				text_to_send = "The " + dataj['phasedata'][0]['phase'] + " will happen at "  + str(moon_dt_user.strftime('%-I:%M %p')) + " on " + str(moon_dt_user.strftime(' %B %d, %Y')) + "!"

				atext = ActualText(user=text.user,text=text,time_to_send=time_to_send,text_sent=text_to_send)
				atext.save()
					
	
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

