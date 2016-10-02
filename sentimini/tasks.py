from __future__ import absolute_import

from celery.task import periodic_task
from datetime import datetime, timedelta
from random import random, triangular, randint
from django.core.mail import send_mail
from email.utils import parsedate_tz, parsedate_to_datetime
import pytz
import re
import imaplib
import email
from celery.task.control import discard_all

import parsedatetime as pdt # for parsing of datetime shit for NLP
from .settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD

import string




# discard_all()

# from django.db import models
# from django.conf import settings
from ent.models import PossibleTextSTM, ActualTextSTM, UserSetting, Incoming, Outgoing, ExperienceSetting, Ontology, Prompttext, ActualTextLTM

# from sentimini import settings
def get_first_text_part(msg):
    maintype = msg.get_content_maintype()
    if maintype == 'multipart':
        for part in msg.get_payload():
            if part.get_content_maintype() == 'text':
                return part.get_payload()
    elif maintype == 'text':
        return msg.get_payload()

def hasNumbers(inputString):
	return bool(re.search(r'\d', inputString))


########### THINGS TO DO
# Check to see if there is only one prompt.  if there are more scheduled to be sent, then remove one
# Add in a check to not send more than X per day
# Add in a check to not send if the respite date

#function for adding time
#function for determining emotion



	

def set_next_prompt_instruction(user):
	working_settings = UserSetting.objects.all().get(user=user)

	#get the latest working entry
	working_entries = Entry.objects.all().filter(user=user).filter(prompt_type__icontains="NUP")

	if working_entries.count() > 0:
		working_entry = working_entries.latest('time_sent')
		instruction_prompt_number = int(re.search(r'\d+', working_entry.prompt_type).group()) + 1
		working_prompt = NewUserPrompt.objects.all().get(NUP_seq=instruction_prompt_number)
	else:
		working_prompt = NewUserPrompt.objects.all().get(NUP_seq=1)

	return(working_prompt)





unanswered_series_wait_time_in_minutes = 60
unanswered_prompt_wait_time_in_minutes = 5


@periodic_task(run_every=timedelta(seconds=300))
def clean_up_outgoing():
	print("CLEAN UP")
	one_day = datetime.now(pytz.utc) - timedelta(days=1)
	Outgoing.objects.all().filter(date_sent__lte=one_day).delete()


####################################################################################################
#################### THIS IS WHERE THE DEFINITIVE FUNCTIONS WILL LIVE DURING THE REFACTOR - NOT IN THE SCHELER FUNCTIONS
####################################################################################################
def sleep_check(text):
	working_settings = UserSetting.objects.all().get(user=text.user)

	#figure out the sleep time (ignoring tz)
	now = datetime.now(pytz.utc)
	now_date = now.date()
	sleepy_time = datetime.combine(now_date,working_settings.sleep_time)

	#figure out the sleep time with local tz
	local_tz = pytz.timezone(working_settings.timezone)
	local_sleep_time = local_tz.localize(sleepy_time)

	#convert the sleep time to the utc sleep time and wake time
	utc_sleep_time = local_sleep_time.astimezone(pytz.UTC)
	utc_wake_time = utc_sleep_time + timedelta(0,60*60*int(working_settings.sleep_duration))
	
	proposed_next_prompt_time = now + timedelta(hours=0,minutes=text.time_to_add,seconds=0)

	# This is the logic to make sure not awake time.  ignore for now
	if utc_sleep_time <= proposed_next_prompt_time <= utc_wake_time:
		time_to_send = utc_wake_time + (utc_wake_time - proposed_next_prompt_time)
	else:
		time_to_send = proposed_next_prompt_time

	return time_to_send			
		
		
