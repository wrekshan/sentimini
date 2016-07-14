from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from datetime import datetime, timedelta
from django.forms import modelformset_factory
import pytz

# Create your views here.
from .forms import  UserSettingForm_Prompt, UserGenPromptForm, UserSettingForm_PromptRate, ExampleFormSetHelper, UserSettingForm_Prompt_Paid
from .models import Emotion, Entry, UserSetting, Carrier, Respite, UserGenPrompt


#This is the main view to edit the user generated prompts
def edit_user_gen_prompt_settings(request):
	if request.user.is_authenticated():	
		if  UserSetting.objects.all().filter(user=request.user).exists():
			working_settings = UserSetting.objects.all().get(user=request.user)
		else: 
			working_settings = UserSetting(user=request.user).save()

		if UserGenPrompt.objects.filter(user=request.user).count()>0:
			working_user_gen = UserGenPrompt.objects.all().filter(user=request.user).filter(show_user=False)
		else:
			working_user_gen = UserGenPrompt(user=request.user).save()
	
		UGPFormset = modelformset_factory(UserGenPrompt, form = UserGenPromptForm, extra=1)
		prompt_rate_form = UserSettingForm_PromptRate(request.POST or None, instance=working_settings)
		helper = ExampleFormSetHelper()
		
		if request.method == "POST":
			print("FORM SET STUFF")
			#do the formset stuff
			formset = UGPFormset(request.POST, queryset = working_user_gen )
			

			if formset.is_valid and prompt_rate_form.is_valid():
				messages.add_message(request, messages.INFO, 'User prompt settings changed!')			
				for form in formset:
					if form.has_changed():
						tmp = form.save(commit=False)
						tmp.user = request.user
						tmp.date_create = datetime.now(pytz.utc)
						tmp.save()

				tmp = prompt_rate_form.save(commit=False)
				working_settings.user_generated_prompt_rate = tmp.user_generated_prompt_rate
				working_settings.save()

				return HttpResponseRedirect(reverse('ent:edit_user_gen_prompt_settings'))
			else:
				context = {
					"helper": helper,
					"prompt_rate_form": prompt_rate_form, 
					"query_results": working_user_gen,
					"formset": formset,
				}
				return render(request, "edit_user_gen_prompts.html", context)
		else:
			formset = UGPFormset(queryset = working_user_gen)
			context = {
				"helper": helper,
				"prompt_rate_form": prompt_rate_form, 
				"query_results": working_user_gen,
				"formset": formset,
			}
			return render(request, "edit_user_gen_prompts.html", context)
	else:
		return render(request, "index_not_logged_in.html")

#User settings
def edit_prompt_settings(request):
	if request.user.is_authenticated():	
		if  UserSetting.objects.filter(user=request.user).exists():
			working_settings = UserSetting.objects.all().get(user=request.user)
			intro_text = "Welcome " + str(request.user) + "!"
		else: 
			working_settings = UserSetting(user=request.user).save()
			intro_text = "Welcome " + str(request.user) + "!"

		if UserGenPrompt.objects.filter(user=request.user).count()>0:
			working_user_gen = UserGenPrompt.objects.all().filter(user=request.user).filter(show_user=False)
		else:
			working_user_gen = UserGenPrompt(user=request.user).save()

		form_free = UserSettingForm_Prompt(request.POST or None, instance=working_settings)
		form_paid = UserSettingForm_Prompt_Paid(request.POST or None, instance=working_settings)
		UGPFormset = modelformset_factory(UserGenPrompt, form = UserGenPromptForm, extra=1)
		form_prompt_percent = UserSettingForm_PromptRate(request.POST or None, instance=working_settings)
		formset = UGPFormset(queryset = working_user_gen)
		helper = ExampleFormSetHelper()


		if request.method == "POST":
			formset = UGPFormset(request.POST, queryset = working_user_gen )
			if 'submit_formset' in request.POST:
				if formset.is_valid:
					print("FORMSET VALID")
					messages.add_message(request, messages.INFO, 'User prompt settings changed!')			
					for form in formset:
						print("FORMSET LOOP")
						if form.has_changed():
							print("FORMSET CHANGED")
							tmp = form.save(commit=False)
							tmp.user = request.user
							tmp.date_create = datetime.now(pytz.utc)
							tmp.save()
					working_settings.save()
				return HttpResponseRedirect('/ent/edit_prompt_settings/#usergen')	

			elif 'submit_paid' in request.POST:
				print("SUBMIT PAID")
				if form_paid.is_valid():
					print("SUBMIT PAID VALID")
					tmp_settings = form_paid.save(commit=False)
					min_awake = (24 - tmp_settings.sleep_duration)*60
					tmp_settings.prompt_interval_minute_avg = min_awake / tmp_settings.prompts_per_day #used in the random draw for the number of minutes to next prompt
					tmp_settings.save()
					messages.add_message(request, messages.INFO, 'Paid Settings Changed')
					return HttpResponseRedirect('/ent/edit_prompt_settings/#paid')		

			elif 'submit_unpaid' in request.POST:
				print("SUBMIT UNPAID")
				if form_free.is_valid():
					print("SUBMIT UNPAID VALID")
					tmp_settings = form_free.save(commit=False)
					tmp_settings.send_text = bool(True)	#just a switch to say the person can be texted
					tmp_settings.sms_address =  tmp_settings.phone + str(carrier_lookup(tmp_settings.carrier)) #Figures otu the address the promtps need to be sent to
					tmp_settings.respite_until_datetime = datetime.now(pytz.utc) #initializes the respite until date (this actually just needs to be set because it does a greater than check)
					tmp_settings.save()
					messages.add_message(request, messages.INFO, 'Unpaid Settings Changed')		
					return HttpResponseRedirect('/ent/edit_prompt_settings/#free')		

			elif 'submit_prompt_percent' in request.POST:
				print("PROMPT PERCENT PAID")
				if form_prompt_percent.is_valid():
					print("SUBMIT PAID VALID")
					tmp_settings = form_prompt_percent.save(commit=False)
					min_awake = (24 - tmp_settings.sleep_duration)*60
					tmp_settings.prompt_interval_minute_avg = min_awake / tmp_settings.prompts_per_day #used in the random draw for the number of minutes to next prompt
					tmp_settings.save()
					messages.add_message(request, messages.INFO, 'Paid usergen Changed')
					return HttpResponseRedirect('/ent/edit_prompt_settings/#paid')		
				
		else:
			print("ELSE")
			form_free = UserSettingForm_Prompt(request.POST or None, instance=UserSetting.objects.all().get(user=request.user))
			form_paid = UserSettingForm_Prompt_Paid(request.POST or None, instance=UserSetting.objects.all().get(user=request.user))
			form_prompt_percent = UserSettingForm_PromptRate(request.POST or None, instance=working_settings)
			UGPFormset = modelformset_factory(UserGenPrompt, form = UserGenPromptForm, extra=1)
			formset = UGPFormset(queryset = working_user_gen)
			context = {
				"helper": helper,
				"form_prompt_percent": form_prompt_percent, 
				"intro_text": intro_text,
				"form_free": form_free,
				"form_paid": form_paid,
				"form_prompt_percent": form_prompt_percent,
				"formset": formset,
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
