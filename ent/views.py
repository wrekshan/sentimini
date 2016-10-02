from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from datetime import datetime, timedelta, time
from django.forms import modelformset_factory
import pytz
from random import random, triangular, randint
from django.db.models import Avg, Count, F, Case, When
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from time import strptime
# Create your views here.
from .forms import  UserSettingForm_Prompt, PossibleTextSTMForm, UserSettingForm_PromptRate, ExampleFormSetHelper, EmotionOntologyForm, EmotionOntologyFormSetHelper, UserGenPromptFixedForm, UserGenPromptFixedFormSetHelper, TimingForm, PossibleTextSTMForm_detail, NewUserForm, NewUser_PossibleTextSTMForm
from .models import PossibleTextSTM, ActualTextSTM, UserSetting, Carrier, Respite, Ontology, UserGenPromptFixed, PossibleTextLTM, ExperienceSetting

from sentimini.sentimini_functions import  get_graph_data_simulated, get_graph_data_simulated_heatmap, get_graph_data_histogram_timing
from sentimini.scheduler_functions import generate_random_prompts_to_show, next_prompt_minutes, determine_next_prompt_series, next_response_minutes

from sentimini.tasks import send_texts, schedule_texts, set_next_prompt, determine_prompt_texts, set_prompt_time, check_email_for_new, process_new_mail, actual_text_consolidate, check_for_nonresponse