def send_text(text):
	now = datetime.now(pytz.utc)
	user_settings = UserSetting.objects.all().get(user=text.user)
	exp_settings = ExperienceSetting.objects.all().filter(user=text.user).get(experience="user")

	# YOU CAN DO THE CHECKS HERE

	#check is this during sleep?
	# text.time_to_send = sleep_check(text=text)
	# text.save()

	#This will check to see if we've emailed this person in the last ten minutes with the same message
	now = datetime.now(pytz.utc)
	past_ten_minutes = datetime.now(pytz.utc) - timedelta(minutes=1)
	out_check = Outgoing.objects.all().filter(entry_id=text.id).filter(date_sent__gte=past_ten_minutes).count()
	print("OUTCHECK:", out_check)

	if now > text.time_to_send and out_check < 1:
		tmp_user = UserSetting.objects.all().get(user=text.user)
		addressee = tmp_user.sms_address
		message_to_send = str(text.text)

		if now > tmp_user.respite_until_datetime and tmp_user.text_request_stop == False or text.system_text==1: 

			Outgoing(addressee=addressee,date_sent=datetime.now(pytz.utc),message=text.text,entry_id=text.id).save()
			#switch out and see if you can send a monky pic
			send_mail('',message_to_send,'emojinseidev@gmail.com', [addressee], fail_silently=False)
			text.time_sent = datetime.now(pytz.utc)
			text.save()

def set_next_prompt(user, text_type):
	working_settings = UserSetting.objects.all().get(user=user)

	#DETERMINE IF RESEARCH OR USER GEN
	if text_type=="user":
		
		#I think this is a kludge
		working_texts = PossibleTextSTM.objects.filter(user=user).filter(text_type="user").filter(show_user=False)
		tmp_texts = []
		for txt in working_texts:
			for i in range(0,txt.text_importance):
				tmp_texts.append(txt.text)

		working_emotion = PossibleTextSTM.objects.filter(user=user).filter(text_type="user").filter(show_user=False).filter(text=tmp_texts[randint(0,len(tmp_texts)-1)]).first()
	
	else:
		#Determine if Emotion, instruction, or series
		working_texts = PossibleTextSTM.objects.filter(text_type="research").filter(show_user=False)
		tmp_texts = []
		for txt in working_texts:
			for i in range(0,txt.text_importance):
				tmp_texts.append(txt.text)

		working_emotion = PossibleTextSTM.objects.filter(text_type="research").get(text=tmp_texts[randint(0,len(tmp_texts)-1)])

	return working_emotion, working_emotion.id	

def determine_prompt_texts(user,prompt,typer):
	if typer == 'user':
		working_UPGR = PossibleTextSTM.objects.all().filter(user=user).filter(text=prompt).first()
		prompt_full = prompt
		prompt_reply_type = working_UPGR.response_type
		
	else:
		ontology_settings = Ontology.objects.all().filter(ontological_type='instruction')

		# Figure out the type of response
		
		dim_max = int(ontology_settings.get(prompt_set = "0 to 10").prompt_set_percent)
		cat_max = int(ontology_settings.get(prompt_set = "Yes or No").prompt_set_percent) + dim_max
		open_max = int(ontology_settings.get(prompt_set = "open").prompt_set_percent) + cat_max 
		none_max = int(ontology_settings.get(prompt_set = "none").prompt_set_percent) + open_max 
		tmp = randint(1,100)
		if tmp <= dim_max:
			prompt_reply_type= "0 to 10"
		if dim_max < tmp <= cat_max:
			prompt_reply_type = "Yes or No"
		if cat_max < tmp <= open_max:	
			prompt_reply_type = "open"
		if open_max < tmp <= none_max:	
			prompt_reply_type = "none"

		#Now figure out the specific texts
		working_texts = Prompttext.objects.all().filter(text_type = prompt_reply_type)
		tmp_texts = []
		for txt in working_texts:
			for i in range(0,txt.text_percent):
				tmp_texts.append(txt.text)
	
		random_draw = randint(0,len(tmp_texts)-1)
		default_prompt = tmp_texts[random_draw]

		#set up the full text 
		prompt_full = str(default_prompt)
		prompt_full = prompt_full.replace("XXX", str(prompt))
		
	return prompt_full, prompt_reply_type		

