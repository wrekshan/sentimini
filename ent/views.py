from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from datetime import datetime, timedelta, time, date
from django.forms import modelformset_factory
import pytz
from random import random, triangular, randint
from django.db.models import Avg, Count, F, Case, When
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from time import strptime
# Create your views here.
from .forms import  UserSettingForm_Prompt, PossibleTextSTMForm, UserSettingForm_ResearchPercent, ExampleFormSetHelper, EmotionOntologyForm, EmotionOntologyFormSetHelper, UserGenPromptFixedForm, UserGenPromptFixedFormSetHelper, TimingForm, PossibleTextSTMForm_detail, NewUserForm, NewUser_PossibleTextSTMForm, AddNewTextSetForm, AddNewTextSetForm_full, AddNewTextSetForm_fullFormSetHelper, TextSetFormSetHelper, ExperienceTimingForm, UserSettingForm_PromptRate
from .models import PossibleTextSTM, ActualTextSTM, UserSetting, Carrier, Respite, Ontology, UserGenPromptFixed, PossibleTextLTM, ExperienceSetting, ActualTextSTM_SIM

from sentimini.sentimini_functions import  get_graph_data_simulated, get_graph_data_simulated_heatmap, get_graph_data_histogram_timing
from sentimini.scheduler_functions import generate_random_prompts_to_show, next_prompt_minutes, determine_next_prompt_series, next_response_minutes, figure_out_timing

from sentimini.tasks import send_texts, schedule_texts, set_next_prompt, determine_prompt_texts, set_prompt_time, check_email_for_new, process_new_mail, actual_text_consolidate, check_for_nonresponse, generate_random_minutes


def update_experiences(user):
	working_experience = ExperienceSetting.objects.all().filter(user=user)

	for exp in working_experience:
		exp.number_of_texts_in_set = PossibleTextSTM.objects.all().filter(user=user).filter(text_type=exp.experience).filter(text_set=exp.text_set).count()
		#figure out timing
		exp.prompt_interval_minute_avg, exp.prompt_interval_minute_min, exp.prompt_interval_minute_max = figure_out_timing(user=user,text_per_week=exp.prompts_per_week)
		exp.save()

def create_new_user_experience(user,ideal_id):
	if ideal_id == "Create New":
		ExperienceSetting(user=user,experience='user',text_set="New Set",user_state="disable").save()
		working_experience = ExperienceSetting.objects.all().filter(user=user).filter(experience="user").get(text_set="New Set")
		working_experience.ideal_id = working_experience.id
		working_experience.description = working_experience.description
		working_experience.unique_text_set = working_experience.unique_text_set
		ideal_id = working_experience.id
		working_experience.save()

	if ExperienceSetting.objects.filter(user=user).filter(experience='user').filter(ideal_id=ideal_id).count()<1:
		library_tmp = ExperienceSetting.objects.all().filter(experience='library').get(ideal_id=ideal_id)
		ExperienceSetting(user=user,experience='user',ideal_id=ideal_id,description=library_tmp.description,text_set=library_tmp.text_set,user_state="disable").save()
		working_experience = ExperienceSetting.objects.all().filter(user=user).filter(experience="user").get(ideal_id=ideal_id)

		#INITIALIZE TEXTS
		if PossibleTextSTM.objects.all().filter(text_type="library").filter(experience_id=ideal_id).count() > 0 :
			tmp_texts = PossibleTextSTM.objects.all().filter(text_type="library").filter(experience_id=ideal_id,text_set=working_experience.text_set)

			for text in tmp_texts:
				tmp_new = PossibleTextSTM(user=user,text=text.text,response_type=text.response_type,experience_id=text.experience_id,text_set=text.text_set,text_type="user",text_importance=text.text_importance,date_created=text.date_created)
				tmp_new.save()

		# You have to add in the texts


