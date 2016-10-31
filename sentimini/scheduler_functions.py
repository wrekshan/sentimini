from datetime import date, datetime, timedelta
from random import random, triangular, randint, gauss
from django.db.models import Avg, Count, F, Case, When
from random import shuffle
import pytz

import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse

from ent.models import UserSetting, PossibleTextSTM, ActualTextSTM, ActualTextLTM, Ontology, Prompttext, UserGenPromptFixed, FeedSetting, ActualTextSTM_SIM
# from ent.views import update_experiences

import plotly.offline as opy
import plotly.graph_objs as go
from numpy import * 

from sentimini.tasks import send_texts, schedule_texts, set_next_prompt, determine_prompt_texts, set_prompt_time




def add_new_simulated_text(user,exp,tmp_date,exp_resp_rate):
	text_new = ActualTextSTM_SIM(user=user,response=None,feed_name=exp.feed_name,simulated=1,feed_id=exp.feed_id)

	# print(text_new.text)	
	text_new.text, text_new.text_id = set_next_prompt(text=text_new)
	text_new.text, text_new.response_type = determine_prompt_texts(text=text_new)


	if ActualTextSTM.objects.all().filter(user=user).filter(simulated=1).count()>1:
		working_entry_last = ActualTextSTM.objects.all().filter(user=user).last()
		if text_new.feed_type == "research":
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

	# text_new.response_time = randint(1,100)

	tmp_date = text_new.time_to_send + timedelta(hours=0,minutes=text_new.response_time,seconds=0)

	wen=text_new
	ltm = ActualTextLTM(user=wen.user,response=wen.response,feed_name=wen.feed_name,text_id=wen.text_id,text=wen.text,time_to_add=wen.time_to_add,feed_type=wen.feed_type,response_type=wen.response_type,time_response=wen.time_response,time_to_send=wen.time_to_send,time_sent=wen.time_sent,simulated=wen.simulated)
	if ltm.response_type == '0 to 10':
		if ltm.response != "":
			ltm.response_dim = ltm.response

			ltm.response_cat = randint(1,2)-1
			ltm.response_cat_bin = ltm.response_cat

			
	else:
		if ltm.response != "":
			ltm.response_cat = str(ltm.response)
			ltm.response_cat_bin = ltm.response

			

	if wen.time_to_send.hour > 12:
		ltm.time_to_send_circa = 'PM'
	ltm.time_to_send_day = wen.time_to_send.strftime('%A')

	# ltm.response_cat=0
	# ltm.response=wen.response
	# ltm.response_dim=wen.response
	ltm.response_time=wen.response_time
	ltm.save()
	text_new.save()

	return text_new


def generate_random_prompts_to_show(request,exp_resp_rate,week,number_of_prompts):
	working_settings = UserSetting.objects.all().get(user=request.user)
	# experience_settings = FeedSetting.objects.all().filter(text_type="user").filter(text_set="user generated").filter(active=1).get(user=request.user)
	
	#Generate 100 prompts
	if ActualTextSTM_SIM.objects.all().filter(user=request.user).count()>0:
		ActualTextSTM_SIM.objects.all().filter(user=request.user).delete()

	#Just set up the starting date
	tmp_date = datetime.now()
	local_tz = pytz.timezone('UTC')
	local_tz = local_tz.localize(tmp_date)
	tmp_date = local_tz.astimezone(pytz.UTC)


	working_experience = FeedSetting.objects.all().filter(user=request.user).filter(feed_type="user").filter(texts_per_week__gt = 0).filter(number_of_texts_in_set__gt = 0)

	print("NUMBER OF EXPERIENCES:", working_experience.count())
	for exp_name in working_experience:
		tmp_date = datetime.now(pytz.UTC)
		exp = FeedSetting.objects.all().exclude(feed_type="library").filter(feed_id=exp_name.feed_id).get(user=request.user)
		#go trhough and generate 100 or whatevs
		start_date = tmp_date
		latest_date = tmp_date
		time_passed = latest_date - start_date
		
		if week > 0:
			# print("WEEK STARTED")
			while (time_passed.days) < 8:
				text_new = add_new_simulated_text(user=request.user,exp=exp,tmp_date=tmp_date,exp_resp_rate=exp_resp_rate)
				#figure out conditions to stop
				tmp_date = text_new.time_to_send

				latest_date = text_new.time_to_send
				time_passed = latest_date - start_date
				# print("time_passed.days", time_passed.days)
		else:
			for i in range(0,number_of_prompts):
				text_new = add_new_simulated_text(user=request.user,exp=exp,tmp_date=tmp_date,exp_resp_rate=exp_resp_rate)
				#figure out conditions to stop
				tmp_date = text_new.time_to_send
				
				latest_date = text_new.time_to_send
				time_passed = latest_date - start_date
				# print("time_passed.days", time_passed.days)
			
			


