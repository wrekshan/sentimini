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
from .forms import  AddNewGroup_Creator_Form, KT_PossibleTextSTMForm, ContactSettingsForm, PossibleTextSTMForm, NewUserForm, NewUser_PossibleTextSTMForm, AddNewTextSetForm_full, AddNewTextSetForm_fullFormSetHelper, TextSetFormSetHelper, ExperienceTimingForm, Edit_PossibleTextSTMForm
from .models import GroupSetting, PossibleTextSTM, ActualTextSTM, UserSetting, Carrier, Respite, Ontology, UserGenPromptFixed, PossibleTextLTM, FeedSetting, ActualTextSTM_SIM

from sentimini.sentimini_functions import  get_graph_data_simulated, get_graph_data_simulated_heatmap
from sentimini.scheduler_functions import generate_random_prompts_to_show_no_sim, generate_random_prompts_to_show, next_prompt_minutes, determine_next_prompt_series, next_response_minutes, figure_out_timing

from sentimini.tasks import send_texts, schedule_texts, set_next_prompt, determine_prompt_texts, set_prompt_time, check_email_for_new, process_new_mail, actual_text_consolidate, check_for_nonresponse, generate_random_minutes, schedule_greeting_text



def advanced_uses(request):
	if request.user.is_authenticated():	


		context = {
			
		}			

		return render(request,"advanced_uses.html",context)
	else:
		return HttpResponseRedirect('/accounts/signup/')

def create_new_feed_page(request,group_id=None):
	if request.user.is_authenticated():
		working_settings = UserSetting.objects.all().get(user=request.user)
		back_page = request.META['HTTP_REFERER']
		pages = back_page.split("/")
		print(pages)
		print(pages[len(pages)-2])

		if group_id is not None:
			working_group = GroupSetting.objects.all().filter(user=request.user).get(id=pages[len(pages)-2])
			group_name = working_group.group_name
		else:
			group_name = "basic"
			group_id = 0

		
		form_feed_name_new= AddNewTextSetForm_full(request.POST or None)

		if request.method == "POST":
			if 'submit_feed_description' in request.POST:
				if form_feed_name_new.is_valid():
					tmp = form_feed_name_new.save(commit=True)
					tmp.user = request.user
					tmp.save()
					
					working_experience = FeedSetting.objects.all().filter(user=request.user).get(id=tmp.id)
					working_experience.feed_id = working_experience.id
					working_experience.group_id = group_id
					working_experience.group_name = group_name
					working_experience.user_state="disable"
					print("NEW FEED VALID")
					working_experience.text_interval_minute_avg,working_experience.text_interval_minute_min,working_experience.text_interval_minute_max = figure_out_timing(user=request.user,text_per_week=working_experience.texts_per_week)
					print("AFTER FEED VALID")
					working_experience.save()

					return HttpResponseRedirect('/ent/add_texts/'+str(working_experience.id)+'/'+str(group_id))


		context = {
			"instruction_text": group_name,
			"form_feed_name_new": form_feed_name_new,
			"back_page": back_page,

		}

		return render(request, "text_set_detail_descriptions.html", context)
	else:
		return HttpResponseRedirect('/accounts/signup/')



				
			


def text_set_detail_descriptions(request, id=None):
	if request.user.is_authenticated():
		if FeedSetting.objects.all().filter(id=id).count()<1:
			return HttpResponseRedirect('/ent/feeds_edit/')
		else:
			ideal_experience = FeedSetting.objects.all().get(id=id)
			id_group = ideal_experience.group_id
			instruction_text = "ha"
			# working_group = GroupSetting.objects.all().get(id=id_group)

			if ideal_experience.group_name == 'basic':
				last_page_go_back = "feeds"
			else:
				last_page_go_back = "groups"

			if UserSetting.objects.all().get(user=request.user).new_user_pages < 2:
				new_user_pages = "new_user"
			else:
				new_user_pages = "old_user"

			if id_group > 0:
				working_group = GroupSetting.objects.all().filter(user=request.user).get(id=id_group)
				group_name = working_group.group_name
			else:
				group_name = "basic"
				group_id = 0

			if FeedSetting.objects.all().filter(user=request.user).filter(feed_type='user').filter(feed_id=id).count()<1:
				working_experience = FeedSetting.objects.all().get(id=id)
			else:
				working_experience = FeedSetting.objects.all().filter(user=request.user).filter(feed_type='user').get(feed_id=id)
				
				
			form_feed_name_new= AddNewTextSetForm_full(request.POST or None, instance = working_experience)
			
			########## NOW THE FORM HANDLING STUFF
			if request.method == "POST":
				if 'submit_feed_description' in request.POST:
					if form_feed_name_new.is_valid():
						# tmp_exp = FeedSetting.objects.all().filter(experience="user").get(feed_id=ideal_experience.id)

						tmp = form_feed_name_new.save(commit=False)
						tmp.texts_per_week = tmp.texts_per_week
						tmp.text_interval_minute_avg,tmp.text_interval_minute_min,tmp.text_interval_minute_max = figure_out_timing(user=request.user,text_per_week=tmp.texts_per_week)
						tmp.save()	

					
						return HttpResponseRedirect('/ent/text_set_detail/'+str(ideal_experience.id)+'/'+str(id_group))


			context = {
				"form_feed_name_new": form_feed_name_new,
				"new_user_pages": new_user_pages,
				"last_page_go_back": last_page_go_back,
				"id_group": id_group,
				"feed_id": int(id),
				"group_id": id_group,
				"instruction_text": group_name,

				
				"working_experience": working_experience,

			}
			return render(request, "text_set_detail_descriptions.html", context)
	else:
		return HttpResponseRedirect('/accounts/signup/')










def group_edit_detail(request, id=None):
	if request.user.is_authenticated():	
		if FeedSetting.objects.all().filter(user=request.user).count()>0:
			update_experiences(user=request.user)

		if id is None:
			form_group_settings = AddNewGroup_Creator_Form(request.POST or None)

			context = {
			
				"form_group_settings": form_group_settings,
			
			}
			
		else:
			working_group = GroupSetting.objects.all().get(id=id)
			working_user_feeds = FeedSetting.objects.all().filter(feed_type="user").filter(group_id = id)
			working_library_feeds = FeedSetting.objects.all().filter(feed_type="library").filter(group_id = id)

			working_user_texts = PossibleTextSTM.objects.all().filter(group_id=id)

			form_group_settings = AddNewGroup_Creator_Form(request.POST or None, instance = working_group)

			form_new_text = KT_PossibleTextSTMForm(request.POST or None)
			context = {
				"working_group": working_group,
				"form_group_settings": form_group_settings,
				"form_new_text": form_new_text,
				"working_user_feeds": working_user_feeds,
				"working_library_feeds": working_library_feeds,
			}

		if request.GET.get('create_new_feed'):
			print("CREATING NEW FEED PRESSED")
			FeedSetting(user=request.user,feed_type='user',feed_name="New Set",group_name=working_group.group_name,group_id=working_group.id,user_state="disable").save()

			working_experience = FeedSetting.objects.all().filter(user=request.user).filter(group_id=working_group.id).filter(feed_type="user").get(feed_name="New Set")
			working_experience.feed_id = working_experience.id
			working_experience.save()

			return HttpResponseRedirect('/ent/text_set_detail/'+str(working_experience.id))


		if request.method == "POST":
			if 'submit_new_group' in request.POST:
				print("NEW GROUP HERE HERE")
				if form_group_settings.is_valid():	
					print("IS VALID HERE HERE")
					tmp = form_group_settings.save()
					tmp.group_type="user"
					tmp.save()
				
				return HttpResponseRedirect('/ent/group_detail/'+str(tmp.id))	

				

		
			

		return render(request, "group_edit_detail.html", context)
	else:
		return HttpResponseRedirect('/accounts/signup/')