def feeds_edit(request):
	if request.user.is_authenticated():	
		#Create new user generated list if none
		if ExperienceSetting.objects.filter(user=request.user).filter(experience='user').filter(text_set="user generated").count()<1:
			ideal_exp = ExperienceSetting.objects.filter(experience='library').get(text_set="user generated")
			create_new_user_experience(user=request.user,ideal_id=ideal_exp.id) #FIX THIS

		#Update the tables with the right numbers of texts
		if ExperienceSetting.objects.all().filter(user=request.user).count()>0:
			update_experiences(user=request.user)
		

		number_of_experiences = ExperienceSetting.objects.all().filter(experience='user').filter(user=request.user).count()
		working_experience_sets = ExperienceSetting.objects.all().filter(experience='user').filter(user=request.user)
		library_experiences = ExperienceSetting.objects.all().filter(experience='library')
		number_of_texts = PossibleTextSTM.objects.all().filter(user=request.user).count()

		#Remove the experiences that have been signed up for
		number_of_texts_per_week = 0
		for exp in working_experience_sets:
			number_of_texts_per_week = number_of_texts_per_week + exp.prompts_per_week
			if library_experiences.filter(ideal_id=exp.ideal_id).count() > 0:
				tmp_remove = library_experiences.filter(experience="library").get(ideal_id=exp.ideal_id)
				library_experiences = library_experiences.exclude(id=tmp_remove.id)


		if request.GET.get('create_new_feed'):
			create_new_user_experience(user=request.user,ideal_id="Create New")
			ideal_experience = ExperienceSetting.objects.all().filter(user=request.user).filter(experience="user").get(text_set="New Set")
			
			return HttpResponseRedirect('/ent/text_set_detail/'+str(ideal_experience.id))				

	
		context = {
			"number_of_texts": number_of_texts,
			"number_of_texts_per_week": number_of_texts_per_week,
			"number_of_experiences": number_of_experiences,
			"working_experience_sets": working_experience_sets,
			"library_experiences": library_experiences,
		}

		return render(request, "feeds_edit.html", context)
	else:
		return HttpResponseRedirect('/accounts/signup/')