def set_prompt_time(text,send_now,fake_time_now):
	working_settings = UserSetting.objects.all().get(user=text.user)
	experience_settings = ExperienceSetting.objects.all().filter(user=text.user).get(experience=text.text_type)
	
	#figure out the sleep time (ignoring tz)
	if fake_time_now == 0:
		now = datetime.now(pytz.UTC)
	else:
		now = fake_time_now

	# Add the minutes
	if send_now == 1:
		minutes_to_add = 0

	else:
		minutes_to_add = int(triangular(experience_settings.prompt_interval_minute_min, experience_settings.prompt_interval_minute_max, experience_settings.prompt_interval_minute_avg)) 
		proposed_next_prompt_time = now + timedelta(hours=0,minutes=minutes_to_add,seconds=0)

		local_tz = pytz.timezone(working_settings.timezone)
		local_sleep_time = local_tz.localize(datetime.combine(now.date(),working_settings.sleep_time))
		local_wake_time = local_sleep_time + timedelta(0,60*60*int(working_settings.sleep_duration))

		utc_sleep_time = local_sleep_time.astimezone(pytz.UTC)
		utc_wake_time = local_wake_time.astimezone(pytz.UTC)

		if utc_sleep_time.time() <= proposed_next_prompt_time.time() <= utc_wake_time.time():

			wake_tmp = datetime.strptime(str(utc_wake_time.time()), '%H:%M:%S')
			sleep_tmp = datetime.strptime(str(utc_sleep_time.time()), '%H:%M:%S')
			next_tmp = datetime.strptime(str(proposed_next_prompt_time.time()), '%H:%M:%S.%f')

			additional_minutes = (wake_tmp - next_tmp) + (next_tmp - sleep_tmp)

			minutes_to_add = minutes_to_add + (additional_minutes.seconds/60)
	
	time_to_send = now + timedelta(hours=0,minutes=minutes_to_add,seconds=0)

	return minutes_to_add, time_to_send			

def schedule_new_text(user,text_type):
	text_new = ActualTextSTM(user=user, response=None,simulated=0,text_type=text_type)
	text_new.text, text_new.text_id = set_next_prompt(user=text_new.user,text_type=text_type)
	text_new.text, text_new.response_type = determine_prompt_texts(user=text_new.user,prompt=text_new.text,typer=text_new.text_type)
	text_new.time_to_add, text_new.time_to_send = set_prompt_time(text=text_new,send_now=0,fake_time_now=0)
	text_new.save()






def determine_pause(tp):
	print("pause PRESENT")
	cal = pdt.Calendar() #intialize caldener for parser
	now = datetime.now(pytz.utc)

	dater = cal.parseDT(tp.email_content.lower(), now)[0] #get the date that this is pause to
	dater = pytz.utc.localize(dater)
	
	#Check to see if there was just a 'pause'
	differ = now - dater
	differ = differ.total_seconds()

	if -10 < differ < 10:
		dater = cal.parseDT('1 day', now)[0] #get the date that this is pause to
	
	working_user = UserSetting.objects.all().get(phone=tp.email_user)
	working_user.respite_until_datetime = dater
	working_user.save()	

	return dater

	#Send text, "pause until", you can start again by.

def consolidate(ent):
	print("Entry ID", ent.id)
	ltm_new = ActualTextLTM(user=ent.user,stm_id=ent.id,text_id=ent.text_id,text=ent.text,text_type=ent.text_type,response_type=ent.response_type,response=ent.response,time_response=ent.time_response,response_time=ent.response_time,time_to_send=ent.time_to_send,time_sent=ent.time_sent,time_to_add=ent.time_to_add,series=ent.series,failed_series=ent.failed_series,simulated=ent.simulated)
	print("response", ent.response)
	if ltm_new.response != "" and ltm_new.response != None:
		print("To sort")
		if hasNumbers(ltm_new.response):
			ltm_new.response_dim = int(re.search(r'\d+', ltm_new.response).group())

		if 'yes' in ltm_new.response.lower():
			ltm_new.response_cat = 'yes'
			ltm_new.response_cat_bin = 1

		if 'no' in ltm_new.response.lower():
			ltm_new.response_cat = 'no'
			ltm_new.response_cat_bin = 0

	if ltm_new.time_to_send.hour > 12:
		ltm_new.time_to_send_circa = 'PM'
	ltm_new.time_to_send_day = ltm_new.time_to_send.strftime('%A')
	ltm_new.save()

	ent.consolidated = 1
	ent.save()