def group_detail(request,id=None):
	if request.user.is_authenticated():	
		if FeedSetting.objects.all().filter(user=request.user).count()>0:
			update_experiences(user=request.user)
		
		working_group = GroupSetting.objects.all().get(id=id)
		working_user_feeds = FeedSetting.objects.all().filter(feed_type="user").filter(group_id = id)
		working_library_feeds = FeedSetting.objects.all().filter(feed_type="library").filter(group_id = id)

		working_user_texts = PossibleTextSTM.objects.all().filter(group_id=id)

		form_group_settings = AddNewGroup_Creator_Form(request.POST or None, instance = working_group)

		form_new_text = KT_PossibleTextSTMForm(request.POST or None)


		if request.GET.get('remove_group'):
			working_user_gen = PossibleTextSTM.objects.all().filter(user=request.user).filter(show_user=False).filter(feed_type="user").filter(feed_id=id)
			text_for_user = "This experience is enabled"
			working_experience = FeedSetting.objects.all().filter(user=request.user).filter(feed_type='user').get(feed_id=id)
			number_of_experiences = FeedSetting.objects.all().filter(user=request.user).filter(feed_type='user').filter(feed_id=id).count()

			user_experience = FeedSetting.objects.all().filter(feed_type="user").filter(feed_id=id)
			user_texts = PossibleTextSTM.objects.all().filter(user=request.user).filter(show_user=False).filter(feed_type="user").filter(feed_id=id)
			user_outgoing = ActualTextSTM.objects.all().filter(user=request.user).filter(feed_type="user").filter(feed_id=id).filter(time_sent__isnull=True)

			for exp in user_experience:
				exp.delete()

			for text in user_texts:
				text.delete()

			for text in user_outgoing:
				text.delete()
			
			return HttpResponseRedirect('/ent/feeds_edit/')

		if request.GET.get('enable_group'):
			ideal_group = GroupSetting.objects.all().get(id=id)
			feeds = FeedSetting.objects.all().filter(group_id=id)

			print("ENABLE PRESSED")

			if FeedSetting.objects.all().filter(user=request.user).filter(feed_type='user').filter(feed_id=id).count()<1:
				working_user_gen = PossibleTextSTM.objects.all().filter(show_user=False).filter(feed_type="library").filter(feed_id=id)
				text_for_user = "This experience is NOT enabled"
				working_experience = FeedSetting.objects.all().get(id=id)
				number_of_experiences = 0
				
				# Create and save new one
				create_new_user_experience(user=request.user,feed_id=working_experience.id,default_experience='library')
				return HttpResponseRedirect('/ent/text_set_detail/'+str(ideal_experience.id))



		if request.GET.get('create_new_feed'):
			
			return HttpResponseRedirect('/ent/create_new_feed_page/'+str(id))			

			# print("CREATING NEW FEED PRESSED")
			# FeedSetting(user=request.user,feed_type='user',feed_name="New Set",group_name=working_group.group_name,group_id=working_group.id,user_state="disable").save()

			# working_experience = FeedSetting.objects.all().filter(user=request.user).filter(group_id=working_group.id).filter(feed_type="user").get(feed_name="New Set")
			# working_experience.feed_id = working_experience.id
			# working_experience.save()

			# return HttpResponseRedirect('/ent/text_set_detail/'+str(working_experience.id))


		if request.method == "POST":
			if 'submit_new_group' in request.POST:
				if form_group_settings.is_valid():	
					tmp = form_group_settings.save()
					tmp.save()
				
				HttpResponseRedirect('/ent/group_detail/'+str(id))	

			if 'submit_new_text' in request.POST:
				if form_new_text.is_valid():	
					tmp = form_new_text.save()
					tmp.user=request.user
					tmp.feed_id = kt_group_exp.id
					tmp.unique_feed_name = kt_group_exp.unique_feed_name
					tmp.feed_name = kt_group_exp.feed_name
					tmp.feed_type = kt_group_exp.feed_type

					tmp.group_id=working_group.id
					tmp.group_name=str(working_group.group_name)

				
					
					if tmp.date_created is None:
						tmp.date_created = datetime.now(pytz.utc)
					tmp.save()
				
				HttpResponseRedirect('/ent/kt_group')

			# elif 'submit_prompt_percent' in request.POST:
			# 	if form_exp_timing.is_valid():
			# 		form_exp_timing.save()
			# 		HttpResponseRedirect('/ent/kt_group')


	
		context = {
			"working_group": working_group,
			"form_group_settings": form_group_settings,
			"form_new_text": form_new_text,
			"working_user_feeds": working_user_feeds,
			"working_library_feeds": working_library_feeds,
		}

		return render(request, "groups_detail.html", context)
	else:
		return HttpResponseRedirect('/accounts/signup/')





def create_new_user_experience(user,feed_id,default_experience):
	if feed_id == "Create New":
		FeedSetting(user=user,feed_type='user',feed_name="New Set",user_state="disable").save()
		working_experience = FeedSetting.objects.all().filter(user=user).filter(feed_type="user").get(feed_name="New Set")
		working_experience.feed_id = working_experience.id
		working_experience.description = working_experience.description
		working_experience.unique_feed_name = working_experience.unique_feed_name
		feed_id = working_experience.id
		working_experience.save()

	if FeedSetting.objects.filter(user=user).filter(feed_type='user').filter(feed_id=feed_id).count()<1:
		print("default_experience",default_experience)
		print("feed_id",feed_id)
		library_tmp = FeedSetting.objects.all().filter(feed_type=default_experience).get(feed_id=feed_id)
		FeedSetting(user=user,feed_type='user',feed_id=feed_id,description=library_tmp.description,feed_name=library_tmp.feed_name,user_state="disable").save()
		working_experience = FeedSetting.objects.all().filter(user=user).filter(feed_type="user").get(feed_id=feed_id)

		#INITIALIZE TEXTS
		if PossibleTextSTM.objects.all().filter(feed_type=default_experience).filter(feed_id=feed_id).count() > 0 :
			tmp_texts = PossibleTextSTM.objects.all().filter(feed_type=default_experience).filter(feed_id=feed_id,feed_name=working_experience.feed_name)

			for text in tmp_texts:
				tmp_new = PossibleTextSTM(user=user,text=text.text,group_name=text.group_name,group_id=text.group_id,response_type=text.response_type,feed_id=text.feed_id,feed_name=text.feed_name,feed_type="user",text_importance=text.text_importance,date_created=text.date_created)
				tmp_new.save()

		# You have to add in the texts