def text_set_detail(request,id=None):
	if request.user.is_authenticated():
		if ExperienceSetting.objects.all().filter(id=id).count()<1:
			return HttpResponseRedirect('/ent/feeds_edit/')
		else:
			ideal_experience = ExperienceSetting.objects.all().get(id=id)

			if ExperienceSetting.objects.all().filter(user=request.user).filter(experience='user').filter(ideal_id=id).count()<1:
				working_user_gen = PossibleTextSTM.objects.all().filter(show_user=False).filter(text_type="library").filter(experience_id=id)
				text_for_user = "This experience is NOT enabled"
				working_experience = ExperienceSetting.objects.all().get(id=id)
				number_of_experiences = 0
			else:
				working_user_gen = PossibleTextSTM.objects.all().filter(user=request.user).filter(show_user=False).filter(text_type="user").filter(experience_id=id)
				text_for_user = "This experience is enabled"
				working_experience = ExperienceSetting.objects.all().filter(user=request.user).filter(experience='user').get(ideal_id=id)
				number_of_experiences = ExperienceSetting.objects.all().filter(user=request.user).filter(experience='user').filter(ideal_id=id).count()
				
			helper = TextSetFormSetHelper()
			UGPFormset = modelformset_factory(PossibleTextSTM, form = PossibleTextSTMForm, extra=1)
			formset = UGPFormset(queryset = working_user_gen)
			form_text_set_new= AddNewTextSetForm_full(request.POST or None, instance = working_experience)
			
			number_of_texts = working_user_gen.count()
			text_per_week = working_experience.prompts_per_week

			if request.GET.get('remove_experience'):
				working_user_gen = PossibleTextSTM.objects.all().filter(user=request.user).filter(show_user=False).filter(text_type="user").filter(experience_id=id)
				text_for_user = "This experience is enabled"
				working_experience = ExperienceSetting.objects.all().filter(user=request.user).filter(experience='user').get(ideal_id=id)
				number_of_experiences = ExperienceSetting.objects.all().filter(user=request.user).filter(experience='user').filter(ideal_id=id).count()

				user_experience = ExperienceSetting.objects.all().filter(experience="user").filter(ideal_id=id)
				user_texts = PossibleTextSTM.objects.all().filter(user=request.user).filter(show_user=False).filter(text_type="user").filter(experience_id=id)
				user_outgoing = ActualTextSTM.objects.all().filter(user=request.user).filter(text_type="user").filter(experience_id=id).filter(time_sent__isnull=True)

				for exp in user_experience:
					exp.delete()

				for text in user_texts:
					text.delete()

				for text in user_outgoing:
					text.delete()
				
				return HttpResponseRedirect('/ent/feeds_edit/')

			if request.GET.get('enable_experience'):
				ideal_experience = ExperienceSetting.objects.all().get(id=id)
				print("ENABLE PRESSED")

				if ExperienceSetting.objects.all().filter(user=request.user).filter(experience='user').filter(ideal_id=id).count()<1:
					working_user_gen = PossibleTextSTM.objects.all().filter(show_user=False).filter(text_type="library").filter(experience_id=id)
					text_for_user = "This experience is NOT enabled"
					working_experience = ExperienceSetting.objects.all().get(id=id)
					number_of_experiences = 0
					
					# Create and save new one
					create_new_user_experience(user=request.user,ideal_id=working_experience.id)
					return HttpResponseRedirect('/ent/text_set_detail/'+str(ideal_experience.id))
			
				#Restore experience from defaul


			########## NOW THE FORM HANDLING STUFF
			if request.method == "POST":
				if 'submit_feed_description' in request.POST:
					if form_text_set_new.is_valid():
						# tmp_exp = ExperienceSetting.objects.all().filter(experience="user").get(ideal_id=ideal_experience.id)

						tmp = form_text_set_new.save(commit=False)
						tmp.prompts_per_week = tmp.prompts_per_week
						tmp.prompt_interval_minute_avg,tmp.prompt_interval_minute_min,tmp.prompt_interval_minute_max = figure_out_timing(user=request.user,text_per_week=tmp.prompts_per_week)
						tmp.save()	

					
						return HttpResponseRedirect('/ent/text_set_detail/'+str(ideal_experience.id))


				if 'submit_formset' in request.POST:
					formset = UGPFormset(request.POST, queryset = working_user_gen )
					if ExperienceSetting.objects.all().filter(user=request.user).filter(experience='user').filter(ideal_id=id).count()<1:
						#EXPERIENCE
						tmp_exp = ExperienceSetting(user=request.user,user_state="disable",ideal_id=ideal_experience.id,experience='user',description=working_experience.description,text_set=working_experience.text_set,prompts_per_week=ideal_experience.prompts_per_week)
						#gotta do the other stuff too
						tmp_exp.save()

						#INITIALIZE TEXTS
						tmp_texts = PossibleTextSTM.objects.all().filter(text_type="library").filter(experience_id=working_experience.id)

						for text in tmp_texts:
							print("NEW TEXT SAVED")
							tmp_new = PossibleTextSTM(user=request.user,text=text.text,response_type=text.response_type,experience_id=text.experience_id,text_set=text.text_set,text_type="user",text_importance=text.text_importance,date_created=text.date_created)
							tmp_new.save()


					if formset.is_valid(): 
						print("FORMSET VALID")
						if ExperienceSetting.objects.all().filter(user=request.user).filter(experience='user').filter(description=working_experience.description).filter(ideal_id=id).count()<0:
							tmp_exp = ExperienceSetting.objects.all().filter(user=request.user).filter(experience='user').filter(description=working_experience.description).filter(ideal_id=id)
						else:
							tmp_exp = ExperienceSetting.objects.all().get(id=ideal_experience.id)

						#Save the Experience
						for form in formset:

							if form.is_valid() and form.has_changed():
								tmp = form.save()

								tmp.user=request.user
								tmp.experience_id=tmp_exp.id
								tmp.text_set=tmp_exp.text_set
								tmp.text_type = 'user'

								if tmp.date_created is None:
									tmp.date_created = datetime.now(pytz.utc)
								tmp.save()
								
								#Save any changes in long term storage
								ptltm = PossibleTextLTM(user=request.user,text_set=tmp.text_set,experience_id=tmp.id,stm_id=tmp.id,text=tmp.text,text_type=tmp.text_type,text_importance=tmp.text_importance,response_type=tmp.response_type,show_user=tmp.show_user,date_created=tmp.date_created,date_altered=datetime.now(pytz.utc))
								ptltm.save()

						return HttpResponseRedirect('/ent/text_set_detail/'+str(ideal_experience.id))

					else:
						messages.add_message(request, messages.INFO, 'Not Valid')
						return HttpResponseRedirect('/ent/text_set_detail/'+ str(ideal_experience.id))

				

			     
			
			context = {
				"form_text_set_new": form_text_set_new,
				"text_for_user": text_for_user,
				"number_of_experiences": number_of_experiences,
				"number_of_texts": number_of_texts,
				"text_per_week": text_per_week,
				"working_user_gen": working_user_gen,

				"helper": helper,
				"formset": formset,

				"number_of_texts": number_of_texts,

				"working_experience": working_experience,

			}
			return render(request, "text_set_detail.html", context)
	else:
		return HttpResponseRedirect('/accounts/signup/')