def new_user(request):
	if request.user.is_authenticated():	
		if  UserSetting.objects.filter(user=request.user).exists():
			working_settings = UserSetting.objects.all().get(user=request.user)
		else: 
			working_settings = UserSetting(user=request.user,begin_date=datetime.now(pytz.utc)).save()
			working_settings = UserSetting.objects.all().get(user=request.user)

		if ExperienceSetting.objects.filter(user=request.user).filter(experience='user').exists():
			working_experience = ExperienceSetting.objects.all().filter(experience='user').get(user=request.user)
		else: 
			working_experience = ExperienceSetting(user=request.user,experience='user').save()
			working_experience = ExperienceSetting.objects.all().filter(experience='user').get(user=request.user)

		if ExperienceSetting.objects.filter(user=request.user).filter(experience='research').exists():
			working_research = ExperienceSetting.objects.all().filter(experience='research').get(user=request.user)
		else:
			tmp = ExperienceSetting(user=request.user,experience='research',prompts_per_week=1)
			tmp.save()

			working_research = ExperienceSetting.objects.all().filter(experience='research').get(user=request.user)
			min_awake = (24 - working_settings.sleep_duration)*60
			working_research.prompt_interval_minute_avg = ((24 - working_settings.sleep_duration)*60) / (working_research.prompts_per_week/7) #used in the random draw for the number of minutes to next prompt
			working_research.prompt_interval_minute_min =  working_research.prompt_interval_minute_avg*.5
			working_research.prompt_interval_minute_max =  working_research.prompt_interval_minute_avg*4
			working_research.save()

		form_new_text = NewUser_PossibleTextSTMForm(request.POST or None)
		form_new_user = NewUserForm(request.POST or None, instance=working_settings)
		form_prompt_percent = UserSettingForm_PromptRate(request.POST or None, instance=working_research)
		
		
		prompts_per_week = working_settings.prompts_per_week
		number_of_texts = PossibleTextSTM.objects.all().filter(user=request.user).filter(text_type='user').count

		if working_settings.new_user_pages < 2:
			graph_data_simulated_heatmap = 0
		else:
			generate_random_prompts_to_show(request,exp_resp_rate=.6,week=0,number_of_prompts=20) #set up 20 random prompts based upon the settings
			graph_data_simulated_heatmap = get_graph_data_simulated_heatmap(request,simulated_val=1)

		########## NOW THE FORM HANDLING STUFF
		if request.method == "POST":
			print("REQUEST POST")
			print("REQUEST POST STUFF", request.POST)
			
			if 'submit_new_text' or 'submit_finished_adding' in request.POST:
				if form_new_text.is_valid():	
					tmp = form_new_text.save()
					tmp.user=request.user
					if tmp.date_created is None:
						tmp.date_created = datetime.now(pytz.utc)
						tmp.save()
					
					#Save any changes in long term storage
					ptltm = PossibleTextLTM(user=request.user,stm_id=tmp.id,text=tmp.text,text_type=tmp.text_type,text_importance=tmp.text_importance,response_type=tmp.response_type,show_user=tmp.show_user,date_created=tmp.date_created,date_altered=datetime.now(pytz.utc))
					ptltm.save()

					if 'submit_new_text'in request.POST:
						return HttpResponseRedirect('/ent/new_user/')

					else:
						if working_settings.new_user_pages== 1:
							working_settings.new_user_pages = 2
							working_settings.save()
							return HttpResponseRedirect('/ent/new_user/')

			if 'submit_new_user' in request.POST:
				print("new_user")
				if form_new_user.is_valid():
					print("form valid")

					form_new_user.save()
					tmp_settings = form_new_user.save(commit=False)
					working_experience.prompts_per_week = tmp_settings.prompts_per_week
					min_awake = (24 - tmp_settings.sleep_duration)*60
					working_experience.prompt_interval_minute_avg = ((24 - tmp_settings.sleep_duration)*60) / (working_experience.prompts_per_week/7) #used in the random draw for the number of minutes to next prompt
					working_experience.prompt_interval_minute_min =  working_experience.prompt_interval_minute_avg*.5
					working_experience.prompt_interval_minute_max =  working_experience.prompt_interval_minute_avg*4
					working_experience.save()
					tmp_settings.save()

					if tmp_settings.phone_input != "":
						print("LENGTH ONLY", len(str(get_num(tmp_settings.phone_input))))
						print("NUMBER ONLY", get_num(tmp_settings.phone_input))

						if len(str(get_num(tmp_settings.phone_input))) == 10:
							tmp_settings.phone = str(get_num(tmp_settings.phone_input))
							tmp_settings.send_text = bool(True)	#just a switch to say the person can be texted
							tmp_settings.sms_address =  tmp_settings.phone_input + str(carrier_lookup(tmp_settings.carrier)) #Figures otu the address the promtps need to be sent to
							tmp_settings.respite_until_datetime = datetime.now(pytz.utc) #initializes the respite until date (this actually just needs to be set because it does a greater than check)

							if working_settings.new_user_pages< 1:
								working_settings.new_user_pages = 1
								working_settings.save()

							tmp_settings.save()
						else:
							messages.add_message(request, messages.INFO, 'Not 10 Expecting a 10 digit US number')
					
					return HttpResponseRedirect('/ent/new_user/')		

			if 'submit_prompt_percent' in request.POST:
				if form_prompt_percent.is_valid():
					tmp_settings = form_prompt_percent.save(commit=False)
					working_research.prompts_per_week = tmp_settings.prompts_per_week

					min_awake = (24 - working_experience.sleep_duration)*60
					working_research.prompt_interval_minute_avg = ((24 - working_experience.sleep_duration)*60) / (working_research.prompts_per_week/7) #used in the random draw for the number of minutes to next prompt
					working_research.prompt_interval_minute_min =  working_research.prompt_interval_minute_avg*.5
					working_research.prompt_interval_minute_max =  working_research.prompt_interval_minute_avg*4
					
					tmp_settings.save()
					return HttpResponseRedirect('/ent/edit_prompt_settings/#paid')		
			return HttpResponseRedirect('/ent/new_user/')
				
		else:
			form_new_user = NewUserForm(request.POST or None, instance=working_settings)
			form_prompt_percent = UserSettingForm_PromptRate(request.POST or None, instance=working_research)
			form_new_text = NewUser_PossibleTextSTMForm(request.POST or None)

			

			context = {
				"prompts_per_week": prompts_per_week,
				"number_of_texts": number_of_texts,
				"form_new_text": form_new_text,
				"graph_data_simulated_heatmap": graph_data_simulated_heatmap,

				
				"form_new_user": form_new_user,
				"form_prompt_percent": form_prompt_percent,
			}
			if working_settings.new_user_pages == 0:
				return render(request, "new_user_page1.html", context)
			elif working_settings.new_user_pages == 1:
				return render(request, "new_user_page2.html", context)
			else:
				return render(request, "new_user_page3.html", context)
	else:
		return render(request, "index_not_logged_in.html")