def consolidate_update(ent):
	print("Entry ID", ent.id)
	ltm_new = ActualTextLTM.objects.all().filter(user=ent.user).get(stm_id=ent.id)
	ltm_new.response = ent.response
	print("response", ent.response)
	if ltm_new.response != "" and ltm_new.response != None:
		print("To sort")
		if hasNumbers(ltm_new.response):
			ltm_new.response_dim = int(re.search(r'\d+', ltm_new.response).group())

		if 'yes' in ltm_new.response.lower():
			ltm_new.response_cat = 'yes'
			ltm_new.response_cat_bin = 1

		if 'no' in ltm_new.response.lower():
			ltm_new.response_cat = 'no'
			ltm_new.response_cat_bin = 0

	if ltm_new.time_to_send.hour > 12:
		ltm_new.time_to_send_circa = 'PM'
	ltm_new.time_to_send_day = ltm_new.time_to_send.strftime('%A')
	ltm_new.save()

	ent.consolidated = 1
	ent.save()	

	#delete old one here

####################################################################################################
#################### THIS IS WHERE THE DEFINITIVE FUNCTIONS WILL LIVE DURING THE REFACTOR
####################################################################################################
def inhibition_global():
	magic_number_text_per_hour_per_user = 400

	now = datetime.now(pytz.utc)
	number_of_texts_last_hour = Outgoing.objects.all().filter(date_sent__gte=datetime.now(pytz.utc) - timedelta(minutes=60)).count()

	max_texts_hour = UserSetting.objects.all().count() * magic_number_text_per_hour_per_user

	if number_of_texts_last_hour < max_texts_hour:
		return True
	else:
		return False

def inhibition_individual(text):
	magic_number_text_per_hour_per_user = 20

	working_settings = UserSetting.objects.all().get(user=text.user)

	now = datetime.now(pytz.utc)
	number_of_texts_last_hour = Outgoing.objects.all().filter(addressee=working_settings.sms_address).filter(date_sent__gte=datetime.now(pytz.utc) - timedelta(minutes=60)).count()

	if number_of_texts_last_hour < magic_number_text_per_hour_per_user:
		return True
	else:
		return False		




@periodic_task(run_every=timedelta(seconds=2))
def send_texts():
	today_date = datetime.now(pytz.utc)
	#filter out the ones that haven't been sent out yet AND the ones that are suppose to be sent out now
	user_texts = ActualTextSTM.objects.filter(time_to_send__lte=datetime.now(pytz.utc)).filter(time_sent=None).filter(text_type="user").filter(simulated=0)
	research_texts = ActualTextSTM.objects.filter(time_to_send__lte=datetime.now(pytz.utc)).filter(time_sent=None).filter(text_type="research").filter(simulated=0)
	system_texts = ActualTextSTM.objects.filter(time_to_send__lte=datetime.now(pytz.utc)).filter(time_sent=None).filter(system_text=1).filter(simulated=0)

	for text in system_texts:
		# print("inhibition global", inhibition_global())
		# print("inhibition individual", inhibition_individual(text=text))
		if inhibition_global() == True and inhibition_individual(text=text) == True:
			send_text(text)

	for text in user_texts:
		if inhibition_global() == True and inhibition_individual(text=text) == True:
			send_text(text)

	for text in research_texts:
		if inhibition_global() == True and inhibition_individual(text=text) == True:
			send_text(text)


#While most of the scheduling is supposed to be done as a result of an event.  There are two events that will result in scheduling.  1) 60 minutes without a response and 2) a response (whichever is first)