def text_set_alter(request,id=None):
	print("TEXT SET ALTER")
	ideal_experience = ExperienceSetting.objects.all().get(id=id)
	working_settings = UserSetting.objects.all().get(user=request.user)

	if ExperienceSetting.objects.all().filter(user=request.user).filter(experience='user').filter(ideal_id=id).count()<1:
		working_user_gen = PossibleTextSTM.objects.all().filter(show_user=False).filter(text_type="library").filter(experience_id=id)
		text_for_user = "This experience is NOT enabled"
		working_experience = ExperienceSetting.objects.all().get(id=id)
		number_of_experiences = 0

		print("ideal_experience.prompts_per_week:", ideal_experience.prompts_per_week)
		tmp_exp = ExperienceSetting(user=request.user,user_state="disable",ideal_id=ideal_experience.id,experience='user',description=working_experience.description,text_set=working_experience.text_set,prompts_per_week=ideal_experience.prompts_per_week)
		#gotta do the other stuff too
		tmp_exp.prompt_interval_minute_avg,tmp_exp.prompt_interval_minute_min,tmp_exp.prompt_interval_minute_max = figure_out_timing(user=request.user,text_per_week=tmp_exp.prompts_per_week)
		tmp_exp.save()

		#INITIALIZE TEXTS
		tmp_texts = PossibleTextSTM.objects.all().filter(text_type="library").filter(experience_id=working_experience.id)

		for text in tmp_texts:
			tmp_new = PossibleTextSTM(user=request.user,text=text.text,response_type=text.response_type,experience_id=text.experience_id,text_set=text.text_set,text_type="user",text_importance=text.text_importance,date_created=text.date_created)
			tmp_new.save()

		print("enable")

		

	else:
		working_user_gen = PossibleTextSTM.objects.all().filter(user=request.user).filter(show_user=False).filter(text_type="user").filter(experience_id=id)
		text_for_user = "This experience is enabled"
		working_experience = ExperienceSetting.objects.all().filter(user=request.user).filter(experience='user').get(ideal_id=id)
		number_of_experiences = ExperienceSetting.objects.all().filter(user=request.user).filter(experience='user').filter(ideal_id=id).count()

		default_texts = PossibleTextSTM.objects.all().filter(show_user=False).filter(text_type="library").filter(experience_id=id)

		user_experience = ExperienceSetting.objects.all().filter(experience="user").filter(text_set=ideal_experience.text_set)
		user_texts = PossibleTextSTM.objects.all().filter(user=request.user).filter(show_user=False).filter(text_type="user").filter(experience_id=id)
		user_outgoing = ActualTextSTM.objects.all().filter(user=request.user).filter(text_type="user").filter(experience_id=id).filter(time_sent__isnull=True)
		print("OUTCOING COUNT", user_outgoing.count())

		for exp in user_experience:
			exp.delete()

		for text in user_texts:
			text.delete()

		for text in user_outgoing:
			text.delete()			
		
		working_settings.save()
		
		print("REMOVE")
	
	if working_settings.new_user_pages < 2:
		return HttpResponseRedirect('/ent/new_user/')
	else:
		return HttpResponseRedirect('/ent/feeds_edit/')




	
	

#User settings
def text_set(request):
	if request.user.is_authenticated():	

		form_text_set_new= AddNewTextSetForm_full(request.POST or None)
		working_experience_sets = ExperienceSetting.objects.all().filter(user=request.user).exclude(text_set="user generated").filter(experience='user')

		number_of_experiences = ExperienceSetting.objects.all().filter(experience='user').filter(user=request.user).exclude(text_set="user generated").count()
		library_experiences_tmp = ExperienceSetting.objects.all().filter(experience='library')

		library_experiences = library_experiences_tmp | working_experience_sets


		for exp in library_experiences:
			if library_experiences.filter(ideal_id=exp.ideal_id).count() > 1:
				tmp_remove = library_experiences.filter(experience="library").get(ideal_id=exp.ideal_id)
				library_experiences = library_experiences.exclude(id=tmp_remove.id)


		########## NOW THE FORM HANDLING STUFF
		if request.method == "POST":
			if 'submit_new_text_set' in request.POST:
				if form_text_set_new.is_valid():	
					tmp = form_text_set_new.save()
					tmp.user=request.user
					
					####   YOU WILL HAVE TO SET THE TIMING HERE							
				return HttpResponseRedirect('/ent/text_set/')

		context = {
			"number_of_experiences": number_of_experiences,
			"working_experience_sets": working_experience_sets,
			"form_text_set_new": form_text_set_new,
			"library_experiences": library_experiences,


		}
		return render(request, "text_set.html", context)
	else:
		return HttpResponseRedirect('/accounts/signup/')