# def groups_create(request):
# 	if request.user.is_authenticated():	
# 		new_group_form = AddNewGroup_Creator_Form()

# 		if request.method == "POST":
# 			if 'submit_new_group' in request.POST:
# 				if new_group_form.is_valid():	
# 					tmp = new_group_form.save()
# 					tmp.user = request.user
# 					tmp.save()

# 				HttpResponseRedirect('/ent/groups_edit/')

# 		context = {
# 			# "form_exp_timing": form_exp_timing,
# 			"new_group_form": new_group_form,
			
# 		}

# 		return render(request, "groups_create.html", context)
# 	else:
# 		return HttpResponseRedirect('/accounts/signup/')




def groups_edit(request):
	if request.user.is_authenticated():	
		#Update the tables with the right numbers of texts

		if UserSetting.objects.all().get(user=request.user).new_user_pages < 2:
			return HttpResponseRedirect('/ent/new_user/')

		# if GroupSetting.objects.all().filter(user=request.user).count()>0:
			# update_experiences(user=request.user)
		

		number_of_experiences = GroupSetting.objects.all().filter(group_type='user').filter(user=request.user).count()
		working_groups = GroupSetting.objects.all().filter(user=request.user).filter(group_type='user')
		library_experiences = GroupSetting.objects.all().filter(viewable=True)

		if request.GET.get('create_new_group'):		
			return HttpResponseRedirect('/ent/group_edit_detail/')		
			# new_group = GroupSetting(user=request.user,group_type="user")
			# new_group.save()
			
			

			
			
		
	
		context = {
			"number_of_experiences": number_of_experiences,
			"working_groups": working_groups,
			"library_experiences": library_experiences,
		}

		return render(request, "groups_edit.html", context)
	else:
		return HttpResponseRedirect('/accounts/signup/')


# def group_alter(request,id=None):
# 	print("TEXT SET ALTER")
# 	ideal_experience = GroupSetting.objects.all().get(id=id)
# 	working_settings = UserSetting.objects.all().get(user=request.user)

# 	if FeedSetting.objects.all().filter(user=request.user).filter(feed_type='user').filter(feed_id=id).count()<1:
# 		working_user_gen = PossibleTextSTM.objects.all().filter(show_user=False).filter(feed_type="library").filter(feed_id=id)
# 		text_for_user = "This experience is NOT enabled"
# 		working_experience = FeedSetting.objects.all().get(id=id)
# 		number_of_experiences = 0

# 		print("ideal_experience.texts_per_week:", ideal_experience.texts_per_week)
# 		tmp_exp = FeedSetting(user=request.user,user_state="disable",feed_id=ideal_experience.id,feed_type='user',description=working_experience.description,feed_name=working_experience.feed_name,texts_per_week=ideal_experience.texts_per_week)
# 		#gotta do the other stuff too
# 		tmp_exp.text_interval_minute_avg,tmp_exp.text_interval_minute_min,tmp_exp.text_interval_minute_max = figure_out_timing(user=request.user,text_per_week=tmp_exp.texts_per_week)
# 		tmp_exp.save()

# 		#INITIALIZE TEXTS
# 		tmp_texts = PossibleTextSTM.objects.all().filter(feed_type="library").filter(feed_id=working_experience.id)

# 		for text in tmp_texts:
# 			tmp_new = PossibleTextSTM(user=request.user,text=text.text,response_type=text.response_type,feed_id=text.feed_id,feed_name=text.feed_name,feed_type="user",text_importance=text.text_importance,date_created=text.date_created)
# 			tmp_new.save()

# 		print("enable")

		

# 	else:
# 		working_user_gen = PossibleTextSTM.objects.all().filter(user=request.user).filter(show_user=False).filter(feed_type="user").filter(feed_id=id)
# 		text_for_user = "This experience is enabled"
# 		working_experience = FeedSetting.objects.all().filter(user=request.user).filter(feed_type='user').get(feed_id=id)
# 		number_of_experiences = FeedSetting.objects.all().filter(user=request.user).filter(feed_type='user').filter(feed_id=id).count()

# 		default_texts = PossibleTextSTM.objects.all().filter(show_user=False).filter(feed_type="library").filter(feed_id=id)

# 		user_experience = FeedSetting.objects.all().filter(feed_type="user").filter(feed_name=ideal_experience.feed_name)
# 		user_texts = PossibleTextSTM.objects.all().filter(user=request.user).filter(show_user=False).filter(feed_type="user").filter(feed_id=id)
# 		user_outgoing = ActualTextSTM.objects.all().filter(user=request.user).filter(feed_type="user").filter(feed_id=id).filter(time_sent__isnull=True)
# 		print("OUTCOING COUNT", user_outgoing.count())

# 		for exp in user_experience:
# 			exp.delete()

# 		for text in user_texts:
# 			text.delete()

# 		for text in user_outgoing:
# 			text.delete()			
		
# 		working_settings.save()
		
# 		print("REMOVE")
	
# 	if working_settings.new_user_pages < 2:
# 		return HttpResponseRedirect('/ent/new_user/')
# 	else:
# 		return HttpResponseRedirect('/ent/feeds_edit/')





def update_experiences(user):
	working_experience = FeedSetting.objects.all().filter(user=user)

	for exp in working_experience:
		exp.number_of_texts_in_set = PossibleTextSTM.objects.all().filter(user=user).filter(feed_type=exp.feed_type).filter(feed_name=exp.feed_name).count()
		#figure out timing
		exp.text_interval_minute_avg, exp.text_interval_minute_min, exp.text_interval_minute_max = figure_out_timing(user=user,text_per_week=exp.texts_per_week)
		exp.save()




def text_delete(request,id=None):
	print("ID HERE:'", id)

	back_page = request.META['HTTP_REFERER']
	PossibleTextSTM.objects.all().get(id=id).delete()

	return HttpResponseRedirect(back_page)



