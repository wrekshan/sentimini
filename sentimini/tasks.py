from __future__ import absolute_import
from celery import Celery
from celery.task import periodic_task, task
from datetime import datetime, timedelta
from random import random, triangular, randint, gauss
from django.core.mail import send_mail
from email.utils import parsedate_tz, parsedate_to_datetime
import pytz
import re
import imaplib
import email
from celery.task.control import discard_all

import parsedatetime as pdt # for parsing of datetime shit for NLP
from .settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, use_gmail

import string

from ent.models import PossibleText, Collection, Timing, Tag, ActualText, Carrier, UserSetting, Outgoing, Incoming

from ent.views import time_window_check, date_check_fun

from .celery import app
# app = Celery()

# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls test('hello') every 10 seconds.
#     sender.add_periodic_task(10.0, schedule_texts, name='add every 10')
#     sender.add_periodic_task(10.0, send_texts, name='add every 10')
#     sender.add_periodic_task(10.0, check_email_for_new, name='add every 10')
#     sender.add_periodic_task(10.0, process_new_mail, name='add every 10')

app.conf.beat_schedule = {
    'schedule': {
        'task': 'schedule_texts',
        'schedule': timedelta(seconds=20),
        'args': ()
    },
    'send': {
        'task': 'send_texts',
        'schedule': timedelta(seconds=20),
        'args': ()
    },
    'check': {
        'task': 'check_email_for_new',
        'schedule': timedelta(seconds=20),
        'args': ()
    },
    'process': {
        'task': 'process_new_mail',
        'schedule': timedelta(seconds=20),
		'args': ()
    },
}    


# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(20.0, schedule_texts, name='add every 10')
#     sender.add_periodic_task(20.0, send_texts, name='add every 10')
#     sender.add_periodic_task(20.0, check_email_for_new, name='add every 10')
#     sender.add_periodic_task(20.0, process_new_mail, name='add every 10')
task_seconds_between = 15
#############################################
######## PERODIC TASK TO SCHEDULE NOW TEXTS
#############################################


def schedule_specific_text(text,working_settings,user_timezone, time_window,day):
	date_today = datetime.now(pytz.utc).astimezone(user_timezone)

	scheduled_date = user_timezone.localize(datetime.combine(date_today, text.timing.hour_start))
	scheduled_date = scheduled_date.astimezone(pytz.UTC)
	
	for i in range(text.timing.repeat_in_window):
		seconds_to_add = randint(0,round(time_window.total_seconds()))
		atext = ActualText(user=text.user,text=text)
		if datetime.now(pytz.utc) > user_timezone.localize(datetime.combine(date_today, text.timing.hour_end)).astimezone(pytz.UTC):
			atext.time_to_send = scheduled_date + timedelta(0,(86400+seconds_to_add))
		elif datetime.now(pytz.utc) > scheduled_date and datetime.now(pytz.utc) < user_timezone.localize(datetime.combine(date_today, text.timing.hour_end)).astimezone(pytz.UTC):
			time_window = datetime.now(pytz.utc) - user_timezone.localize(datetime.combine(date_today, text.timing.hour_start)).astimezone(pytz.UTC)
			seconds_to_add = randint(0,int(time_window.total_seconds()))
			atext.time_to_send = scheduled_date + timedelta(0,(seconds_to_add))+ timedelta(day,0)
		else:
			atext.time_to_send = scheduled_date + timedelta(0,(seconds_to_add))+ timedelta(day,0)

		atext.save()

	text.date_scheduled = datetime.now(pytz.utc)
	text.save()