def add_texts(request):
	if request.user.is_authenticated():	
		form_new_text = NewUser_PossibleTextSTMForm(request.POST or None)
		number_of_texts = PossibleTextSTM.objects.all().filter(user=request.user).filter(text_type='user').count()


		if request.method == "POST":
			
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
						return HttpResponseRedirect('/ent/feeds_edit/add_texts')

					else:
						return HttpResponseRedirect('/ent/feeds_edit/')
				else:
					if 'submit_finished_adding' in request.POST and number_of_texts > 0:
						return HttpResponseRedirect('/ent/feeds_edit/')

		else:
			form_new_text = NewUser_PossibleTextSTMForm(request.POST or None)

		context = {
				"number_of_texts": number_of_texts,
				"form_new_text": form_new_text,
			}
		
		return render(request, "add_new_texts.html", context)
	else:
		return HttpResponseRedirect('/accounts/signup/')

def new_user_help(request):
	if request.user.is_authenticated():	
	
		
		context = {
			
		}			

		return render(request,"new_user_help.html",context)
	else:
		return render(request,"new_user_help.html")


def new_user(request):
	if request.user.is_authenticated():	
		if  UserSetting.objects.filter(user=request.user).exists():
			working_settings = UserSetting.objects.all().get(user=request.user)
		else: 
			working_settings = UserSetting(user=request.user,begin_date=datetime.now(pytz.utc),respite_until_datetime = datetime.now(pytz.utc)).save()
			working_settings = UserSetting.objects.all().get(user=request.user)

		lib_usr_tmp = ExperienceSetting.objects.all().filter(experience='library').get(text_set="user generated")
		if ExperienceSetting.objects.filter(user=request.user).filter(experience='user').filter(ideal_id=lib_usr_tmp.id).exists():
			working_experience = ExperienceSetting.objects.all().filter(experience='user').filter(user=request.user).get(ideal_id=lib_usr_tmp.id)
		else: 
			working_experience = ExperienceSetting(user=request.user,experience='user',text_set="user generated",ideal_id=lib_usr_tmp.id,user_state="disable").save()
			working_experience = ExperienceSetting.objects.all().filter(experience='user').filter(user=request.user).get(ideal_id=lib_usr_tmp.id)

		if ExperienceSetting.objects.all().filter(user=request.user).count()>0:
			update_experiences(user=request.user)
				

		form_new_text = NewUser_PossibleTextSTMForm(request.POST or None)
		form_new_user = NewUserForm(request.POST or None, instance=working_settings)
		
		
		working_experience_sets = ExperienceSetting.objects.all().filter(user=request.user).filter(experience='user')
		library_experiences = ExperienceSetting.objects.all().filter(experience='library').filter(active=1)
		
		number_of_experiences = ExperienceSetting.objects.all().filter(experience='user').filter(user=request.user).count()
		
		prompts_per_week = working_settings.prompts_per_week
		number_of_texts = PossibleTextSTM.objects.all().filter(user=request.user).filter(text_type='user').count()

		library_experiences_tmp = ExperienceSetting.objects.all().filter(experience='library')
		library_experiences = library_experiences_tmp | working_experience_sets

		for exp in library_experiences:
			if library_experiences.filter(ideal_id=exp.ideal_id).count() > 1:
				tmp_remove = library_experiences.filter(experience="library").get(ideal_id=exp.ideal_id)
				library_experiences = library_experiences.exclude(id=tmp_remove.id)


		if working_settings.new_user_pages < 2:
			graph_data_simulated_heatmap = 0
		else:
			generate_random_prompts_to_show(request,exp_resp_rate=.6,week=1,number_of_prompts=20) #set up 20 random prompts based upon the settings
			graph_data_simulated_heatmap = get_graph_data_simulated_heatmap(request)

		# if working_settings.new_user_pages == 2:
			# working_settings.new_user_pages = 3


		if request.GET.get('finished_experience'):
			if PossibleTextSTM.objects.all().filter(user=request.user).count()>0:
				if working_settings.new_user_pages== 1:
					working_settings.new_user_pages = 2
					working_settings.save()
					return HttpResponseRedirect('/ent/new_user/')
	


		########## NOW THE FORM HANDLING STUFF
		if request.method == "POST":
			print("REQUEST POST")
			print("REQUEST POST STUFF", request.POST)
			
			if 'submit_new_text' in request.POST or 'submit_finished_adding' in request.POST:
				print("NEW")
				if form_new_text.is_valid():	
					tmp = form_new_text.save()
					tmp.user=request.user
					tmp.experience_id=working_experience.ideal_id
					if tmp.date_created is None:
						tmp.date_created = datetime.now(pytz.utc)
					tmp.text_type = 'user'
					tmp.save()

					if not 'user generated' in working_settings.active_experiences:
						working_settings.active_experiences="user generated,"+working_settings.active_experiences
					
					#Save any changes in long term storage
					ptltm = PossibleTextLTM(user=request.user,experience_id=working_experience.ideal_id,stm_id=tmp.id,text=tmp.text,text_type=tmp.text_type,text_importance=tmp.text_importance,response_type=tmp.response_type,show_user=tmp.show_user,date_created=tmp.date_created,date_altered=datetime.now(pytz.utc))
					ptltm.save()

					if 'submit_new_text'in request.POST:
						return HttpResponseRedirect('/ent/new_user/')

					else:
						if working_settings.new_user_pages== 1 and PossibleTextSTM.objects.all().filter(user=request.user).count()>0:
							working_settings.new_user_pages = 2
							working_settings.save()
						return HttpResponseRedirect('/ent/simulate_week/')
				else:
					if 'submit_finished_adding' in request.POST and PossibleTextSTM.objects.all().filter(user=request.user).count()>0:
						if working_settings.new_user_pages== 1:
							working_settings.new_user_pages = 2
							working_settings.save()
					return HttpResponseRedirect('/ent/simulate_week/')		


			elif 'submit_contact' in request.POST:
				print("new_user")
				if form_new_user.is_valid():
					tmp_settings = form_new_user.save(commit=False)
					tmp_settings.save()

					if tmp_settings.phone_input != "":
						if len(str(get_num(tmp_settings.phone_input))) == 10:
							tmp_settings.phone = str(get_num(tmp_settings.phone_input))
							tmp_settings.send_text = bool(True)	#just a switch to say the person can be texted
							tmp_settings.sms_address =  tmp_settings.phone_input + str(carrier_lookup(tmp_settings.carrier)) #Figures otu the address the promtps need to be sent to
							tmp_settings.respite_until_datetime = datetime.now(pytz.utc) #initializes the respite until date (this actually just needs to be set because it does a greater than check)

							if working_settings.new_user_pages < 1:
								working_settings.new_user_pages = 1
								working_settings.save()

							tmp_settings.save()
						else:
							messages.add_message(request, messages.INFO, 'Not 10 Expecting a 10 digit US number')
					
					return HttpResponseRedirect('/ent/new_user/')		


			print("NOTHING")
			return HttpResponseRedirect('/ent/simulate_week/')		

		if number_of_texts > 0:
			ready_to_move_on = 1
		else:
			ready_to_move_on = 0
		
		context = {
			"prompts_per_week": prompts_per_week,
			"number_of_texts": number_of_texts,
			"form_new_text": form_new_text,
			"graph_data_simulated_heatmap": graph_data_simulated_heatmap,
			"library_experiences": library_experiences,
			"number_of_experiences": number_of_experiences,
			"ready_to_move_on":ready_to_move_on,

			
			"form_new_user": form_new_user,
			
		}
		if working_settings.new_user_pages == 0:
			return render(request, "new_user_page1.html", context)
		elif working_settings.new_user_pages == 1:
			return render(request, "new_user_page2.html", context)
		elif working_settings.new_user_pages == 2:
			return HttpResponseRedirect('/ent/simulate_week/')	
		else:
			return HttpResponseRedirect('/ent/simulate_week/')
	else:
		return HttpResponseRedirect('/accounts/signup/')


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



