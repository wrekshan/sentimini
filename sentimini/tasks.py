from __future__ import absolute_import

from celery.task import periodic_task
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


#############################################
######## PERODIC TASK TO SCHEDULE NOW TEXTS
#############################################
@periodic_task(run_every=timedelta(seconds=10))
def schedule_texts():
	print("----- STARTING schedule_texts -----")
	#Specific Timings
	working_texts = PossibleText.objects.all().filter(tmp_save=False).filter(active=True).filter(timing__fuzzy=False).filter(timing__date_start__lte=pytz.utc.localize(datetime.now()))
	for text in working_texts:
		if text.timing.dow_check() == 1:
			if ActualText.objects.all().filter(text=text).filter(time_sent__isnull=True).count()<1:
				# The following conditional is to only schedule texts once a day
				working_settings = UserSetting.objects.all().get(user=text.user)
				user_timezone = pytz.timezone(working_settings.timezone)

				if text.date_scheduled is not None:
					if pytz.utc.localize(datetime.now()) > text.date_scheduled + timedelta(1,0):
						# print("SCHEDULING NEW SPECIFIC TEXT")
						time_window = user_timezone.localize(datetime.combine(datetime.today(), text.timing.hour_end)) - user_timezone.localize(datetime.combine(datetime.today(), text.timing.hour_start))
						scheduled_date = datetime.combine(datetime.today(), text.timing.hour_start)
						seconds_to_add = randint(0,time_window.total_seconds())

						time_to_send_tmp = user_timezone.localize(scheduled_date + timedelta(0,seconds_to_add))
						
						atext = ActualText(user=text.user,text=text)
						atext.time_to_send = time_to_send_tmp.astimezone(pytz.UTC)
						atext.save()

						text.date_scheduled = datetime.now(pytz.utc)
						text.save()
				
				else:
					# print("SCHEDULING NEW SPECIFIC")
					time_window = user_timezone.localize(datetime.combine(datetime.today(), text.timing.hour_end)) - user_timezone.localize(datetime.combine(datetime.today(), text.timing.hour_start))
					# print("TIME WINOW", time_window)
					scheduled_date = datetime.combine(datetime.today(), text.timing.hour_start)
					# print("scheduled_date", scheduled_date)
					seconds_to_add = randint(0,time_window.total_seconds())
					# print("seconds_to_add", seconds_to_add)

					atext = ActualText(user=text.user,text=text)
					time_to_send_tmp = user_timezone.localize(scheduled_date + timedelta(0,seconds_to_add))
					# print("time_to_send_tmp", time_to_send_tmp)
					atext.time_to_send = time_to_send_tmp.astimezone(pytz.UTC)
					# print("atext.time_to_send", atext.time_to_send)
					atext.save()

					text.date_scheduled = datetime.now(pytz.utc)
					text.save()

	#Fuzzy Timings
	working_texts = PossibleText.objects.all().filter(tmp_save=False).filter(active=True).filter(timing__fuzzy=True).filter(timing__date_start__lte=pytz.utc.localize(datetime.now()))
	for text in working_texts:
		if ActualText.objects.all().filter(text=text).filter(time_sent__isnull=True).count()<1:
			print("SCHEDULING NEW FUZZY TEXT")

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

			# THIS IS OLO, AND I THINK IT LEADS TO TEXTING AT NIGHTTIME
			# possible_date = pytz.utc.localize(datetime.now()) + timedelta(0,seconds_to_add)

			# THIS IS NEW AND THINK COULD BE BETTER
			working_settings = UserSetting.objects.all().get(user=text.user)
			user_timezone = pytz.timezone(working_settings.timezone)
			possible_date = pytz.utc.localize(datetime.now()) + timedelta(0,seconds_to_add)

			print("POSSIBLE DATE BEFORE", possible_date)


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
	print("OUTCHECK:", out_check)

	if out_check < 1:
		if tmp_user.send_email_check == True:
			send_mail('',message_to_send,str('system@sentimini.com'), [text.user.email], fail_silently=False)
			text.time_sent = datetime.now(pytz.utc)
			text.save()

			outgoing_tmp = Outgoing(text=text,date_sent=datetime.now(pytz.utc))
			outgoing_tmp.save()
			print("Sent 1 email")

		if tmp_user.send_text_check == True:
			send_mail('',message_to_send,str('system@sentimini.com'), [addressee], fail_silently=False)
			text.time_sent = datetime.now(pytz.utc)
			text.save()

			outgoing_tmp = Outgoing(text=text,date_sent=datetime.now(pytz.utc))
			outgoing_tmp.save()
			print("Sent 1 text")

	
@periodic_task(run_every=timedelta(seconds=10))
def send_texts():
	print("----- STARTING send_texts -----")
	today_date = datetime.now(pytz.utc)
	#filter out the ones that haven't been sent out yet AND the ones that are suppose to be sent out now
	user_texts = ActualText.objects.filter(time_to_send__lte=datetime.now(pytz.utc)).filter(time_sent=None)
	
	for text in user_texts:
		# YOU WILL HAVE TO ADD SOME CHECKS INTO THIS
		# user specific text (i.e. they texted "stop")
		# time specific checks (i.e. sent more than 5 in the last 10 minutes, etc)

		send_text(text)		

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

		
@periodic_task(run_every=timedelta(seconds=2))
def check_email_for_new():
	#Set up the email 
	print("TASK 3 - RECIEVE MAIL")
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
			if UserSetting.objects.all().filter(phone=tp.email_user).count() == 1:
				working_user = UserSetting.objects.all().get(phone=tp.email_user)	
			else:
				working_user = UserSetting.objects.all().filter(phone=tp.email_user).first()
			
			#check to see if the user wants to stop
			print("CHECKING FOR STOP")
			############################################################
			############### CHECK FOR RESPONSE AND DETERMINE WHAT IT IS
			############################################################
			if tp.email_content is not None: #this is new
				working_text = ActualText.objects.all().filter(user=working_user.user).exclude(time_sent__isnull=True)
				working_text = working_text.filter(time_sent__lte=tp.email_date)
				
				if working_text.count() > 0:
					working_text = working_text.latest('time_sent')

					if working_text.response is None or working_text.response == "":
						print("first consolidate conditional")
						working_text.time_response = tp.email_date
						working_text.response = tp.email_content
						working_text.save()
						

		print("Email Processed")
		tp.processed = 1
		tp.save()
		
		
						