def figure_out_timing(user,text_per_week):
	tmp_settings = UserSetting.objects.all().get(user=user)

	local_tz = pytz.timezone(tmp_settings.timezone)
	sleep = local_tz.localize(datetime.combine(datetime.now().date(),tmp_settings.sleep_time))
	wake = local_tz.localize(datetime.combine(datetime.now().date(),tmp_settings.wake_time))

	td = wake - sleep
	tmp_settings.sleep_duration = int(td.seconds/60/60)
	tmp_settings.save()
	print("SLEEP DURATION:",tmp_settings.sleep_duration)

	if text_per_week > 0:
		min_awake = (24 - tmp_settings.sleep_duration)*60
		average = ((24 - tmp_settings.sleep_duration)*60) / (text_per_week/7) #used in the random draw for the number of minutes to next prompt
		if text_per_week <= 30:
			minumum =  average*.01
			maximium =  average*10
		elif text_per_week > 30 and text_per_week <= 60:
			minumum =  average*.01
			maximium =  average*10
		elif text_per_week > 60:
			minumum =  average*.01
			maximium =  average*10		

	else:
		average = 0
		minumum =  0
		maximium =  0

	return average, minumum, maximium



	

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
	experience_settings = FeedSetting.objects.all().filter(user=user).get(experience="user")
	
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
		# time_away_minutes = int(triangular(experience_settings.text_interval_minute_min, experience_settings.text_interval_minute_max, experience_settings.text_interval_minute_avg)) 
		time_away_minutes = generate_random_minutes(experience_settings)

		
	
	############ YOU HAVE TO DO THIS BASED UPON TIME AND NOT THE DATE.  THIS IS BECAUSE THERE COULD BE PROMPTS FOR LIKE FOUR DAYS FROM NOW.
	local_tz = pytz.timezone(working_settings.timezone)
	local_sleep_time = local_tz.localize(datetime.combine(time_anchor.date(),working_settings.sleep_time))
	local_wake_time = local_tz.localize(datetime.combine(time_anchor.date(),working_settings.wake_time))
	# local_wake_time = local_sleep_time + timedelta(0,60*60*int(working_settings.sleep_duration))

	utc_sleep_time = local_sleep_time.astimezone(pytz.UTC)
	utc_wake_time = local_wake_time.astimezone(pytz.UTC)
	
	proposed_next_prompt_time = time_anchor + timedelta(hours=0,minutes=time_away_minutes,seconds=0)

	print("SLEEP:    ", utc_sleep_time)
	print("WAKE:     ",  utc_wake_time)
	print("PROPOSED: ", proposed_next_prompt_time)

	if utc_sleep_time.time() <= proposed_next_prompt_time.time() <= utc_wake_time.time():

		wake_tmp = datetime.strptime(str(utc_wake_time.time()), '%H:%M:%S')
		sleep_tmp = datetime.strptime(str(utc_sleep_time.time()), '%H:%M:%S')
		next_tmp = datetime.strptime(str(proposed_next_prompt_time.time()), '%H:%M:%S.%f')

		additional_minutes = (wake_tmp - next_tmp) + (next_tmp - sleep_tmp)

		time_away_minutes = time_away_minutes + (additional_minutes.seconds/60)
		proposed_next_prompt_time_revised = time_anchor + timedelta(hours=0,minutes=time_away_minutes,seconds=0)

	return time_away_minutes	



def next_response_minutes(user):
	#this is just to simulate the responses so, DON"T CARE ABOUT IT
	working_settings = UserSetting.objects.all().get(user=user)
	time_away_minutes = int(triangular(working_settings.exp_response_time_min, working_settings.exp_response_time_max, working_settings.exp_response_time_avg)) #please note, that you'll want to change this.  it'll probs be some other distro, but this is just easy peasy for now.#low, high, mode
	
	return time_away_minutes	









