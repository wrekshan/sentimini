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




# discard_all()

# from django.db import models
# from django.conf import settings
from ent.models import Emotion, Entry, UserSetting, Incoming, NewUserPrompt, Outgoing, UserGenPrompt
# from emojinsei import settings
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

def next_prompt_minutes(user):
	working_settings = UserSetting.objects.all().get(user=user)
	time_away_minutes = int(triangular(working_settings.prompt_interval_minute_min, working_settings.prompt_interval_minute_max, working_settings.prompt_interval_minute_avg)) #please note, that you'll want to change this.  it'll probs be some other distro, but this is just easy peasy for now.#low, high, mode
	return time_away_minutes

def set_prompt_time(user,minutes_to_add):
	working_settings = UserSetting.objects.all().get(user=user)
	
	################################################################################
	##### GET THE SMART WAKE AND SLEEP TIMES (THAT ACCOUNT FOR TIMEZONES AND SHIT)
	################################################################################
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
	################################################################################
	##### GET THE SMART WAKE AND SLEEP TIMES (THAT ACCOUNT FOR TIMEZONES AND SHIT)
	################################################################################
	
	proposed_next_prompt_time = datetime.now(pytz.utc) + timedelta(hours=0,minutes=minutes_to_add,seconds=0)

	# This is the logic to make sure not awake time.  ignore for now
	if utc_sleep_time <= proposed_next_prompt_time <= utc_wake_time:
		time_to_send = utc_wake_time + (utc_wake_time - proposed_next_prompt_time)
	else:
		time_to_send = proposed_next_prompt_time

	return time_to_send


def determine_next_prompt_series(user):
	working_settings = UserSetting.objects.all().get(user=user)

	#Determine if Emotion, instruction, or series
	tmp = randint(1,100)
	series_max = int(working_settings.prompt_multiple_rate*100)

	#Check to see if last prompt was part of the series
	working_entry = Entry.objects.all().filter(user=user)
	working_entry_last = working_entry.latest('time_sent')

	#not a failed series last prompt
	series_num = 0

	if working_entry_last.failed_series == 0:
		if tmp <= series_max:
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


	

def set_next_prompt(user,typer):
	working_settings = UserSetting.objects.all().get(user=user)

	#Determine if user generated or not
	tmp = randint(0,100)
	if tmp <= working_settings.user_generated_prompt_rate and UserGenPrompt.objects.filter(user=user).count()>0:
		emo_type= "User Generated"
		working_emotion = UserGenPrompt.objects.filter(user=user).filter(active=True).filter(show_user=True).order_by('?').first()
	else:
		if typer=="any":
			#Determine if Emotion, instruction, or series
			tmp = randint(1,100)
			core_max = int(working_settings.emotion_core_rate*100)
			top_max = int(working_settings.emotion_top100_rate*100) + core_max
			other_max = int(working_settings.emotion_other_rate*100) + top_max 

			if tmp <= core_max:
				emo_type= "CORE"
			if core_max < tmp <= top_max:
				emo_type = "Top100"
			if top_max < tmp <= other_max:	
				emo_type = "Other"
		else:
			emo_type= "CORE"
			
		working_emotion = Emotion.objects.filter(emotion_type=emo_type).order_by('?').first()


		# working_entry = Entry.objects.all().filter(user=user) # I don't know why I have this here
		# working_entry_last = working_entry.latest('time_sent') # I don't know why I have this here

		

	return working_emotion, emo_type

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


# def prompt_type_lookup(user, prompt):
# 	if Emotion.objects.all().filter(emotion=prompt).count()>0:
# 		print("EMOTION PROMPT")
# 		prompt_type = Emotion.objects.all().get(emotion=prompt).emotion_type
# 	elif UserGenPrompts.objects.all().filter(user=user).filter(prompt=prompt)>0:
# 		print("USER PROMPT")
# 		prompt_type = "User Gen"
# 	else:
# 		prompt_type = "Unknown"
# 	return prompt_type

end_of_teaching_period = "NUP5"
unanswered_series_wait_time_in_minutes = 2


