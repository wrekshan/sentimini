from django.db import models
from django.conf import settings
import pytz
from datetime import datetime, time
from decimal import *
from django.core.validators import MinValueValidator, MaxValueValidator

########## NEW AND TO KEEP 
#This just stores the email addresss, the @blah.com, to email texts to person



class Carrier(models.Model):
	carrier = models.CharField(blank=True,max_length=100,default='Verizon')
	sms_address = models.CharField(max_length=100,default='',null=True)
	
	def __str__(self):
		return self.carrier

class Beta(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	content = models.CharField(max_length=5000,default='',null=True)
	date_created = models.DateTimeField(blank=True,null=True)
	
	def __str__(self):
		return self.content		

#This is the other main workhorse that keeps user preferences.  
class UserSetting(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	begin_date = models.DateTimeField(default=datetime(2000,1,1,0,00))
	settings_complete = models.BooleanField(default=False)
	phone_verified = models.BooleanField(default=False)
	send_text = models.BooleanField(default=False) #This is just a yes/no switch.  I think this is set when a user edits contact information and used a high level switch at the beginning of the task file
	send_text_tmp = models.BooleanField(default=False) #This is just a yes/no switch.  I think this is set when a user edits contact information and used a high level switch at the beginning of the task file
	text_request_stop = models.BooleanField(default=False) # This is a yes/no switch that stops texts right before the send_email().  It is set when the tasks reads emails.
	phone_input = models.CharField(max_length=16,default='') #This is the user phone number
	phone = models.CharField(max_length=30,default='',null=True) #This is the user phone number
	carrier = models.CharField(blank=True,max_length=100,default='CHANGE ME') #THis is the carrier
	sms_address = models.EmailField(default='',null=True) #This is the address actually used.  Calculated from phone and carrier lookup
	timezone = models.CharField(max_length=30,default='UTC') #THis is the timezone.  User encouraged to update when travelling.  Not sure if I want a stable timezone too.
	timezone_search = models.CharField(max_length=30,default='UTC') #THis is the timezone.  User encouraged to update when travelling.  Not sure if I want a stable timezone too.
	
	research_check = models.BooleanField(default=False)
	send_email_check = models.BooleanField(default=False)
	send_text_check = models.BooleanField(default=True)

	
	def __str__(self):
		return self.user.username
	

class Tag(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	tag = models.CharField(max_length=160,unique=True,null=True)

	def __str__(self):
		return self.tag


class Timing(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	intended_text = models.CharField(max_length=160,blank=True,null=True)
	repeat_summary = models.CharField(max_length=2000,blank=True,null=True)
	system_time  = models.BooleanField(default=False)
	show_user  = models.BooleanField(default=False)
	default_timing  = models.BooleanField(default=False)
	private  = models.BooleanField(default=False)
	timing = models.CharField(max_length=160,default='')
	description = models.CharField(max_length=160,default='')

	date_start = models.DateField(blank=True,null=True)
	date_end = models.DateField(blank=True,null=True)
	date_start_value = models.CharField(max_length=160,default='')
	date_end_value = models.CharField(max_length=160,default='')
	hour_start = models.TimeField(default=datetime(2016,1,30,9,00))
	hour_end = models.TimeField(default=datetime(2016,1,30,21,00))
	hour_start_value  = models.IntegerField(blank=True,null=True)
	hour_end_value  = models.IntegerField(blank=True,null=True)
	fuzzy  = models.BooleanField(default=False) 
	fuzzy_denomination = models.CharField(max_length=160,default='')
	iti  = models.IntegerField(blank=True,null=True)
	iti_raw  = models.IntegerField(blank=True,null=True)
	iti_noise  = models.IntegerField(blank=True,null=True)

	fuzzy_denomination_start = models.CharField(max_length=160,default='')
	iti_raw_start  = models.IntegerField(blank=True,null=True)
	iti_noise_start  = models.IntegerField(blank=True,null=True)
	
	repeat  = models.BooleanField(default=False) 
	repeat_in_window = models.IntegerField(blank=True,null=True)
	repeat_weeks = models.IntegerField(blank=True,null=True)

	monday  = models.BooleanField(default=True) 
	tuesday  = models.BooleanField(default=True) 
	wednesday  = models.BooleanField(default=True) 
	thursday  = models.BooleanField(default=True) 
	friday  = models.BooleanField(default=True) 
	saturday  = models.BooleanField(default=True) 
	sunday  = models.BooleanField(default=True) 

	def timing_summary(self):
		# return "1 text around every " + str(self.iti_raw) + " " + self.fuzzy_denomination
		if self.hour_start == self.hour_end:
			hours_between = str(self.hour_start.strftime("%-I:%M%p"))
		else:
			hours_between = str(self.hour_start.strftime("%-I:%M%p")) +  " - " + str(self.hour_end.strftime("%-I:%M%p"))
			
		if self.fuzzy == True:
			if self.fuzzy_denomination == "minutes":
				iti_standard = (60 / self.iti_raw) * 24 * 7
			if self.fuzzy_denomination == "hours":
				iti_standard = (24 / self.iti_raw) * 7
			if self.fuzzy_denomination == "days":
				iti_standard = (7 / self.iti_raw)
			if self.fuzzy_denomination == "weeks":
				iti_standard = self.iti_raw
			if self.fuzzy_denomination == "months":
				iti_standard = (self.iti_raw / 4)
			return str(round(iti_standard,2)) + " per week (every " + str(self.iti_raw) + " " + self.fuzzy_denomination + ")\n" + hours_between
		else:
			num_out = int(0)
			weekdays = []
			if self.monday == True:
				num_out = num_out + int(self.repeat_in_window)
				weekdays.append("Monday")
			if self.tuesday == True:
				num_out = num_out + int(self.repeat_in_window)
				weekdays.append("Tuesday")
			if self.wednesday == True:
				num_out = num_out + int(self.repeat_in_window)
				weekdays.append("Wednesday")
			if self.thursday == True:
				num_out = num_out + int(self.repeat_in_window)
				weekdays.append("Thursday")
			if self.friday == True:
				num_out = num_out + int(self.repeat_in_window)
				weekdays.append("Friday")
			if self.saturday == True:
				num_out = num_out + int(self.repeat_in_window)
				weekdays.append("Saturday")
			if self.sunday == True:
				num_out = num_out + int(self.repeat_in_window)
				weekdays.append("Sunday")


			tmp = str(weekdays)
			tmp = str.replace(tmp,'[','')
			tmp = str.replace(tmp,']','')
			tmp = str.replace(tmp,'\'','')
			if len(weekdays) == 7:
				tmp = "all days"
			elif len(weekdays) == 5:
				if self.sunday == False & self.saturday == False:
					tmp = "weekdays"
			elif len(weekdays) == 2:
				if self.sunday == True & self.saturday == True:
					tmp = "weekends"
			
			return str(round(num_out)) + " per week (" + str(self.repeat_in_window) + " on " + str(tmp) + ") \n" + hours_between


	def __str__(self):
		return str(self.id)

	def dow_check(self)	:
		dow_check = 0
		current_day = datetime.now(pytz.utc).strftime("%A")

		if current_day == "Monday":
			if self.monday == True:
				dow_check = 1
			else:
				dow_check = 0	

		if current_day == "Tuesday":
			if self.tuesday == True:
				dow_check = 1
			else:
				dow_check = 0

		if current_day == "Wednesday":
			if self.wednesday == True:
				dow_check = 1
			else:
				dow_check = 0	

		if current_day == "Thursday":
			if self.thursday == True:
				dow_check = 1
			else:
				dow_check = 0

		if current_day == "Friday":
			if self.friday == True:
				dow_check = 1
			else:
				dow_check = 0

		if current_day == "Saturday":
			if self.saturday == True:
				dow_check = 1
			else:
				dow_check = 0

		if current_day == "Sunday":
			if self.sunday == True:
				dow_check = 1
			else:
				dow_check = 0

		return dow_check





class Collection(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	collection = models.CharField(max_length=160,default='')
	collection_name = models.CharField(max_length=160,default='')
	author = models.CharField(max_length=500,default='')
	description = models.CharField(max_length=3000,default='')
	long_description = models.CharField(max_length=3000,default='')
	tag = models.ManyToManyField(Tag,blank=True)
	publish  = models.BooleanField(default=False) 
	explict_save  = models.BooleanField(default=False) 
	intended_tags = models.CharField(max_length=600,blank=True,null=True)

	def __str__(self):
		return self.collection

class PossibleText(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	collection = models.ManyToManyField(Collection,default=1, related_name='texts',blank=True)
	timing = models.ForeignKey(Timing,null=True)
	text = models.CharField(max_length=160,default='')
	input_text = models.CharField(max_length=160,default='')
	date_created = models.DateTimeField(blank=True,null=True)
	date_scheduled = models.DateTimeField(blank=True,null=True)
	tag = models.ManyToManyField(Tag,blank=True)
	active = models.BooleanField(default=True) 
	tmp_save = models.BooleanField(default=True) 
	quick_suggestion = models.BooleanField(default=False) 

	intended_collection = models.CharField(max_length=160,blank=True,null=True)
	intended_tags = models.CharField(max_length=600,blank=True,null=True)
	
	def __str__(self):
		return self.text

	# def burden(self):
	# 	if self.timing.fuzzy==True:
	# 		return (960 / self.timing.iti) / 7
	# 	else:
	# 		if self.timing.repeat_in_window is not None:
	# 			num_out = int(0)
	# 			if self.timing.monday == True:
	# 				num_out = num_out + int(self.timing.repeat_in_window)
	# 			if self.timing.tuesday == True:
	# 				num_out = num_out + int(self.timing.repeat_in_window)
	# 			if self.timing.wednesday == True:
	# 				num_out = num_out + int(self.timing.repeat_in_window)
	# 			if self.timing.thursday == True:
	# 				num_out = num_out + int(self.timing.repeat_in_window)
	# 			if self.timing.friday == True:
	# 				num_out = num_out + int(self.timing.repeat_in_window)
	# 			if self.timing.saturday == True:
	# 				num_out = num_out + int(self.timing.repeat_in_window)
	# 			if self.timing.sunday == True:
	# 				num_out = num_out + int(self.timing.repeat_in_window)

	# 			return (self.timing.repeat_in_window * num_out) / 30
	# 		else:
	# 			return 0


class ActualText(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	# feed = models.ForeignKey(Feed,default=0)
	text = models.ForeignKey(PossibleText,default=0)
	time_to_send = models.DateTimeField(blank=True,null=True)
	time_sent = models.DateTimeField(blank=True,null=True)
	time_response = models.DateTimeField(blank=True,null=True)
	response = models.CharField(max_length=160,null=True,blank=True) #This is the prompt type

	def __str__(self):
		return self.text.text

class QuickSuggestion(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	text = models.ForeignKey(PossibleText,default=0)
	date = models.DateTimeField(blank=True,null=True)
	added = models.BooleanField(default=False)
	rejected = models.BooleanField(default=False)

	def __str__(self):
		return self.text.text

#This is just a log of the outgoing emails
class Outgoing(models.Model):
	date_sent = models.DateTimeField(blank=True,null=True)
	text = models.ForeignKey(ActualText,null=True)




#This is just a log of the incoming emails
class Incoming(models.Model):
	email_user = models.CharField(max_length=120,default='',null=True)
	email_date = models.DateTimeField(blank=True,null=True)
	email_message = models.TextField(null=True)
	email_content = models.TextField(null=True)
	processed = models.IntegerField(default=0) 




class Prompttext(models.Model):
	text = models.CharField(max_length=500,default='How much XXX is in your present moment (0-10)?',null=True) #this is the type of emotion.
	text_type = models.CharField(max_length=500,default='DIM',null=True) #this is the type.  it coudl be different.
	text_percent = models.IntegerField(default=10) #probability that this should be choosen


	def __str__(self):
		return self.text