def schedule_greeting_text(exp,text_type):
	if text_type == "user":
		working_settings = UserSetting.objects.all().get(user=exp.user)
		working_settings.user_generated_prompt_rate

		text1 = str('Hello! You just signed up to receive around '+ str(working_settings.user_generated_prompt_rate) + ' texts per week.  If you did not, just reply with ‘stop’ or visit sentimini.com to stop receiving these messages.')
		ActualTextSTM(user=exp.user,text=text1,response=None,simulated=0,ready_for_next=1,text_type='user',time_to_send=datetime.now(pytz.utc)).save()


@periodic_task(run_every=timedelta(seconds=2))
def schedule_texts():
	exp_settings = ExperienceSetting.objects.all().filter(experience="user").filter(prompt_interval_minute_avg__gte=0)
	research_settings = ExperienceSetting.objects.all().filter(experience="research").filter(prompt_interval_minute_avg__gte=0)

	for exp in exp_settings:
		if ActualTextSTM.objects.all().filter(simulated=0).filter(user=exp.user).filter(text_type="user").count() < 1:

			schedule_greeting_text(exp=exp,text_type="user")
		else:
			texts = ActualTextSTM.objects.all().filter(user=exp.user).filter(text_type="user")
			text_last = texts.latest('time_to_send')

			if text_last.ready_for_next == 1:
				schedule_new_text(user=exp.user,text_type="user")

	for exp in research_settings:
		if exp.prompts_per_week > 0:

			if ActualTextSTM.objects.all().filter(user=exp.user).filter(text_type="research").count() < 1:
				schedule_new_text(user=exp.user,text_type="research")
			else:
				texts = ActualTextSTM.objects.all().filter(simulated=0).filter(user=exp.user).filter(text_type="research")
				text_last = texts.latest('time_to_send')

				if text_last.ready_for_next == 1:
					schedule_new_text(user=exp.user,text_type="research")




@periodic_task(run_every=timedelta(seconds=2))
def check_email_for_new():
	#Set up the email 
	print("TASK 3 - RECIEVE MAIL")
	mail = imaplib.IMAP4_SSL('imap.gmail.com')
	mail.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
	mail.list()

	# Out: list of "folders" aka labels in gmail.
	mail.select("inbox") # connect to inbox.

	#Get the IDs of the mail in the boxes
	result, data = mail.search(None, "ALL")
	ids = data[0] # data is a list.
	id_list = ids.split()

	#Go through each new email and figure out what it corresponds to
	for id in id_list:
		print("DOWNLOADING MESSAGES")
		print(id)
		result, data = mail.fetch(id, "(RFC822)") # fetch the email body (RFC822) for the given ID
		
		if data is not None:
			print("data is not none")
			raw_email = data[0][1] # here's the body, which is raw text of the whole email
			email_message = email.message_from_bytes(raw_email) #converts to email object
	
			
			#Get the email info
			email_user = email_message['From'].split('@',1)[0]
			email_date = parsedate_to_datetime(email_message.get('date'))
			email_content = get_first_text_part(email_message)

			Incoming(email_user=email_user,email_date=email_date,email_message=email_message,email_content=email_content).save()
			print("NEW INCOMING SAVED")
			mail.store(id, '+FLAGS', '\\Deleted') # flage this for deletion
	mail.expunge() #delete them
	print("BOX CLEANED")