@periodic_task(run_every=timedelta(seconds=2))
def send_emotion_prompt():
	print("TASK 1 - SENDING")
	today_date = datetime.now(pytz.utc)
	print(today_date)
	#filter out the ones that haven't been sent out yet AND the ones that are suppose to be sent out now
	working_entries = Entry.objects.filter(time_to_send__lte=datetime.now(pytz.utc)).filter(time_sent=None)

	#Go through the entries and determine if any need to be sent
	for working_entry in working_entries:
		# Send and update shit
		now = datetime.now(pytz.utc)


		#Check to see if the is not respite.  if good, then send.  ALSO SHOULD ADD IN THE ADDITIONAL CHECKS (number of prompts, not night time)
		working_settings = UserSetting.objects.all().get(user=working_entry.user)
		if now > working_settings.respite_until_datetime or 'Pause' in working_entry.prompt_type:
			print("Time is not during respite")
			################################################################################
			##### GET THE SMART WAKE AND SLEEP TIMES (THAT ACCOUNT FOR TIMEZONES AND SHIT)
			################################################################################
			#figure out the sleep time (ignoring tz)
			now_date = now.date()
			sleepy_time = datetime.combine(now_date,working_settings.sleep_time)

			#figure out the sleep time with local tz
			local_tz = pytz.timezone(working_settings.timezone)
			local_sleep_time = local_tz.localize(sleepy_time)

			#convert the sleep time to the utc sleep time and wake time
			utc_sleep_time = local_sleep_time.astimezone(pytz.UTC)
			utc_wake_time = utc_sleep_time + timedelta(0,60*60*int(working_settings.sleep_duration))
			################################################################################
			##### GET THE SMART WAKE AND SLEEP TIMES (THAT ACCOUNT FOR TIMEZONES AND SHIT)
			################################################################################

			if utc_sleep_time <= now <= utc_wake_time:
				print("Time is not during respite but during sleep")
				working_entry.time_to_send = utc_wake_time + timedelta(hours=0, minutes=randint(1,60))
				working_entry.save()
			else:
				print("Time is not during respite or sleep")
				
				if working_settings.text_request_stop == False:
					addressee = UserSetting.objects.all().get(user=working_entry.user).sms_address

					#Check to see if instruction or user generated or what not
					if not working_entry.prompt_type == 'User Generated' and not "NUP" in working_entry.prompt_type and not "Pause" in working_entry.prompt_type :

						if working_entry.series > 0:
							message_to_send = "How much " + str(working_entry.prompt) + " is in your present moment (0-10)? This is " + str(working_entry.series) + " out of 3 prompts."
						else:
							message_to_send = "How much " + str(working_entry.prompt) + " is in your present moment (0-10)?"
					else:
						message_to_send = str(working_entry.prompt)

					#This will check to see if we've emailed this person in the last ten minutes with the same message
					past_ten_minutes = datetime.now(pytz.utc) - timedelta(minutes=1)
					out_check = Outgoing.objects.all().filter(entry_id=working_entry.id).filter(date_sent__gte=past_ten_minutes).count()
					print("OUTCHECK VAL")
					print(out_check)
					if out_check < 1:
						print("HAVEN'T SENT MESSAGE IN THE LAST 1 MINUTES")
						print("SMS SENT!")

						Outgoing(addressee=UserSetting.objects.all().get(user=working_entry.user).sms_address,date_sent=datetime.now(pytz.utc),message=working_entry.prompt,entry_id=working_entry.id).save()
						send_mail('',message_to_send,'emojinsei@gmail.com', [addressee], fail_silently=False)
						working_entry.time_sent = datetime.now(pytz.utc)

						#Normal texts don't need a response back.  but teaching ones do
						if working_settings.teaching_period_on == True and "NUP" in working_entry.prompt_type:
							working_entry.ready_for_next = False
						working_entry.save()
						
					else:
						print("THIS PROMPT HAS BEEN SENT IN THE LAST 15 MINUTES.  NOT SENT")
				else:
					# print(wrking_settings.user)
					# print(working_settings.text_request_stop)
					print("SMS NOT SENT! - Text Request Stop")
		else:
			print("Time is during respite")