def contact_settings(request):
	if request.user.is_authenticated():	

		if  UserSetting.objects.filter(user=request.user).exists():
			working_settings = UserSetting.objects.all().get(user=request.user)
		else: 
			working_settings = UserSetting(user=request.user,begin_date=datetime.now(pytz.utc)).save()
			working_settings = UserSetting.objects.all().get(user=request.user)

		
		
		form_free = UserSettingForm_Prompt(request.POST or None, instance=working_settings)
		
		form_prompt_percent = UserSettingForm_PromptRate(request.POST or None, instance = working_settings)
		
		
		

		########## NOW THE FORM HANDLING STUFF
		if request.method == "POST":
			if 'submit_contact' in request.POST:
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
					return HttpResponseRedirect('/ent/contact_settings/')		
				else:
					messages.add_message(request, messages.INFO, 'Not Valid')
					return HttpResponseRedirect('/ent/contact_settings/')		

			
		

		context = {

			"form_free": form_free,
			
		}
		return render(request, "settings_contact.html", context)
	else:
		return HttpResponseRedirect('/accounts/signup/')		










#User settings

def initialize_research_texts(user):
	if PossibleTextSTM.objects.all().filter(user=user).filter(text_type="research").count() > 0 :
		rtexts = PossibleTextSTM.objects.all().filter(user=user).filter(text_type="research")
		for rtext in rtexts:
			rtext.delete()

	rtexts = PossibleTextSTM.objects.all().filter(text_type="research").filter(system_text=2)
	for rtext in rtexts:
		tmp = PossibleTextSTM(user=user,text_type="research",text_set="research",text=rtext.text,text_importance=rtext.text_importance)
		tmp.save()