def text_activate(request,id=None):
	print("ACTIVATE ID HERE:'", id)
	text = PossibleTextSTM.objects.all().get(id=id)
	PossibleTextSTM(user=request.user,text=text.text,group_name=text.group_name,group_id=text.group_id,response_type=text.response_type,feed_id=text.feed_id,feed_name=text.feed_name,feed_type="user",text_importance=text.text_importance,date_created=text.date_created).save()
	return HttpResponseRedirect('/ent/kt_group')


def kt_group(request):
	if request.user.is_authenticated():	
		if FeedSetting.objects.all().filter(user=request.user).count()>0:
			update_experiences(user=request.user)
		
		kt_group_exp = FeedSetting.objects.all().filter(feed_type='kt').get(unique_feed_name='kt_library_1')
		if FeedSetting.objects.all().filter(user=request.user).filter(feed_type='user').filter(feed_id=kt_group_exp.id).count() < 1:
			print("LESS 1")
			create_new_user_experience(user=request.user,feed_id=kt_group_exp.id, default_experience='kt')

		working_experience = FeedSetting.objects.all().filter(user=request.user).filter(feed_type='user').get(feed_id=kt_group_exp.id)
		# form_exp_timing= ExperienceTimingForm(request.POST or None, instance = working_experience)
		form_new_text = KT_PossibleTextSTMForm(request.POST or None)


		working_user_texts = PossibleTextSTM.objects.all().filter(show_user=False).filter(feed_type="user").filter(feed_id=kt_group_exp.id)
		working_kt_library = PossibleTextSTM.objects.all().filter(show_user=False).filter(feed_type="kt").filter(feed_id=kt_group_exp.id)

		
		if request.method == "POST":
			if 'submit_new_text' in request.POST:
				if form_new_text.is_valid():	
					tmp = form_new_text.save()
					tmp.user=request.user
					tmp.feed_id = kt_group_exp.id
					tmp.unique_feed_name = kt_group_exp.unique_feed_name
					tmp.feed_name = kt_group_exp.feed_name
					tmp.feed_type = kt_group_exp.feed_type
					
					if tmp.date_created is None:
						tmp.date_created = datetime.now(pytz.utc)
					tmp.save()
					HttpResponseRedirect('/ent/kt_group')

			# elif 'submit_prompt_percent' in request.POST:
			# 	if form_exp_timing.is_valid():
			# 		form_exp_timing.save()
			# 		HttpResponseRedirect('/ent/kt_group')


	
		context = {
			# "form_exp_timing": form_exp_timing,
			"form_new_text": form_new_text,
			"working_user_texts": working_user_texts,
			"working_kt_library": working_kt_library,
		}

		return render(request, "kt_group.html", context)
	else:
		return HttpResponseRedirect('/accounts/signup/')