@periodic_task(run_every=timedelta(seconds=2))
def determine_next_prompt():
	print("TASK 2- UPDATING NEW PROMPTS")
	today_date = datetime.now(pytz.utc)
	print(today_date)
	
	#you is going to have to do this by the user
	US = UserSetting.objects.filter(send_text=True)
	for working_settings in US:
		print(working_settings.user)


		

		#This checks to see if there are any entries.  If there are not, then it adds a new one!  This should only be fore the instruction prompts
		if Entry.objects.filter(user=working_settings.user).count() < 1:
			print("CREATING NUP SERIES")
			working_entry_new = Entry(user=working_settings.user,prompt_reply=None,time_created=datetime.now(pytz.utc))
			working_entry_new.time_to_add = 0

			working_prompt = set_next_prompt_instruction(user=working_settings.user) #this is the prompt to send
			working_entry_new.time_to_send = set_prompt_time(user=working_settings.user,minutes_to_add=working_entry_new.time_to_add)
			working_entry_new.prompt = working_prompt.prompt
			working_entry_new.prompt_type = 'NUP'+ str(working_prompt.NUP_seq)

			working_entry_new.send_next_immediately = working_prompt.send_next_immediately
			working_entry_new.save()

		else:
			print("NOT NUP SERIES")
			working_entries = Entry.objects.filter(user=working_settings.user)
			working_entry = working_entries.latest('time_to_send')

		
			#Check to see if they have just reach their teaching period
			if working_entry.prompt_type == end_of_teaching_period:
				# if working_entry.emotion_type == end_of_teaching_period:
				print("END OF TEACHING")
				working_settings.teaching_period_on = False
				working_settings.save()
			

			#Check to see if we are in a respite period.  If this is the case, then update the time to send.  This will be run pretty much once
			now = datetime.now(pytz.utc) 
			if now < working_settings.respite_until_datetime:
				print("Time is during respite, time to send updated")
				working_entry.time_to_send = working_settings.respite_until_datetime
				working_entry.save()
			else:
				#do a quick check to see if the series has been forgotten
				if working_entry.series > 0 and working_entry.time_response == None and not working_entry.time_sent == None:
					td = datetime.now(pytz.utc) - working_entry.time_sent
					td_mins = td / timedelta(minutes=1)

					#I thnk this just solvees a problem during the debug
					td = datetime.now(pytz.utc) - working_entry.time_to_send
					td2_mins = td / timedelta(minutes=1)

					print("UNANSWERED SERIES")
					print(int(td_mins))

					#This is if the last prompt was unanswered
					if int(td_mins) > unanswered_series_wait_time_in_minutes and td2_mins>2:

						working_entry.failed_series = 1
						working_entry.ready_for_next = True
						working_entry.save()
						print("EDITED PROMPT line 340")


				#See if the latest prompt has been sent.  If it has, then create a new one to send
				if not working_entry.time_sent == None and working_entry.ready_for_next == True:
				#create new entry
					if working_settings.teaching_period_on == True:
						print("CREATE TEACHING INSTRUCTION")
						working_entry_new = Entry(user=working_entry.user,prompt_reply=None,time_created=datetime.now(pytz.utc))

						#Should it be sent immediately (i.e. instruction or series?)
						if working_entry.send_next_immediately == True:
							working_entry_new.time_to_add = 0
						else:
							working_entry_new.time_to_add = next_prompt_minutes(user=working_entry.user)

						working_prompt = set_next_prompt_instruction(user=working_entry.user) #this is the prompt to send
						working_entry_new.time_to_send = set_prompt_time(user=working_entry.user,minutes_to_add=working_entry_new.time_to_add)
						working_entry_new.prompt = working_prompt.prompt
						working_entry_new.prompt_type = 'NUP'+ str(working_prompt.NUP_seq)

						working_entry_new.send_next_immediately = working_prompt.send_next_immediately
						working_entry_new.save()
						print("NEW PROMPT line 363")


					else:
						print("Normal Period")
						working_entry_new = Entry(user=working_entry.user,prompt_reply=None,time_created=datetime.now(pytz.utc))
						working_entry_new.prompt, working_entry_new.prompt_type = set_next_prompt(user=working_entry.user,typer="any")
						# working_entry_new.emotion_type = prompt_type_lookup(user=working_entry.user, prompt=working_entry_new.emotion)
						working_entry_new.series = determine_next_prompt_series(user=working_entry.user)
											
						if working_entry.send_next_immediately == True:
							working_entry_new.time_to_add = 0
						else:
							working_entry_new.time_to_add = next_prompt_minutes(user=working_entry.user)

						if 0 < working_entry_new.series <= 2:
							working_entry_new.time_to_add = 0
							working_entry_new.ready_for_next = False
							working_entry_new.send_next_immediately = True

						if working_entry_new.series == 3:
							working_entry_new.time_to_add = 0
							working_entry_new.ready_for_next = False
							working_entry_new.send_next_immediately = False


						working_entry_new.time_to_send = set_prompt_time(user=working_entry.user,minutes_to_add=working_entry_new.time_to_add)
						working_entry_new.save()
						print("NEW PROMPT line 416")