def simulate_week(request):
	if request.user.is_authenticated():	
		if  UserSetting.objects.filter(user=request.user).exists():
			working_settings = UserSetting.objects.all().get(user=request.user)
		else: 
			working_settings = UserSetting(user=request.user,begin_date=datetime.now(pytz.utc)).save()
			working_settings = UserSetting.objects.all().get(user=request.user)


		if ExperienceSetting.objects.filter(user=request.user).filter(experience='user').filter(text_set="user generated").count()>0:
			working_experience = ExperienceSetting.objects.all().filter(experience='user').filter(user=request.user).filter(text_set="user generated").first()
		else: 
			working_experience = ExperienceSetting(user=request.user,experience='user',text_set="user generated").save()
			working_experience = ExperienceSetting.objects.all().filter(experience='user').filter(user=request.user).filter(text_set="user generated").first()

		update_experiences(user=request.user)

		

		
		
		generate_random_prompts_to_show(request,exp_resp_rate=.6,week=1,number_of_prompts=0) #set up 20 random prompts based upon the settings
		graph_data_simulated_heatmap = get_graph_data_simulated_heatmap(request)
		graph_data_histogram_timing = get_graph_data_histogram_timing(request)
		prompts_per_week = working_settings.prompts_per_week

		actual_number_texts = ActualTextSTM_SIM.objects.all().filter(user=request.user).count()

		text_sets = ExperienceSetting.objects.all().exclude(experience='library').filter(user=request.user).values('text_set').distinct()

		total_expected_number = 0
		working_experience_sets = ExperienceSetting.objects.all().filter(user=request.user).exclude(experience='library').filter(prompts_per_week__gt = 0).filter(number_of_texts_in_set__gt = 0)

		count_out = []
		exp_out = []
		list_out = []
		for exp in working_experience_sets:
			total_expected_number = int(exp.prompts_per_week) + total_expected_number
			exp_out.append(int(exp.prompts_per_week))
			count_out.append(int(ActualTextSTM_SIM.objects.all().filter(user=request.user).filter(text_set=exp.text_set).count()))
			list_out.append({"name":exp.text_set,"expected":int(exp.prompts_per_week),"ideal_id":exp.ideal_id,"observed":int(ActualTextSTM_SIM.objects.all().filter(user=request.user).filter(text_set=exp.text_set).count())})
			# print("total_expected_number",total_expected_number )

		print("total_expected_number",total_expected_number)

		

		# print(ExperienceSetting.objects.all().filter(experience='user').filter(user=request.user).values('text_set').distinct().aggregate("Count"))





		context = {
			"prompts_per_week": prompts_per_week,
			"actual_number_texts": actual_number_texts,
			"text_sets": text_sets,
			"total_expected_number": total_expected_number,
			"count_out": count_out,
			"exp_out": exp_out,
			"list_out": list_out,

			"graph_data_simulated_heatmap": graph_data_simulated_heatmap,
			"graph_data_histogram_timing": graph_data_histogram_timing,
		}
		return render(request, "simulated_week.html", context)
	else:
		return HttpResponseRedirect('/accounts/signup/')		


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