def texter(request):
	if request.user.is_authenticated():	

		#Create the Text
		if request.GET.get('create_unsent_text'):
			print("Creating Unsent Texts")
			text_new = ActualTextSTM(user=request.user, response=None,simulated=0,text_type="user")
			text_new.text, text_new.text_id = set_next_prompt(user=text_new.user,text_type="user")
			text_new.text, text_new.response_type = determine_prompt_texts(user=request.user,prompt=text_new.text,typer=text_new.text_type)
			text_new.time_to_send = set_prompt_time(text=text_new,send_now=1)
			text_new.save()
			
			return HttpResponseRedirect('/ent/texter/')
			
		# Send the text	
		if request.GET.get('check_for_unsent'):
			print("button pressed . sending texts")
			send_texts()
			return HttpResponseRedirect('/ent/texter/')

		if request.GET.get('schedule'):
			print("SCHEDULE")
			schedule_texts()
			return HttpResponseRedirect('/ent/texter/')

		if request.GET.get('check_email_for_new'):
			print("check_email_for_new")
			check_email_for_new()
			return HttpResponseRedirect('/ent/texter/')

		if request.GET.get('process_new_mail'):
			print("process_new_mail")
			process_new_mail()
			return HttpResponseRedirect('/ent/texter/')

		if request.GET.get('actual_text_consolidate'):
			print("actual_text_consolidate")
			actual_text_consolidate()
			return HttpResponseRedirect('/ent/texter/')

		if request.GET.get('check_for_nonresponse'):
			print("check_for_nonresponse")
			check_for_nonresponse()
			return HttpResponseRedirect('/ent/texter/')					

			
	
		
		context = {
			
		}			

		return render(request,"texter.html",context)
	else:
		return HttpResponseRedirect('/accounts/signup/')



def get_num(x):
    return int(''.join(ele for ele in x if ele.isdigit()))

def get_digits(text):
    return filter(str.isdigit, text)