# @periodic_task(run_every=timedelta(seconds=10))
# @periodic_task(run_every=timedelta(seconds=task_seconds_between))
# @app.task
# @task(name='schedule_texts')
@task()
def schedule_texts():
	print("TASK 1 - STARTING schedule_texts")
	#Specific Timings
	working_texts = PossibleText.objects.all().filter(tmp_save=False).filter(active=True).filter(timing__fuzzy=False).filter(timing__date_start__lte=pytz.utc.localize(datetime.now()))
	for text in working_texts:
		if text.timing.dow_check() == 1:
			if ActualText.objects.all().filter(text=text).filter(time_sent__isnull=True).count()<1:
				# The following conditional is to only schedule texts once a day
				working_settings = UserSetting.objects.all().get(user=text.user)
				user_timezone = pytz.timezone(working_settings.timezone)

				# print("TEXT:", text.text)
				# print("TEXT:", text.timing.repeat_in_window)


				#If the text is not newly scheduled	
				if text.date_scheduled is not None:
					#Idea is to schedule it once a day for the next day
					if pytz.utc.localize(datetime.now()) > text.date_scheduled + timedelta(1,0):
						date_today = datetime.now(pytz.utc).astimezone(user_timezone)
						time_window = user_timezone.localize(datetime.combine(date_today, text.timing.hour_end)) - user_timezone.localize(datetime.combine(date_today, text.timing.hour_start))
						schedule_specific_text(text,working_settings,user_timezone,time_window,1)
						
				else:
					#This is for newly scheduled texts.  Text it today
					# print("NOT SCHEULDED")
					#Schedule it for today

					date_today = datetime.now(pytz.utc).astimezone(user_timezone)
					starting_time = user_timezone.localize(datetime.combine(date_today, text.timing.hour_start))
					starting_time = starting_time.astimezone(pytz.UTC)

					ending_time = user_timezone.localize(datetime.combine(date_today, text.timing.hour_end))
					ending_time = ending_time.astimezone(pytz.UTC)

					# print("STARTING TIME:", starting_time)
					# print("date_today", date_today)
					# print("ENDING TIME:", ending_time)


					###### SCHEDULE IT FOR TODAY - this is just like an extra thing.  
					if not starting_time == ending_time:
						# print("THERE IS A RANGE")
						# Schedule them for today
						if starting_time < date_today < ending_time:
							# print("DATE NOW BETWEEN RANGE")
							time_window = user_timezone.localize(datetime.combine(date_today, text.timing.hour_end)) - date_today
							schedule_specific_text(text,working_settings,user_timezone,time_window,0)
						else:
							# print("DATE BEFORE RANGE")
							time_window = user_timezone.localize(datetime.combine(date_today, text.timing.hour_end)) - user_timezone.localize(datetime.combine(date_today, text.timing.hour_start))
							schedule_specific_text(text,working_settings,user_timezone,time_window,0)
					else:
						if date_today < starting_time:
							time_window = user_timezone.localize(datetime.combine(date_today, text.timing.hour_end)) - user_timezone.localize(datetime.combine(date_today, text.timing.hour_start))
							schedule_specific_text(text,working_settings,user_timezone,time_window,0)

					#Schedule it for tomorrow!
					time_window = user_timezone.localize(datetime.combine(date_today, text.timing.hour_end)) - user_timezone.localize(datetime.combine(date_today, text.timing.hour_start))					
					schedule_specific_text(text,working_settings,user_timezone,time_window,1)
					
					


	#Fuzzy Timings
	working_texts = PossibleText.objects.all().filter(tmp_save=False).filter(active=True).filter(timing__fuzzy=True).filter(timing__date_start__lte=pytz.utc.localize(datetime.now()))
	for text in working_texts:
		if ActualText.objects.all().filter(text=text).filter(time_sent__isnull=True).count()<1:
			# print("SCHEDULING NEW FUZZY TEXT")

			# Get the timing info
			# Hack to have discrete values in slider
			noise_tmp = 100
			if text.timing.iti_noise == 1:
				noise_tmp = 100
			if text.timing.iti_noise == 2:
				noise_tmp = 400
			if text.timing.iti_noise == 3:
				noise_tmp = 600
			if text.timing.iti_noise == 4:
				noise_tmp = 800	
			

			ITI_noise_tmp = noise_tmp/100
			ITI_mean = text.timing.iti
			max_minutes = ITI_mean + (ITI_mean*ITI_noise_tmp)
			min_minutes = ITI_mean - (ITI_mean*ITI_noise_tmp)

			# Add seconds
			seconds_to_add = 60 * int(triangular(min_minutes, max_minutes, ITI_mean))

			
			#Get user timezone
			working_settings = UserSetting.objects.all().get(user=text.user)
			user_timezone = pytz.timezone(working_settings.timezone)
			

			#Get today's date and end in UTC
			date_today = datetime.now(pytz.utc).astimezone(user_timezone)
			possible_date = date_today + timedelta(0,seconds_to_add)
			possible_date = possible_date.astimezone(pytz.UTC)
					
			possible_date = time_window_check(text,possible_date)
			date_check = date_check_fun(text,possible_date)


			possible_date = possible_date.astimezone(pytz.UTC)
			# possible_date = pytz.utc.localize(possible_date)

			if date_check == 1:
				atext = ActualText(user=text.user,text=text,time_to_send=possible_date)
				atext.save()

#############################################
######## Send the texts
#############################################
def send_text(text):
	# Save all outgoing
	tmp_user = UserSetting.objects.all().get(user=text.user)
	addressee = tmp_user.sms_address

	message_to_send = str(text.text)


	past_ten_minutes = datetime.now(pytz.utc) - timedelta(minutes=1)
	out_check = Outgoing.objects.all().filter(text=text).filter(date_sent__gte=past_ten_minutes).count()
	actual_check = ActualText.objects.all().filter(user=text.user).filter(text=text.id).filter(time_sent__gte=past_ten_minutes).count()
	# print("ACUTAL CHECK", actual_check)
	# print("OUTCHECK:", out_check)

	if out_check < 1 and actual_check < 1:
		if tmp_user.send_email_check == True:
			send_mail('',message_to_send, str(EMAIL_HOST_USER), [text.user.email], fail_silently=False)
			text.time_sent = datetime.now(pytz.utc)
			text.save()

			outgoing_tmp = Outgoing(text=text,date_sent=datetime.now(pytz.utc))
			outgoing_tmp.save()
			# print("Sent 1 email")

		if tmp_user.send_text_check == True:
			send_mail('',message_to_send, str("Sentimini <"+EMAIL_HOST_USER+">"), [addressee], fail_silently=False)
			text.time_sent = datetime.now(pytz.utc)
			text.save()

			outgoing_tmp = Outgoing(text=text,date_sent=datetime.now(pytz.utc))
			outgoing_tmp.save()
			print("Sent 1 text")

	
