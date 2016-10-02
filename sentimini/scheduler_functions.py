from datetime import date, datetime, timedelta
from random import random, triangular, randint
from django.db.models import Avg, Count, F, Case, When
from random import shuffle
import pytz

import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse

from ent.models import UserSetting, PossibleTextSTM, ActualTextSTM, ActualTextLTM, Ontology, Prompttext, UserGenPromptFixed, ExperienceSetting
import plotly.offline as opy
import plotly.graph_objs as go
from numpy import * 

from sentimini.tasks import send_texts, schedule_texts, set_next_prompt, determine_prompt_texts, set_prompt_time


def generate_random_prompts_to_show(request,exp_resp_rate,week,number_of_prompts):
	working_settings = UserSetting.objects.all().get(user=request.user)
	experience_settings = ExperienceSetting.objects.all().filter(experience="user").get(user=request.user)
	research_settings = ExperienceSetting.objects.all().filter(experience="research").get(user=request.user)
	
	#Generate 100 prompts
	if ActualTextSTM.objects.all().filter(user=request.user).filter(simulated=1).count()>0:
		ActualTextSTM.objects.all().filter(user=request.user).filter(simulated=1).delete()

	if ActualTextLTM.objects.all().filter(user=request.user).filter(simulated=1).count()>0:
		ActualTextLTM.objects.all().filter(user=request.user).filter(simulated=1).delete()
	
	#Just set up the starting date
	tmp_date = datetime.now()
	local_tz = pytz.timezone('UTC')
	local_tz = local_tz.localize(tmp_date)
	tmp_date = local_tz.astimezone(pytz.UTC)

	#go trhough and generate 100 or whatevs
	start_date = tmp_date
	latest_date = tmp_date
	time_passed = latest_date - start_date

	if week == 1:
		while (time_passed.days) < 8:	
			# print ("STARTING NEW ENTRY")	
			#Set up the basic for the prompt
			text_new = ActualTextSTM(user=request.user, response=None,simulated=1)
			text_new.text, text_new.text_id = set_next_prompt(user=text_new.user,text_type="user")
			text_new.text, text_new.response_type = determine_prompt_texts(user=request.user,prompt=text_new.text,typer=text_new.text_type)

			# print("working_entry_new.text",working_entry_new.text)
			
			#See if it is part of a series
	
			if ActualTextSTM.objects.all().filter(user=request.user).filter(simulated=1).count()>1:
				working_entry_last = ActualTextSTM.objects.all().filter(user=request.user).last()
				if text_new.text_type == "research":
					text_new.series = determine_next_prompt_series(user=text_new.user)
				else:
					text_new.series = 0

				if text_new.series > 1:
					text_new.time_to_add = 0

				if text_new.series > 1 and not working_entry_last.response == None:
					text_new.response = randint(1,10)
					text_new.response_time = 0
					
			text_new.time_to_add, text_new.time_to_send = set_prompt_time(text=text_new,send_now=0,fake_time_now=tmp_date)
			text_new.time_sent = text_new.time_to_send

			#Figure out the response
			if text_new.series < 2:
				tmp = randint(1,100)

				if tmp <= (exp_resp_rate*100):
					text_new.response_time = next_response_minutes(user=text_new.user)
					if text_new.response_type == '0 to 10':
						text_new.response = randint(1,10)
					else:
						text_new.response = randint(1,2)-1

				else:
					text_new.response_time = 0

			tmp_date = text_new.time_to_send + timedelta(hours=0,minutes=text_new.response_time,seconds=0)
			text_new.save()
			wen=text_new

			ltm = ActualTextLTM(user=wen.user,response=wen.response,text_id=wen.text_id,text=wen.text,time_to_add=wen.time_to_add,text_type=wen.text_type,response_type=wen.response_type,time_response=wen.time_response,time_to_send=wen.time_to_send,time_sent=wen.time_sent,simulated=wen.simulated)
			if ltm.response_type == '0 to 10':
				if ltm.response != "":
					ltm.response_dim = ltm.response
			else:
				if ltm.response != "":
					ltm.response_cat = str(ltm.response)
					ltm.response_cat_bin = ltm.response

					

			if wen.time_to_send.hour > 12:
				ltm.time_to_send_circa = 'PM'
			ltm.time_to_send_day = wen.time_to_send.strftime('%A')

			ltm.response_cat=0
			ltm.response=wen.response
			ltm.response_dim=wen.response
			ltm.response_cat=wen.response_time
			ltm.save()


			#figure out conditions to stop
			latest_date = text_new.time_to_send
			time_passed = latest_date - start_date
	else:
		for i in range(0,number_of_prompts):	
			
			#Set up the basic for the prompt
			text_new = ActualTextSTM(user=request.user,ready_for_next = False, response=None,simulated=1)
			text_new.text, text_new.text_id = set_next_prompt(user=text_new.user,text_type="user")
			text_new.text, text_new.response_type = determine_prompt_texts(user=request.user,prompt=text_new.text,typer=text_new.text_type)
			# print("LOOK HERE")
			# print(working_entry_new.prompt.id)

			#See if it is part of a series
			text_new.time_to_add = next_prompt_minutes(user=text_new.user,simulation_val=1,send_now=0)

			if ActualTextSTM.objects.all().filter(user=request.user).filter(simulated=1).count()>1:
				working_entry_last = ActualTextSTM.objects.all().filter(user=request.user).last()
				if text_new.text_type == "research":
					text_new.series = determine_next_prompt_series(user=text_new.user)
				else: 
					text_new.series =0

				if text_new.series > 1:
					text_new.time_to_add = 0

				if text_new.series > 1 and not working_entry_last.response == None:
					text_new.response = randint(1,10)
					text_new.response_time = 0
					
					
			#compute the actual times
			
			text_new.time_to_add, text_new.time_to_send = set_prompt_time(text=text_new,send_now=0,fake_time_now=tmp_date)


			
			text_new.time_sent = text_new.time_to_send
			

			#Figure out the response
			if text_new.series < 2:
				tmp = randint(1,100)

				if tmp <= (exp_resp_rate*100):
					text_new.response_time = next_response_minutes(user=text_new.user)
					if text_new.response_type == '0 to 10':
						text_new.response = randint(1,10)
					else:
						text_new.response = randint(1,2)-1
				else:
					text_new.reponse_time = 0


			tmp_date = text_new.time_to_send + timedelta(hours=0,minutes=text_new.response_time,seconds=0)
			text_new.save()

			wen=text_new


			ltm = ActualTextLTM(user=wen.user,response=wen.response,text_id=wen.text_id,text=wen.text,text_type=wen.text_type,response_type=wen.response_type,time_response=wen.time_response,time_to_send=wen.time_to_send,time_sent=wen.time_sent,simulated=wen.simulated)
			if ltm.response_type == '0 to 10':
				if ltm.response != "":
					ltm.response_dim = ltm.response
			else:
				if ltm.response != "":
					ltm.response_cat = str(ltm.response)
					ltm.response_cat_bin = ltm.response

			# print("wen.time_to_send.day",wen.time_to_send.day)
			if wen.time_to_send.hour > 12:
				ltm.time_to_send_circa = 'PM'
			ltm.time_to_send_day = wen.time_to_send.strftime('%A')
			ltm.response=wen.response
			ltm.save()






	