#User settings
def edit_prompt_settings(request):
	if request.user.is_authenticated():	
		if  UserSetting.objects.filter(user=request.user).exists():
			working_settings = UserSetting.objects.all().get(user=request.user)
		else: 
			working_settings = UserSetting(user=request.user,begin_date=datetime.now(pytz.utc)).save()
			working_settings = UserSetting.objects.all().get(user=request.user)

		if ExperienceSetting.objects.filter(user=request.user).filter(experience='user').exists():
			working_experience = ExperienceSetting.objects.all().filter(experience='user').get(user=request.user)
		else: 
			working_experience = ExperienceSetting(user=request.user,experience='user').save()
			working_experience = ExperienceSetting.objects.all().filter(experience='user').get(user=request.user)

		if ExperienceSetting.objects.filter(user=request.user).filter(experience='research').exists():
			working_research = ExperienceSetting.objects.all().filter(experience='research').get(user=request.user)
		else:
			tmp = ExperienceSetting(user=request.user,experience='research',prompts_per_week=1)
			tmp.save()

			working_research = ExperienceSetting.objects.all().filter(experience='research').get(user=request.user)
			min_awake = (24 - working_settings.sleep_duration)*60
			working_research.prompt_interval_minute_avg = ((24 - working_settings.sleep_duration)*60) / (working_research.prompts_per_week/7) #used in the random draw for the number of minutes to next prompt
			working_research.prompt_interval_minute_min =  working_research.prompt_interval_minute_avg*.5
			working_research.prompt_interval_minute_max =  working_research.prompt_interval_minute_avg*4
			working_research.save()

		#UGPR
		if PossibleTextSTM.objects.filter(user=request.user).filter(text_type="user").count()>0:
			working_user_gen = PossibleTextSTM.objects.all().filter(user=request.user).filter(show_user=False).filter(text_type="user")
		else:
			PossibleTextSTM(user=request.user,text='How are you doing?',text_importance=1, date_created = datetime.now(pytz.utc),response_type = '0 to 10').save()
			working_user_gen = PossibleTextSTM.objects.all().filter(user=request.user).filter(show_user=False).filter(text_type="user")


		############ SET UP THE FORMS
		#UGPR
		if PossibleTextSTM.objects.filter(user=request.user).count()==1:
			UGPFormset = modelformset_factory(PossibleTextSTM, form = PossibleTextSTMForm, extra=1)
			formset = UGPFormset(queryset = working_user_gen)
		else:
			UGPFormset = modelformset_factory(PossibleTextSTM, form = PossibleTextSTMForm, extra=0)
			formset = UGPFormset()

		helper = ExampleFormSetHelper()
		form_free = UserSettingForm_Prompt(request.POST or None, instance=working_settings)
		form_sleep = TimingForm(request.POST or None, instance=working_settings)
		form_prompt_percent = UserSettingForm_PromptRate(request.POST or None, instance=working_research)
		
		generate_random_prompts_to_show(request,exp_resp_rate=.6,week=0,number_of_prompts=20) #set up 20 random prompts based upon the settings
		graph_data_simulated_heatmap = get_graph_data_simulated_heatmap(request,simulated_val=1)
		graph_data_histogram_timing = get_graph_data_histogram_timing(request,simulated_val=1)
		prompts_per_week = working_settings.prompts_per_week

		########## NOW THE FORM HANDLING STUFF
		if request.method == "POST":
			if PossibleTextSTM.objects.filter(user=request.user).count()==1:
				formset = UGPFormset(request.POST)
			else:
				formset = UGPFormset(request.POST, queryset = working_user_gen )

			if 'submit_formset' in request.POST:
				if formset.is_valid: 
					for form in formset:
						if form.is_valid() and form.has_changed():	
							tmp = form.save()
							if tmp.date_created is None:
								tmp.date_created = datetime.now(pytz.utc)
								tmp.save()
							
							#Save any changes in long term storage
							ptltm = PossibleTextLTM(user=request.user,stm_id=tmp.id,text=tmp.text,text_type=tmp.text_type,text_importance=tmp.text_importance,response_type=tmp.response_type,show_user=tmp.show_user,date_created=tmp.date_created,date_altered=datetime.now(pytz.utc))
							ptltm.save()
				return HttpResponseRedirect('/ent/edit_prompt_settings/#create_your_own_texts')

			elif 'submit_timing' in request.POST:
				if form_sleep.is_valid():
					form_sleep.save()
					tmp_settings = form_sleep.save(commit=False)
					working_experience.prompts_per_week = tmp_settings.prompts_per_week
					min_awake = (24 - tmp_settings.sleep_duration)*60
					working_experience.prompt_interval_minute_avg = ((24 - tmp_settings.sleep_duration)*60) / (working_experience.prompts_per_week/7) #used in the random draw for the number of minutes to next prompt
					working_experience.prompt_interval_minute_min =  working_experience.prompt_interval_minute_avg*.5
					working_experience.prompt_interval_minute_max =  working_experience.prompt_interval_minute_avg*4
					working_experience.save()
					tmp_settings.save()
					
					return HttpResponseRedirect('/ent/edit_prompt_settings/#timing')		

			elif 'submit_contact' in request.POST:
				if form_free.is_valid():
					tmp_settings = form_free.save(commit=False)
					print("Contact Valid")

					if tmp_settings.phone_input != "":
						print("LENGTH ONLY", len(str(get_num(tmp_settings.phone_input))))
						print("NUMBER ONLY", get_num(tmp_settings.phone_input))

						if len(str(get_num(tmp_settings.phone_input))) == 10:
							tmp_settings.phone = str(get_num(tmp_settings.phone_input))
							tmp_settings.send_text = bool(True)	#just a switch to say the person can be texted
							tmp_settings.sms_address =  tmp_settings.phone_input + str(carrier_lookup(tmp_settings.carrier)) #Figures otu the address the promtps need to be sent to
							tmp_settings.respite_until_datetime = datetime.now(pytz.utc) #initializes the respite until date (this actually just needs to be set because it does a greater than check)
							tmp_settings.save()
						else:
							messages.add_message(request, messages.INFO, 'Not 10 Expecting a 10 digit US number')
					else:
						messages.add_message(request, messages.INFO, ' Nothing Expecting a 10 digit US number')
					return HttpResponseRedirect('/ent/edit_prompt_settings/#contact')		
				else:
					messages.add_message(request, messages.INFO, 'Not Valid')
					return HttpResponseRedirect('/ent/edit_prompt_settings/#contact')		

			elif 'submit_prompt_percent' in request.POST:
				if form_prompt_percent.is_valid():
					tmp_settings = form_prompt_percent.save(commit=False)
					working_research.prompts_per_week = tmp_settings.prompts_per_week

					min_awake = (24 - working_experience.sleep_duration)*60
					working_research.prompt_interval_minute_avg = ((24 - working_experience.sleep_duration)*60) / (working_research.prompts_per_week/7) #used in the random draw for the number of minutes to next prompt
					working_research.prompt_interval_minute_min =  working_research.prompt_interval_minute_avg*.5
					working_research.prompt_interval_minute_max =  working_research.prompt_interval_minute_avg*4
					
					tmp_settings.save()
					return HttpResponseRedirect('/ent/edit_prompt_settings/#paid')		
				
		else:
			form_free = UserSettingForm_Prompt(request.POST or None, instance=UserSetting.objects.all().get(user=request.user))
			form_sleep = TimingForm(request.POST or None, instance=working_settings)
			form_prompt_percent = UserSettingForm_PromptRate(request.POST or None, instance=working_research)

			if PossibleTextSTM.objects.filter(user=request.user).filter(text_type="user").count()==1 and PossibleTextSTM.objects.filter(user=request.user).filter(text_type="user").first().prompt == '':
				print("EQUAL TO ONE")
				UGPFormset = modelformset_factory(PossibleTextSTM, form = PossibleTextSTMForm, extra=0)
				formset = UGPFormset()
			else:
				print("NOT ONE")
				UGPFormset = modelformset_factory(PossibleTextSTM, form = PossibleTextSTMForm, extra=1)
				formset = UGPFormset(queryset = working_user_gen)
				
			helper = ExampleFormSetHelper()

			context = {
				"prompts_per_week": prompts_per_week,

				"helper": helper,
				"form_sleep": form_sleep,
				"form_free": form_free,
				"form_prompt_percent": form_prompt_percent,
				"formset": formset,

				"graph_data_simulated_heatmap": graph_data_simulated_heatmap,
				"graph_data_histogram_timing": graph_data_histogram_timing,
			}
			return render(request, "settings_prompts.html", context)
	else:
		return render(request, "index_not_logged_in.html")