# @periodic_task(run_every=timedelta(seconds=10))

# @app.task

# @periodic_task(run_every=timedelta(seconds=task_seconds_between))
# @app.task
# @task(name="send_texts")
@task()
def send_texts():
	# print("TASK 2 - STARTING send_texts ")
	today_date = datetime.now(pytz.utc)
	#filter out the ones that haven't been sent out yet AND the ones that are suppose to be sent out now
	user_texts = ActualText.objects.filter(time_to_send__lte=datetime.now(pytz.utc)).filter(time_sent=None)
	
	for text in user_texts:
		# YOU WILL HAVE TO ADD SOME CHECKS INTO THIS
		# user specific text (i.e. they texted "stop")

		# This is to remove any old texts that are backed up.
		td = datetime.now(pytz.utc) - text.time_to_send.astimezone(pytz.UTC)
		if td.seconds/60 > 5:
			text.delete()
		else:
			send_text(text)		
		# time specific checks (i.e. sent more than 5 in the last 10 minutes, etc)

		

#############################################
######## GET THE REPLIES
#############################################

def get_first_text_part(msg):
    maintype = msg.get_content_maintype()
    if maintype == 'multipart':
        for part in msg.get_payload():
            if part.get_content_maintype() == 'text':
                return part.get_payload()
    elif maintype == 'text':
        return msg.get_payload()

		
# @periodic_task(run_every=timedelta(seconds=10))

# @app.task

# @periodic_task(run_every=timedelta(seconds=task_seconds_between))
# @app.task
# @task(name="check_email_for_new")
@task()
def check_email_for_new():
	#Set up the email 
	# print("TASK 3 - RECIEVE MAIL")
	if use_gmail == 1:
		mail = imaplib.IMAP4_SSL('imap.gmail.com')
	else:
		mail = imaplib.IMAP4_SSL('imappro.zoho.com')

	#### GMAIL
	# mail = imaplib.IMAP4_SSL('imap.gmail.com')
	# mail.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
	# mail.list()

	#### ZOHO
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
		# print("DOWNLOADING MESSAGES")
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
			# print("NEW INCOMING SAVED")
			mail.store(id, '+FLAGS', '\\Deleted') # flage this for deletion
	mail.expunge() #delete them
	# print("BOX CLEANED")





# @periodic_task(run_every=timedelta(seconds=10))

# @app.task
# @task(name="process_new_mail")
# @periodic_task(run_every=timedelta(seconds=task_seconds_between))
# @app.task
# @task(name="process_new_mail")
@task()
def process_new_mail():
	# print("TASK 4 - PROCESS MAIL")
	Toprocess = Incoming.objects.all().filter(processed=0)
	for tp in Toprocess:
	
		#need conditional
		# print("tp.email_user", tp.email_user)
		if UserSetting.objects.all().filter(phone=tp.email_user).exists():
			if UserSetting.objects.all().filter(phone=tp.email_user).count() == 1:
				working_user = UserSetting.objects.all().get(phone=tp.email_user)	
			else:
				working_user = UserSetting.objects.all().filter(phone=tp.email_user).first()
			
			#check to see if the user wants to stop
			
			############################################################
			############### CHECK FOR RESPONSE AND DETERMINE WHAT IT IS
			############################################################
			# print("tp.email_content ", tp.email_content )
			if tp.email_content is not None: #this is new
				working_text = ActualText.objects.all().filter(user=working_user.user).exclude(time_sent__isnull=True)
				working_text = working_text.filter(time_sent__lte=tp.email_date)
				new_text_conditional = 0
				# print("TEXT CONTENT: ", tp.email_content.lower())
				if len(str(tp.email_content.lower())) < 6:
					if 'stop' in tp.email_content.lower():
						working_user.text_request_stop = True
						working_user.save()

				if len(str(tp.email_content.lower())) < 6:
					if 'start' in tp.email_content.lower():
						working_user.text_request_stop = False
						working_user.save()		

				if len(str(tp.email_content.lower())) > 3:
					if 'new:' in tp.email_content.lower()[:4]:
						default_timing = Timing.objects.all().filter(user=working_user.user).get(default_timing=True)

						if PossibleText.objects.all().filter(user=working_user.user).filter(text=tp.email_content[4:]).count() < 1:
							new_text = PossibleText(user=working_user.user,tmp_save=False,timing=default_timing,text=tp.email_content[4:],date_created=pytz.utc.localize(datetime.now()))
							new_text.save()

						new_text_conditional = 1

				if working_text.count() > 0 and new_text_conditional == 0:
					working_text = working_text.latest('time_sent')

					if working_text.response is None or working_text.response == "":
						# print("first consolidate conditional")
						working_text.time_response = tp.email_date
						working_text.response = tp.email_content
						working_text.save()
						
		tp.processed = 1
		tp.save()
		
		
						