@periodic_task(run_every=timedelta(seconds=2))
def check_email_for_new():
	#Set up the email 
	print("TASK 3 - RECIEVE MAIL")
	mail = imaplib.IMAP4_SSL('imap.gmail.com')
	mail.login('emojinsei@gmail.com', 'wr579351')
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

				if 'pause' in tp.email_content.lower():
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

					working_user.respite_until_datetime = dater
					working_user.save()


					#create new entry to send
					working_entry_new = Entry(user=working_user.user,prompt_reply=None,time_created=datetime.now(pytz.utc))
					working_entry_new.time_to_add = 0
					working_entry_new.time_to_send = set_prompt_time(user=working_user.user,minutes_to_add=working_entry_new.time_to_add)
					working_entry_new.prompt = "Pausing for now"
					working_entry_new.prompt_type = "Pause"
					working_entry_new.save()

				if 'start' in tp.email_content.lower():
					print("START PRESENT")
					working_user.respite_until_datetime = datetime.now(pytz.utc)
					working_user.text_request_stop = False
					working_user.save()

					#create new entry to send
					working_entry_new = Entry(user=working_user.user,prompt_reply=None,time_created=datetime.now(pytz.utc))
					working_entry_new.time_to_add = 0
					working_entry_new.time_to_send = set_prompt_time(user=working_user.user,minutes_to_add=working_entry_new.time_to_add)
					working_entry_new.prompt = "Starting again"
					working_entry_new.prompt_type = "Pause"
					working_entry_new.save()

					
					


			working_entry = Entry.objects.all().filter(user=working_user.user).exclude(time_sent__isnull=True) 
			working_entry = working_entry.filter(time_sent__lte=tp.email_date)
			print(working_entry.count())
			if working_entry.count() > 0:
				print("more than 0")
				working_entry = working_entry.latest('time_sent') #YOU DO INDDED WANT LATEST
				# working_entry = working_entry.order_by('time_sent')[0] #EARLIEST.  I ON'Y HAVE THIS HERE FOR TESTING

				#Look for only the digits
				if hasNumbers(tp.email_content) == True:
					print("EMAIL HAS DIGITS")

					working_entry.time_response = tp.email_date
					td =  working_entry.time_response - working_entry.time_sent
					working_entry.response_time_seconds = int(td.seconds)
					email_content_int = int(re.search(r'\d+', tp.email_content).group())
					working_entry.prompt_reply = email_content_int
				
				working_entry.ready_for_next = True #this tells me there is a response, so i can sent the next instruction
				working_entry.save()		
		else:
			print("User doesn't exist, so make it")
		
		print("Email Processed")
		tp.processed = 1
		tp.save()
print("CHECKING FOR MESSAGES DONE")
		




# CELERYBEAT_SCHEDULE = {
#     'every-second': {
#         'task': 'check_email_for_new',
#         'schedule': timedelta(seconds=15),
#     },
# }

# CELERYBEAT_SCHEDULE = {
#     'every-second': {
#         'task': 'determine_next_prompt',
#         'schedule': timedelta(seconds=15),
#     },
# }

# CELERYBEAT_SCHEDULE = {
#     'every-second': {
#         'task': 'send_emotion_prompt',
#         'schedule': timedelta(seconds=15),
#     },
# }

# CELERYBEAT_SCHEDULE = {
#     'every-second': {
#         'task': 'process_new_mail',
#         'schedule': timedelta(seconds=15),
#     },
# }







########### HOW TO RUN
#Open three term windows
# 1 start rabit with: sudo rabbitmq-server
	#you might have to add a path to the terminal before you do with
# 2 start server with runserver
# 3 start celery (you need both worker and beat)
	#alright, you cd into the emojinsei project
	#start it with:  celery -A emojinsei worker -B
# start it with sudo rabbitmq-server
#stop it with: $ sudo rabbitmqctl stop