##########################################################
##### HERE ARE THINGS YOU HAVE TO HAVE
##########################################################
#This creates a entry for the settings file for the people.  Right now it just displays the things a user would want to change.  I've tried to add in some adaptive flexibility, but right now it is just a place holder
def carrier_lookup(carrier):
	return Carrier.objects.all().get(carrier=carrier).sms_address

def respite_one_day(request):
	working_settings = UserSetting.objects.all().get(user=request.user)
	today_date = datetime.now(pytz.utc)
	working_settings.respite_until_datetime = today_date + timedelta(1,0)
	working_settings.save()

	Respite(user=request.user,respite_type='1 day',date_request=today_date).save()
	messages.add_message(request, messages.INFO, 'No prompts will be sent for 1 day')
	return redirect(request.META['HTTP_REFERER'])

def respite_three_day(request):
	working_settings = UserSetting.objects.all().get(user=request.user)
	today_date = datetime.now(pytz.utc)
	working_settings.respite_until_datetime = today_date + timedelta(3,0)
	working_settings.save()

	Respite(user=request.user,respite_type='3 day',date_request=today_date).save()
	messages.add_message(request, messages.INFO, 'No prompts will be sent for 3 days')
	return redirect(request.META['HTTP_REFERER'])

def respite_seven_day(request):
	working_settings = UserSetting.objects.all().get(user=request.user)
	today_date = datetime.now(pytz.utc)
	working_settings.respite_until_datetime = today_date + timedelta(7,0)
	working_settings.save()

	Respite(user=request.user,respite_type='7 day',date_request=today_date).save()
	messages.add_message(request, messages.INFO, 'No prompts will be sent for 7 days')
	return redirect(request.META['HTTP_REFERER'])

def respite_start_again(request):
	working_settings = UserSetting.objects.all().get(user=request.user)
	today_date = datetime.now(pytz.utc)
	working_settings.respite_until_datetime = today_date  
	tmp_msg = "Starting again"
	
	working_settings.text_request_stop = False
	working_settings.save()
	Respite(user=request.user,respite_type='start_again',date_request=today_date).save()
	messages.add_message(request, messages.INFO, 'Starting prompts again')
	return redirect(request.META['HTTP_REFERER'])