def text_set_detail(request,feed_id=None,group_id=None):
	if request.user.is_authenticated():
		if FeedSetting.objects.all().filter(id=feed_id).count()<1:
			return HttpResponseRedirect('/ent/feeds_edit/')
		else:
			ideal_experience = FeedSetting.objects.all().get(id=feed_id)
			id_group = ideal_experience.group_id
			# working_group = GroupSetting.objects.all().get(id=id_group)

			if ideal_experience.group_name == 'basic':
				last_page_go_back = "feeds"
			else:
				last_page_go_back = "groups"

			if UserSetting.objects.all().get(user=request.user).new_user_pages < 2:
				new_user_pages = "new_user"
			else:
				new_user_pages = "old_user"

			if int(group_id)<1:
				if FeedSetting.objects.all().filter(user=request.user).filter(feed_type='user').filter(feed_id=feed_id).count()<1:
					working_user_gen = PossibleTextSTM.objects.all().filter(show_user=False).filter(feed_type="library").filter(feed_id=feed_id)
					text_for_user = "This experience is NOT enabled"
					working_experience = FeedSetting.objects.all().get(id=feed_id)
					number_of_experiences = 0
				else:
					working_user_gen = PossibleTextSTM.objects.all().filter(user=request.user).filter(show_user=False).filter(feed_type="user").filter(feed_id=feed_id)
					text_for_user = "This experience is enabled"
					working_experience = FeedSetting.objects.all().filter(user=request.user).filter(feed_type='user').get(feed_id=feed_id)
					number_of_experiences = FeedSetting.objects.all().filter(user=request.user).filter(feed_type='user').filter(feed_id=feed_id).count()
			else:
				if FeedSetting.objects.all().filter(user=request.user).filter(feed_type='user').filter(group_id=group_id).filter(feed_id=feed_id).count()<1:
					working_user_gen = PossibleTextSTM.objects.all().filter(show_user=False).filter(group_id=group_id).filter(feed_id=feed_id)
					text_for_user = "This experience is NOT enabled"
					working_experience = FeedSetting.objects.all().get(id=feed_id)
					number_of_experiences = 0
				else:
					working_user_gen = PossibleTextSTM.objects.all().filter(group_id=group_id).filter(show_user=False).filter(feed_type="user").filter(feed_id=feed_id)
					text_for_user = "This experience is enabled"
					working_experience = FeedSetting.objects.all().filter(user=request.user).filter(group_id=group_id).filter(feed_type='user').get(feed_id=feed_id)
					number_of_experiences = FeedSetting.objects.all().filter(user=request.user).filter(feed_type='user').filter(feed_id=feed_id).count()
				
			helper = TextSetFormSetHelper()
			UGPFormset = modelformset_factory(PossibleTextSTM, form = PossibleTextSTMForm, extra=1)
			formset = UGPFormset(queryset = working_user_gen)
			form_feed_name_new= AddNewTextSetForm_full(request.POST or None, instance = working_experience)
			form_new_text = NewUser_PossibleTextSTMForm(request.POST)
			
			number_of_texts = working_user_gen.count()
			text_per_week = working_experience.texts_per_week

			if request.GET.get('remove_experience'):
				working_user_gen = PossibleTextSTM.objects.all().filter(user=request.user).filter(show_user=False).filter(feed_type="user").filter(feed_id=feed_id)
				text_for_user = "This experience is enabled"
				working_experience = FeedSetting.objects.all().filter(user=request.user).filter(feed_type='user').get(feed_id=feed_id)
				number_of_experiences = FeedSetting.objects.all().filter(user=request.user).filter(feed_type='user').filter(feed_id=feed_id).count()

				user_experience = FeedSetting.objects.all().filter(feed_type="user").filter(feed_id=feed_id)
				user_texts = PossibleTextSTM.objects.all().filter(user=request.user).filter(show_user=False).filter(feed_type="user").filter(feed_id=feed_id)
				user_outgoing = ActualTextSTM.objects.all().filter(user=request.user).filter(feed_type="user").filter(feed_id=feed_id).filter(time_sent__isnull=True)

				for exp in user_experience:
					exp.delete()

				for text in user_texts:
					text.delete()

				for text in user_outgoing:
					text.delete()
				
				return HttpResponseRedirect('/ent/feeds_edit/')

			if request.GET.get('enable_experience'):
				ideal_experience = FeedSetting.objects.all().get(id=feed_id)
				print("ENABLE PRESSED")

				if FeedSetting.objects.all().filter(user=request.user).filter(feed_type='user').filter(feed_id=feed_id).count()<1:
					working_user_gen = PossibleTextSTM.objects.all().filter(show_user=False).filter(feed_type="library").filter(feed_id=feed_id)
					text_for_user = "This experience is NOT enabled"
					working_experience = FeedSetting.objects.all().get(id=feed_id)
					number_of_experiences = 0
					
					# Create and save new one
					create_new_user_experience(user=request.user,feed_id=working_experience.id,default_experience='library')
					return HttpResponseRedirect('/ent/text_set_detail/'+str(ideal_experience.id)+'/'+str(group_id))
			
				#Restore experience from defaul


			########## NOW THE FORM HANDLING STUFF
			if request.method == "POST":
				if 'submit_feed_description' in request.POST:
					if form_feed_name_new.is_valid():
						# tmp_exp = FeedSetting.objects.all().filter(experience="user").get(feed_id=ideal_experience.id)

						tmp = form_feed_name_new.save(commit=False)
						tmp.texts_per_week = tmp.texts_per_week
						tmp.text_interval_minute_avg,tmp.text_interval_minute_min,tmp.text_interval_minute_max = figure_out_timing(user=request.user,text_per_week=tmp.texts_per_week)
						tmp.save()	

					
						return HttpResponseRedirect('/ent/text_set_detail/'+str(ideal_experience.id)+'/'+str(group_id))


				if 'submit_formset' in request.POST:
					formset = UGPFormset(request.POST, queryset = working_user_gen )
					if FeedSetting.objects.all().filter(user=request.user).filter(feed_type='user').filter(feed_id=feed_id).count()<1:
						#EXPERIENCE
						tmp_exp = FeedSetting(user=request.user,user_state="disable",feed_id=ideal_experience.id,feed_type='user',description=working_experience.description,feed_name=working_experience.feed_name,texts_per_week=ideal_experience.texts_per_week)
						#gotta do the other stuff too
						tmp_exp.save()

						#INITIALIZE TEXTS
						tmp_texts = PossibleTextSTM.objects.all().filter(feed_type="library").filter(feed_id=working_experience.id)

						for text in tmp_texts:
							print("NEW TEXT SAVED")
							tmp_new = PossibleTextSTM(user=request.user,group_name=text.group_name,group_id=text.group_id,text=text.text,response_type=text.response_type,feed_id=text.feed_id,feed_name=text.feed_name,feed_type="user",text_importance=text.text_importance,date_created=text.date_created)
							tmp_new.save()


				
					print("FORMSET VALID")
					if FeedSetting.objects.all().filter(user=request.user).filter(feed_type='user').filter(description=working_experience.description).filter(feed_id=feed_id).count()<0:
						tmp_exp = FeedSetting.objects.all().filter(user=request.user).filter(feed_type='user').filter(description=working_experience.description).filter(feed_id=feed_id)
					else:
						tmp_exp = FeedSetting.objects.all().get(id=ideal_experience.id)

					#Save the Experience
					for form in formset:

						if form.is_valid() and form.has_changed():
							tmp = form.save()

							tmp.user=request.user
							tmp.feed_id=tmp_exp.id
							tmp.feed_name=tmp_exp.feed_name
							tmp.feed_type = 'user'
							# tmp.group_id=working_group.id
							# tmp.group_name=str(working_group.group_name)

							if tmp.date_created is None:
								tmp.date_created = datetime.now(pytz.utc)
							tmp.save()
							
							#Save any changes in long term storage
							ptltm = PossibleTextLTM(user=request.user,feed_name=tmp.feed_name,feed_id=tmp.id,stm_id=tmp.id,text=tmp.text,feed_type=tmp.feed_type,text_importance=tmp.text_importance,response_type=tmp.response_type,show_user=tmp.show_user,date_created=tmp.date_created,date_altered=datetime.now(pytz.utc))
							ptltm.save()

					return HttpResponseRedirect('/ent/text_set_detail/'+str(ideal_experience.id)+'/'+str(group_id))

					

				

			     
			
			context = {
				"form_feed_name_new": form_feed_name_new,
				"text_for_user": text_for_user,
				"number_of_experiences": number_of_experiences,
				"number_of_texts": number_of_texts,
				"text_per_week": text_per_week,
				"working_user_gen": working_user_gen,
				"new_user_pages": new_user_pages,
				"last_page_go_back": last_page_go_back,
				"id_group": id_group,
				"form_new_text": form_new_text,

				"helper": helper,
				"formset": formset,

				"number_of_texts": number_of_texts,

				"working_experience": working_experience,

			}
			return render(request, "text_set_detail.html", context)
	else:
		return HttpResponseRedirect('/accounts/signup/')


def feeds_edit(request):
	if request.user.is_authenticated():	
		#Create new user generated list if none
		# if FeedSetting.objects.filter(user=request.user).filter(experience='user').filter(feed_name="user generated").count()<1:
		# 	ideal_exp = FeedSetting.objects.filter(experience='library').get(feed_name="user generated")
		# 	create_new_user_experience(user=request.user,feed_id=ideal_exp.id) #FIX THIS

		#Update the tables with the right numbers of texts

		if UserSetting.objects.all().get(user=request.user).new_user_pages < 2:
			return HttpResponseRedirect('/ent/new_user/')

				
		if FeedSetting.objects.all().filter(user=request.user).count()>0:
			update_experiences(user=request.user)
		

		number_of_experiences = FeedSetting.objects.all().filter(feed_type='user').filter(group_name='basic').filter(user=request.user).count()
		working_experience_sets = FeedSetting.objects.all().filter(feed_type='user').filter(group_name='basic').filter(user=request.user)
		library_experiences = FeedSetting.objects.all().filter(feed_type='library').filter(group_name='basic').exclude(feed_name="user generated")
		number_of_texts = PossibleTextSTM.objects.all().filter(user=request.user).count()

		#Remove the experiences that have been signed up for
		number_of_texts_per_week = 0
		for exp in working_experience_sets:
			number_of_texts_per_week = number_of_texts_per_week + exp.texts_per_week
			if library_experiences.filter(feed_id=exp.feed_id).count() > 0:
				tmp_remove = library_experiences.filter(feed_type="library").get(feed_id=exp.feed_id)
				library_experiences = library_experiences.exclude(id=tmp_remove.id)


		if request.GET.get('create_new_feed'):			
			return HttpResponseRedirect('/ent/create_new_feed_page/')				

	
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