@periodic_task(run_every=timedelta(seconds=3))
def process_new_mail():
	print("TASK 4 - PROCESS MAIL")
	Toprocess = Incoming.objects.all().filter(processed=0)
	for tp in Toprocess:
	
		#need conditional
		if UserSetting.objects.all().filter(phone=tp.email_user).exists():
			working_user = UserSetting.objects.all().get(phone=tp.email_user)	
			
			#check to see if the user wants to stop
			print("CHECKING FOR STOP")
			############################################################
			############### CHECK FOR RESPONSE AND DETERMINE WHAT IT IS
			############################################################
			if tp.email_content is not None: #this is new

				if 'stop' in tp.email_content.lower():
					print("STOP PRESENT")
					working_user.text_request_stop = True
					working_user.save()
					
					possible_text = PossibleTextSTM.objects.all().get(text_type='system stop')
					text_out = ActualTextSTM(user=working_user.user, response=None,simulated=0,text=possible_text.text, system_text=1)
					text_out.time_to_add, text_out.time_to_send = set_prompt_time(text=text_out,send_now=1,fake_time_now=0)
					text_out.save()


				elif 'pause' in tp.email_content.lower():
					pause_until_date = determine_pause(tp)

					possible_text = PossibleTextSTM.objects.all().get(text_type='system pause')

					text_out = possible_text.text
					text_out = text_out.replace("XXX", str(pause_until_date))

					print(text_out)

					text_out = ActualTextSTM(user=working_user.user, response=None,simulated=0,text=text_out, system_text=1)
					text_out.time_to_add, text_out.time_to_send = set_prompt_time(text=text_out,send_now=1,fake_time_now=0)
					text_out.save()
										

				elif 'start' in tp.email_content.lower():
					print("START PRESENT")
					working_user.respite_until_datetime = datetime.now(pytz.utc)
					working_user.text_request_stop = False
					working_user.save()

					possible_text = PossibleTextSTM.objects.all().get(text_type='system start')
					text_out = ActualTextSTM(user=working_user.user, response=None,simulated=0,text=possible_text.text, system_text=1)
					text_out.time_to_add, text_out.time_to_send = set_prompt_time(text=text_out,send_now=1,fake_time_now=0)
					text_out.save()


				working_entry = ActualTextSTM.objects.all().filter(user=working_user.user).exclude(time_sent__isnull=True)
				working_entry = working_entry.filter(time_sent__lte=tp.email_date)
				
				if working_entry.count() > 0:
					working_entry = working_entry.latest('time_sent')

					
					if working_entry.response is None or working_entry.response == "":
						#save in to actual stm
						working_entry.time_response = tp.email_date
						td =  working_entry.time_response - working_entry.time_sent
						working_entry.response_time_seconds = int(td.seconds)
						working_entry.response = tp.email_content
						working_entry.ready_for_next = True
						working_entry.save()

						if working_entry.ready_for_next == True and working_entry.system_text == 0:
							if ActualTextLTM.objects.all().filter(user=ent.user).filter(stm_id=ent.id).count()<1:
								consolidate(working_entry)
							else:
								consolidate_update(working_entry)
						

						
		else:
			print("User doesn't exist, so make it")

		print("Email Processed")
		tp.processed = 1
		tp.save()
		
		


@periodic_task(run_every=timedelta(seconds=2))



def actual_text_consolidate():
	working_entry = ActualTextSTM.objects.all().exclude(time_sent__isnull=True).filter(consolidated=0).filter(ready_for_next=True)
	print("++++++++ ACTUAL TEXT CONSOLIDATE ++++++++")
	print("ENTRY COUNT:", ActualTextSTM.objects.all().exclude(time_sent__isnull=True).filter(consolidated=0).filter(ready_for_next=True).count())
	# you are going to have to fix this....unanswered text consolidated
	for ent in working_entry:
		consolidate(ent)
		

	

@periodic_task(run_every=timedelta(seconds=2))
def check_for_nonresponse():
	working_entry = ActualTextSTM.objects.all().exclude(time_sent__isnull=True).filter(ready_for_next=False)
	
	for ent in working_entry:
		exp_settings = ExperienceSetting.objects.all().filter(experience=ent.text_type).get(user=ent.user)

		td = datetime.now(pytz.utc) - ent.time_sent
		td_mins = td / timedelta(minutes=1)

		if td_mins > exp_settings.time_to_declare_lost:
			ent.ready_for_next = True
			ent.save()

		#OR if a new one was sent


		
		











########### HOW TO RUN
#Open three term windows
# 1 start rabit with: sudo rabbitmq-server
	#you might have to add a path to the terminal before you do with
# 2 start server with runserver
# 3 start celery (you need both worker and beat)
	#alright, you cd into the sentimini project
	#start it with:  celery -A sentimini worker -B
# start it with sudo rabbitmq-server
#stop it with: $ sudo rabbitmqctl stop

