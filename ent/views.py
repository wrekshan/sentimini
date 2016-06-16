from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from datetime import datetime, timedelta
from django.forms import modelformset_factory
import pytz

# Create your views here.
# from .forms import  UserSettingForm_Prompt, UserGenPromptForm
# from .models import Emotion, Entry, UserSetting, Carrier, Respite, UserGenPrompt


# #This is the main view to edit the user generated prompts
# def edit_user_gen_prompt_settings(request):
# 	if request.user.is_authenticated():	
# 		if  UserSetting.objects.all().filter(user=request.user).exists():
# 			working_settings = UserSetting.objects.all().get(user=request.user)
# 		else: 
# 			working_settings = UserSetting(user=request.user).save()

# 		if UserGenPrompt.objects.filter(user=request.user).count()>0:
# 			working_user_gen = UserGenPrompt.objects.all().filter(user=request.user).filter(show_user=True)
# 		else:
# 			working_user_gen = UserGenPrompt(user=request.user).save()
	
# 		UGPFormset = modelformset_factory(UserGenPrompt, fields=('prompt', 'active', 'show_user'),extra=1)

		
# 		if request.method == "POST":
# 			formset = UGPFormset(request.POST, queryset = working_user_gen )
# 			if formset.is_valid():
# 				messages.add_message(request, messages.INFO, 'User Prompts Changed')			
# 				for form in formset:
# 					if form.has_changed():
# 						tmp = form.save(commit=False)
# 						tmp.user = request.user
# 						tmp.date_create = datetime.now(pytz.utc)
# 						tmp.save()
# 				return HttpResponseRedirect(reverse('ent:edit_user_gen_prompt_settings'))
# 			else:
# 				context = {
# 					"query_results": working_user_gen,
# 					"formset": formset,
# 				}
# 			return render(request, "edit_user_gen_prompts.html", context)
# 		else:
# 			formset = UGPFormset(queryset = working_user_gen)
# 			context = {
# 				"query_results": working_user_gen,
# 				"formset": formset,
# 			}
# 			return render(request, "edit_user_gen_prompts.html", context)
# 	else:
# 		return render(request, "index_not_logged_in.html")

# #User settings
# def edit_prompt_settings(request):
# 	if request.user.is_authenticated():	
# 		if  UserSetting.objects.filter(user=request.user).exists():
# 			working_settings = UserSetting.objects.all().get(user=request.user)
# 			intro_text = "Welcome back " + str(request.user) + "!  Please make sure this is all correct."
# 		else: 
# 			working_settings = UserSetting(user=request.user).save()
# 			intro_text = "Welcome back " + str(request.user) + "!  Please just fill out this form.  You'll have to complete the full form for this to begin working."

# 		form = UserSettingForm_Prompt(request.POST or None, instance=working_settings)
		
# 		if form.is_valid():
# 			working_settings = form.save(commit=False)
# 			min_awake = (24 - working_settings.sleep_duration)*60
# 			working_settings.prompt_interval_minute_avg = min_awake / working_settings.prompts_per_day #used in the random draw for the number of minutes to next prompt
# 			working_settings.send_text = bool(True)	#just a switch to say the person can be texted
# 			working_settings.sms_address =  working_settings.phone + str(carrier_lookup(working_settings.carrier)) #Figures otu the address the promtps need to be sent to
# 			working_settings.respite_until_datetime = datetime.now(pytz.utc) #initializes the respite until date (this actually just needs to be set because it does a greater than check)
# 			working_settings.save()

# 			messages.add_message(request, messages.INFO, 'Prompt Settings Changed')			
# 			context = {
# 				"intro_text": intro_text,
# 				"form": form,
# 		} 
# 		else:
# 			context = {
# 				"intro_text": intro_text,
# 				"form": form,
# 			}
# 		return render(request, "create_user_settings_form.html", context)
# 	else:
# 		return render(request, "index_not_logged_in.html")


# ##########################################################
# ##### HERE ARE THINGS YOU HAVE TO HAVE
# ##########################################################
# #This creates a entry for the settings file for the people.  Right now it just displays the things a user would want to change.  I've tried to add in some adaptive flexibility, but right now it is just a place holder
# def carrier_lookup(carrier):
# 	return Carrier.objects.all().get(carrier=carrier).sms_address

# def respite_one_day(request):
# 	working_settings = UserSetting.objects.all().get(user=request.user)
# 	today_date = datetime.now(pytz.utc)
# 	working_settings.respite_until_datetime = today_date + timedelta(1,0)
# 	working_settings.save()

# 	Respite(user=request.user,respite_type='1 day',date_request=today_date).save()
# 	messages.add_message(request, messages.INFO, 'No prompts will be sent for 1 day')
# 	return redirect(request.META['HTTP_REFERER'])

# def respite_three_day(request):
# 	working_settings = UserSetting.objects.all().get(user=request.user)
# 	today_date = datetime.now(pytz.utc)
# 	working_settings.respite_until_datetime = today_date + timedelta(3,0)
# 	working_settings.save()

# 	Respite(user=request.user,respite_type='3 day',date_request=today_date).save()
# 	messages.add_message(request, messages.INFO, 'No prompts will be sent for 3 days')
# 	return redirect(request.META['HTTP_REFERER'])

# def respite_seven_day(request):
# 	working_settings = UserSetting.objects.all().get(user=request.user)
# 	today_date = datetime.now(pytz.utc)
# 	working_settings.respite_until_datetime = today_date + timedelta(7,0)
# 	working_settings.save()

# 	Respite(user=request.user,respite_type='7 day',date_request=today_date).save()
# 	messages.add_message(request, messages.INFO, 'No prompts will be sent for 7 days')
# 	return redirect(request.META['HTTP_REFERER'])

# def respite_start_again(request):
# 	working_settings = UserSetting.objects.all().get(user=request.user)
# 	today_date = datetime.now(pytz.utc)
# 	working_settings.respite_until_datetime = today_date  
# 	tmp_msg = "Starting again"
	
# 	working_settings.text_request_stop = bool('False')
# 	working_settings.save()
# 	Respite(user=request.user,respite_type='start_again',date_request=today_date).save()
# 	messages.add_message(request, messages.INFO, 'Starting prompts again')
# 	return redirect(request.META['HTTP_REFERER'])