def text_set_alter(request,id=None):
	print("TEXT SET ALTER")
	print(request.META['HTTP_REFERER'])

	back_page = request.META['HTTP_REFERER']
	ideal_experience = FeedSetting.objects.all().get(id=id)
	working_settings = UserSetting.objects.all().get(user=request.user)

	if FeedSetting.objects.all().filter(user=request.user).filter(feed_type='user').filter(feed_id=id).count()<1:
		working_user_gen = PossibleTextSTM.objects.all().filter(show_user=False).filter(feed_type="library").filter(feed_id=id)
		text_for_user = "This experience is NOT enabled"
		working_experience = FeedSetting.objects.all().get(id=id)
		number_of_experiences = 0

		print("ideal_experience.texts_per_week:", ideal_experience.texts_per_week)
		tmp_exp = FeedSetting(user=request.user,user_state="disable",feed_id=ideal_experience.id,feed_type='user',description=working_experience.description,feed_name=working_experience.feed_name,texts_per_week=ideal_experience.texts_per_week)
		#gotta do the other stuff too
		tmp_exp.text_interval_minute_avg,tmp_exp.text_interval_minute_min,tmp_exp.text_interval_minute_max = figure_out_timing(user=request.user,text_per_week=tmp_exp.texts_per_week)
		tmp_exp.save()

		#INITIALIZE TEXTS
		tmp_texts = PossibleTextSTM.objects.all().filter(feed_type="library").filter(feed_id=working_experience.id)

		for text in tmp_texts:
			tmp_new = PossibleTextSTM(user=request.user,text=text.text,group_name=text.group_name,group_id=text.group_id,response_type=text.response_type,feed_id=text.feed_id,feed_name=text.feed_name,feed_type="user",text_importance=text.text_importance,date_created=text.date_created)
			tmp_new.save()

		print("enable")

		

	else:
		working_user_gen = PossibleTextSTM.objects.all().filter(user=request.user).filter(show_user=False).filter(feed_type="user").filter(feed_id=id)
		text_for_user = "This experience is enabled"
		working_experience = FeedSetting.objects.all().filter(user=request.user).filter(feed_type='user').get(feed_id=id)
		number_of_experiences = FeedSetting.objects.all().filter(user=request.user).filter(feed_type='user').filter(feed_id=id).count()

		default_texts = PossibleTextSTM.objects.all().filter(show_user=False).filter(feed_type="library").filter(feed_id=id)

		user_experience = FeedSetting.objects.all().filter(feed_type="user").filter(feed_name=ideal_experience.feed_name)
		user_texts = PossibleTextSTM.objects.all().filter(user=request.user).filter(show_user=False).filter(feed_type="user").filter(feed_id=id)
		user_outgoing = ActualTextSTM.objects.all().filter(user=request.user).filter(feed_type="user").filter(feed_id=id).filter(time_sent__isnull=True)
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
		return HttpResponseRedirect(back_page)




	
	

#User settings
def text_set(request):
	if request.user.is_authenticated():	

		form_feed_name_new= AddNewTextSetForm_full(request.POST or None)
		

		number_of_experiences = FeedSetting.objects.all().filter(feed_type='user').filter(user=request.user).exclude(feed_name="user generated").count()
		library_experiences_tmp = FeedSetting.objects.all().filter(feed_type='library')

		working_experience_sets = FeedSetting.objects.all().filter(user=request.user).exclude(feed_name="user generated").filter(feed_type='user')
		library_experiences = library_experiences_tmp | working_experience_sets


		for exp in library_experiences:
			if library_experiences.filter(feed_id=exp.feed_id).count() > 1:
				tmp_remove = library_experiences.filter(feed_type="library").get(feed_id=exp.feed_id)
				library_experiences = library_experiences.exclude(id=tmp_remove.id)


		########## NOW THE FORM HANDLING STUFF
		if request.method == "POST":
			if 'submit_new_feed_name' in request.POST:
				if form_feed_name_new.is_valid():	
					tmp = form_feed_name_new.save()
					tmp.user=request.user
					
					####   YOU WILL HAVE TO SET THE TIMING HERE							
				return HttpResponseRedirect('/ent/text_set/')

		context = {
			"number_of_experiences": number_of_experiences,
			"working_experience_sets": working_experience_sets,
			"form_feed_name_new": form_feed_name_new,
			"library_experiences": library_experiences,


		}
		return render(request, "text_set.html", context)
	else:
		return HttpResponseRedirect('/accounts/signup/')



def text_edit(request,id=None):
	if request.user.is_authenticated():	
		working_text = PossibleTextSTM.objects.all().filter(user=request.user).get(id=id)
		feed_id = working_text.feed_id
		group_id = working_text.group_id
		
		form_new_text = Edit_PossibleTextSTMForm(request.POST or None, instance=working_text)
		number_of_texts = PossibleTextSTM.objects.all().filter(user=request.user).filter(feed_type='user').count()

		
		
		if feed_id is not None:
			working_feed = FeedSetting.objects.all().filter(user=request.user).filter(feed_type='user').get(feed_id=feed_id)

		if request.method == "POST":
			if 'submit_new_text' or 'submit_finished_adding' in request.POST:
				if form_new_text.is_valid():	
					tmp = form_new_text.save()
					tmp.user=request.user
					if tmp.date_created is None:
						tmp.date_created = datetime.now(pytz.utc)
						tmp.feed_id = feed_id
						tmp.feed_type = "user"
						tmp.feed_name = working_feed.feed_name
						tmp.save()
					
					#Save any changes in long term storage
					ptltm = PossibleTextLTM(user=request.user,stm_id=tmp.id,text=tmp.text,feed_type=tmp.feed_type,text_importance=tmp.text_importance,response_type=tmp.response_type,show_user=tmp.show_user,date_created=tmp.date_created,date_altered=datetime.now(pytz.utc))
					ptltm.save()
					return HttpResponseRedirect('/ent/text_set_detail/'+str(feed_id)+'/'+str(group_id))
		

		context = {
				"feed_name": working_feed.feed_name,
				"number_of_texts": number_of_texts,
				"form_new_text": form_new_text,
				"feed_id": feed_id,
				"group_id": group_id,
			}
		
		return render(request, "add_new_texts.html", context)
	else:
		return HttpResponseRedirect('/accounts/signup/')