def determine_next_prompt_series(user):
	#Check to see if last prompt was part of the series
	working_entry_last = ActualTextSTM.objects.all().filter(user=user).filter(simulated=1).last()
	
	#not a failed series last prompt
	series_num = 0

	if working_entry_last.failed_series == 0:
		if working_entry_last.series == 0:
			series_num = 1
		else:
			series_num = 0

		if working_entry_last.series == 1:
			series_num = 2

		if working_entry_last.series == 2:
			series_num = 3
	else:
		if tmp <= series_max:
			series_num = 1

	
	return series_num




#This sets the number of minutes - this is crazy right now, please fix
def next_prompt_minutes(user,simulation_val,send_now):
	working_settings = UserSetting.objects.all().get(user=user)
	experience_settings = ExperienceSetting.objects.all().filter(user=user).get(experience="user")
	
	#get the time anchor.
	if ActualTextSTM.objects.all().filter(user=user).filter(simulated=simulation_val).order_by('time_sent').count() < 1:
		if simulation_val < 1:
			time_anchor = datetime.now()
		else: 
			time_anchor = datetime.now()
	else:
		if simulation_val < 1:
			time_anchor = datetime.now()
		else:
			time_anchor_tmp = ActualTextSTM.objects.all().filter(user=user).filter(simulated=simulation_val).order_by('-time_sent').first()
			time_anchor = time_anchor_tmp.time_sent

	# print("TIME ANCHOR: ", time_anchor)
	if send_now == 1:
		time_away_minutes = 0
	else:
		time_away_minutes = int(triangular(experience_settings.prompt_interval_minute_min, experience_settings.prompt_interval_minute_max, experience_settings.prompt_interval_minute_avg)) 
	
	############ YOU HAVE TO DO THIS BASED UPON TIME AND NOT THE DATE.  THIS IS BECAUSE THERE COULD BE PROMPTS FOR LIKE FOUR DAYS FROM NOW.
	local_tz = pytz.timezone(working_settings.timezone)
	local_sleep_time = local_tz.localize(datetime.combine(time_anchor.date(),working_settings.sleep_time))
	local_wake_time = local_sleep_time + timedelta(0,60*60*int(working_settings.sleep_duration))

	utc_sleep_time = local_sleep_time.astimezone(pytz.UTC)
	utc_wake_time = local_wake_time.astimezone(pytz.UTC)
	
	proposed_next_prompt_time = time_anchor + timedelta(hours=0,minutes=time_away_minutes,seconds=0)


	if utc_sleep_time.time() <= proposed_next_prompt_time.time() <= utc_wake_time.time():

		wake_tmp = datetime.strptime(str(utc_wake_time.time()), '%H:%M:%S')
		sleep_tmp = datetime.strptime(str(utc_sleep_time.time()), '%H:%M:%S')
		next_tmp = datetime.strptime(str(proposed_next_prompt_time.time()), '%H:%M:%S.%f')

		additional_minutes = (wake_tmp - next_tmp) + (next_tmp - sleep_tmp)

		time_away_minutes = time_away_minutes + (additional_minutes.seconds/60)
		proposed_next_prompt_time_revised = time_anchor + timedelta(hours=0,minutes=time_away_minutes,seconds=0)

	return time_away_minutes	



def next_response_minutes(user):
	working_settings = UserSetting.objects.all().get(user=user)
	time_away_minutes = int(triangular(working_settings.exp_response_time_min, working_settings.exp_response_time_max, working_settings.exp_response_time_avg)) #please note, that you'll want to change this.  it'll probs be some other distro, but this is just easy peasy for now.#low, high, mode
	return time_away_minutes	