def add_texts(request,feed_id=None,group_id=None):
	if request.user.is_authenticated():	
		working_settings = UserSetting.objects.all().get(user=request.user)
		form_new_text = NewUser_PossibleTextSTMForm(request.POST or None)
		number_of_texts = PossibleTextSTM.objects.all().filter(user=request.user).filter(feed_type='user').filter(feed_id=feed_id).count()
		back_page = request.META['HTTP_REFERER']

		if group_id is not None and int(group_id) > 0:
			print("GROUP ID", group_id)
			working_group = GroupSetting.objects.all().filter(user=request.user).get(id=group_id)
			group_name = working_group.group_name
		else:
			group_id = 0
			group_name = "basic"
		
		if feed_id is not None:
			working_feed = FeedSetting.objects.all().filter(user=request.user).filter(feed_type='user').get(feed_id=feed_id)
			feed_name = working_feed.feed_name
		else:
			feed_id = 0
			feed_name = ""

		if request.method == "POST":
			if 'submit_new_text' or 'submit_finished_adding' in request.POST:
				if form_new_text.is_valid():	
					tmp = form_new_text.save()
					tmp.user=request.user
					if tmp.date_created is None:
						tmp.date_created = datetime.now(pytz.utc)
					tmp.feed_id = feed_id
					tmp.group_id = group_id
					tmp.group_name= group_name
					tmp.feed_type = "user"
					tmp.feed_name = feed_name
					tmp.save()
					
					#Save any changes in long term storage
					ptltm = PossibleTextLTM(user=request.user,stm_id=tmp.id,text=tmp.text,feed_type=tmp.feed_type,text_importance=tmp.text_importance,response_type=tmp.response_type,show_user=tmp.show_user,date_created=tmp.date_created,date_altered=datetime.now(pytz.utc))
					ptltm.save()

					if 'submit_new_text'in request.POST:
						return HttpResponseRedirect('/ent/add_texts/'+str(feed_id)+"/"+str(group_id))
					else:
						if working_settings.new_user_pages < 2:
							return HttpResponseRedirect('/ent/new_user/')
						else:
							return HttpResponseRedirect('/ent/text_set_detail/'+str(feed_id)+'/'+str(group_id))
				
		else:
			form_new_text = NewUser_PossibleTextSTMForm(request.POST or None)

		context = {
				"feed_name": working_feed.feed_name,
				"number_of_texts": number_of_texts,
				"form_new_text": form_new_text,
				"feed_id": feed_id,
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

		# lib_usr_tmp = FeedSetting.objects.all().filter(experience='library').get(feed_name="user generated")
		# if FeedSetting.objects.filter(user=request.user).filter(experience='user').filter(feed_id=lib_usr_tmp.id).exists():
		# 	working_experience = FeedSetting.objects.all().filter(experience='user').filter(user=request.user).get(feed_id=lib_usr_tmp.id)
		# else: 
		# 	working_experience = FeedSetting(user=request.user,experience='user',feed_name="user generated",feed_id=lib_usr_tmp.id,user_state="disable").save()
		# 	working_experience = FeedSetting.objects.all().filter(experience='user').filter(user=request.user).get(feed_id=lib_usr_tmp.id)

		if FeedSetting.objects.all().filter(user=request.user).count()>0:
			update_experiences(user=request.user)
				

		form_new_text = NewUser_PossibleTextSTMForm(request.POST or None)
		form_new_user = NewUserForm(request.POST or None, instance=working_settings)
		
		
		working_experience_sets = FeedSetting.objects.all().filter(user=request.user).filter(feed_type='user')
		library_experiences = FeedSetting.objects.all().filter(feed_type='library').filter(active=1).filter(group_id=0)
		
		number_of_experiences = FeedSetting.objects.all().filter(feed_type='user').filter(user=request.user).count()
		
		texts_per_week = working_settings.texts_per_week
		number_of_texts = PossibleTextSTM.objects.all().filter(user=request.user).filter(feed_type='user').count()

		library_experiences_tmp = FeedSetting.objects.all().filter(feed_type='library').filter(group_id=0)
		library_experiences = library_experiences_tmp | working_experience_sets

		for exp in library_experiences:
			if library_experiences.filter(feed_id=exp.feed_id).count() > 1:
				tmp_remove = library_experiences.filter(feed_type="library").get(feed_id=exp.feed_id)
				library_experiences = library_experiences.exclude(id=tmp_remove.id)


		if request.GET.get('create_new_feed'):
			return HttpResponseRedirect('/ent/create_new_feed_page/')	
			# create_new_user_experience(user=request.user,feed_id="Create New",default_experience='user')
			# ideal_experience = FeedSetting.objects.all().filter(user=request.user).filter(feed_type="user").get(feed_name="New Set")
			
			# return HttpResponseRedirect('/ent/text_set_detail/'+str(ideal_experience.id))					

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

			if 'submit_contact' in request.POST:
				print("new_user")
				if form_new_user.is_valid():
					tmp_settings = form_new_user.save(commit=False)
					tmp_settings.save()

					if "midnight" in tmp_settings.sleep_time_in:
						print("midnight")
						tmp_settings.sleep_time = datetime(2016,1,30,00,00)
					elif "noon" in tmp_settings.sleep_time_in:
						tmp_settings.sleep_time = datetime(2016,1,30,12,00)
					elif "AM" in tmp_settings.sleep_time_in:
						tmp_settings.sleep_time = datetime(2016,1,30,int(tmp_settings.sleep_time_in.split(" AM")[0]),00)
					elif "PM" in tmp_settings.sleep_time_in:
						tmp_settings.sleep_time = datetime(2016,1,30,int(tmp_settings.sleep_time_in.split(" PM")[0])+12,00)

					if "midnight" in tmp_settings.wake_time_in:
						print("midnight")
						tmp_settings.wake_time = datetime(2016,1,30,00,00)
					elif "noon" in tmp_settings.wake_time_in:
						tmp_settings.wake_time = datetime(2016,1,30,12,00)
					elif "AM" in tmp_settings.wake_time_in:
						tmp_settings.wake_time = datetime(2016,1,30,int(tmp_settings.wake_time_in.split(" AM")[0]),00)
					elif "PM" in tmp_settings.wake_time_in:
						tmp_settings.wake_time = datetime(2016,1,30,int(tmp_settings.wake_time_in.split(" PM")[0])+12,00)	

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

							schedule_greeting_text(user=request.user)
						else:
							messages.add_message(request, messages.INFO, 'Expecting a 10 digit US number!')
					
					return HttpResponseRedirect('/ent/new_user/')		


			print("NOTHING")
			return HttpResponseRedirect('/ent/new_user/')		

		if number_of_texts > 0:
			ready_to_move_on = 1
		else:
			ready_to_move_on = 0
		
		context = {
			"texts_per_week": texts_per_week,
			"number_of_texts": number_of_texts,
			"form_new_text": form_new_text,
			"library_experiences": library_experiences,
			"number_of_experiences": number_of_experiences,
			"ready_to_move_on":ready_to_move_on,
			# "user_gen_exp_id": lib_usr_tmp.id,

			
			"form_new_user": form_new_user,
			
		}
		if working_settings.new_user_pages == 0:
			return render(request, "new_user_page1.html", context)
		elif working_settings.new_user_pages == 1:
			return render(request, "new_user_page2.html", context)
		elif working_settings.new_user_pages == 2:
			return HttpResponseRedirect('/ent/simulate_week/')	
		else:
			return HttpResponseRedirect('/ent/new_user/')
	else:
		return HttpResponseRedirect('/accounts/signup/')


def texter(request):
	if request.user.is_authenticated():	

		#Create the Text
		if request.GET.get('create_unsent_text'):
			print("Creating Unsent Texts")
			text_new = ActualTextSTM(user=request.user, response=None,simulated=0,feed_type="user")
			text_new.text, text_new.text_id = set_next_prompt(user=text_new.user,feed_type="user")
			text_new.text, text_new.response_type = determine_prompt_texts(user=request.user,prompt=text_new.text,typer=text_new.feed_type)
			text_new.time_to_send = set_prompt_time(text=text_new,send_now=1)
			text_new.save()
			
			return HttpResponseRedirect('/ent/texter/')
			
		# Send the text	

		if request.GET.get('create_rando_generated'):
			print("button pressed . sending texts")
			generate_random_prompts_to_show_no_sim(request,exp_resp_rate=.8,week=0,number_of_prompts=100) #set up 20 random prompts based upon the settings
			return HttpResponseRedirect('/ent/texter/')



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

		
		
		form_free = ContactSettingsForm(request.POST or None, instance=working_settings)
		
		
		
		

		########## NOW THE FORM HANDLING STUFF
		if request.method == "POST":
			if 'submit_contact' in request.POST:
				if form_free.is_valid():
					tmp_settings = form_free.save(commit=False)
					print("SLEEP", tmp_settings.sleep_time_in)
					print("Contact Valid")
					messages.add_message(request, messages.INFO, 'Form Saved!')
					if "midnight" in tmp_settings.sleep_time_in:
						print("midnight")
						tmp_settings.sleep_time = datetime(2016,1,30,00,00)
					elif "noon" in tmp_settings.sleep_time_in:
						tmp_settings.sleep_time = datetime(2016,1,30,12,00)
					elif "AM" in tmp_settings.sleep_time_in:
						tmp_settings.sleep_time = datetime(2016,1,30,int(tmp_settings.sleep_time_in.split(" AM")[0]),00)
					elif "PM" in tmp_settings.sleep_time_in:
						tmp_settings.sleep_time = datetime(2016,1,30,int(tmp_settings.sleep_time_in.split(" PM")[0])+12,00)

					if "midnight" in tmp_settings.wake_time_in:
						print("midnight")
						tmp_settings.wake_time = datetime(2016,1,30,00,00)
					elif "noon" in tmp_settings.wake_time_in:
						tmp_settings.wake_time = datetime(2016,1,30,12,00)
					elif "AM" in tmp_settings.wake_time_in:
						tmp_settings.wake_time = datetime(2016,1,30,int(tmp_settings.wake_time_in.split(" AM")[0]),00)
					elif "PM" in tmp_settings.wake_time_in:
						tmp_settings.wake_time = datetime(2016,1,30,int(tmp_settings.wake_time_in.split(" PM")[0])+12,00)	
						
						

						





					# sleep_time = models.TimeField(default=datetime(2016,1,30,22,00)) #This is the time the user sleeps.  Used to calculate deadtimes
					# wake_time = models.TimeField(default=datetime(2016,1,30,22,00))

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
	if PossibleTextSTM.objects.all().filter(user=user).filter(feed_type="research").count() > 0 :
		rtexts = PossibleTextSTM.objects.all().filter(user=user).filter(feed_type="research")
		for rtext in rtexts:
			rtext.delete()

	rtexts = PossibleTextSTM.objects.all().filter(feed_type="research").filter(system_text=2)
	for rtext in rtexts:
		tmp = PossibleTextSTM(user=user,feed_type="research",feed_name="research",text=rtext.text,text_importance=rtext.text_importance)
		tmp.save()







def simulate_week(request):
	if request.user.is_authenticated():	
		if  UserSetting.objects.filter(user=request.user).exists():
			working_settings = UserSetting.objects.all().get(user=request.user)
		else: 
			working_settings = UserSetting(user=request.user,begin_date=datetime.now(pytz.utc)).save()
			working_settings = UserSetting.objects.all().get(user=request.user)


		# if FeedSetting.objects.filter(user=request.user).filter(experience='user').filter(feed_name="user generated").count()>0:
		# 	working_experience = FeedSetting.objects.all().filter(experience='user').filter(user=request.user).filter(feed_name="user generated").first()
		# else: 
		# 	working_experience = FeedSetting(user=request.user,experience='user',feed_name="user generated").save()
		# 	working_experience = FeedSetting.objects.all().filter(experience='user').filter(user=request.user).filter(feed_name="user generated").first()

		update_experiences(user=request.user)

		

		
		
		generate_random_prompts_to_show(request,exp_resp_rate=.6,week=1,number_of_prompts=0) #set up 20 random prompts based upon the settings
		graph_data_simulated_heatmap = get_graph_data_simulated_heatmap(request)
		texts_per_week = working_settings.texts_per_week

		actual_number_texts = ActualTextSTM_SIM.objects.all().filter(user=request.user).count()

		feed_names = FeedSetting.objects.all().exclude(feed_type='library').filter(user=request.user).values('feed_name').distinct()

		total_expected_number = 0
		working_experience_sets = FeedSetting.objects.all().filter(user=request.user).exclude(feed_type='library').filter(texts_per_week__gt = 0).filter(number_of_texts_in_set__gt = 0)

		count_out = []
		exp_out = []
		list_out = []
		for exp in working_experience_sets:
			total_expected_number = int(exp.texts_per_week) + total_expected_number
			exp_out.append(int(exp.texts_per_week))
			count_out.append(int(ActualTextSTM_SIM.objects.all().filter(user=request.user).filter(feed_name=exp.feed_name).count()))
			list_out.append({"name":exp.feed_name,"expected":int(exp.texts_per_week),"feed_id":exp.feed_id,"observed":int(ActualTextSTM_SIM.objects.all().filter(user=request.user).filter(feed_name=exp.feed_name).count())})
			# print("total_expected_number",total_expected_number )

		print("total_expected_number",total_expected_number)

		

		# print(FeedSetting.objects.all().filter(experience='user').filter(user=request.user).values('feed_name').distinct().aggregate("Count"))





		context = {
			"texts_per_week": texts_per_week,
			"actual_number_texts": actual_number_texts,
			"feed_names": feed_names,
			"total_expected_number": total_expected_number,
			"count_out": count_out,
			"exp_out": exp_out,
			"list_out": list_out,

			"graph_data_simulated_heatmap": graph_data_simulated_heatmap,
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
