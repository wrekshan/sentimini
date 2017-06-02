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
		return self.carrier		

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





# #This is the major spot to keep the texts.  
# class GroupSetting(models.Model):
# 	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
# 	ideal_id = models.IntegerField(default=0) 
# 	group_name = models.CharField(max_length=30,default='user') 
# 	unique_group_name = models.CharField(max_length=30,default='user') 
# 	group_type = models.CharField(max_length=30,default='library') 
# 	passcode = models.CharField(max_length=30,default='library') 
# 	viewable = models.BooleanField(default=False) 
# 	joinable = models.BooleanField(default=False) 
# 	editable = models.BooleanField(default=False) 
# 	feeds = models.CharField(max_length=30,default='user') 
# 	user_state =  models.CharField(max_length=100,default='activate') 

# 	#extra
# 	description =  models.CharField(max_length=1000,default='',null=True) 
	
# 	def __str__(self):
# 		return self.group_name

# class FeedSetting(models.Model):
# 	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
# 	feed_name = models.CharField(max_length=300,default='',null=True) 
# 	unique_feed_name = models.CharField(max_length=300,default='',null=True) 
# 	feed_type = models.CharField(max_length=30,default='user') 
# 	feed_id = models.IntegerField(default=0) 
# 	group_name = models.CharField(max_length=120,default='basic',null=True) #basic, kt, other
# 	group_id = models.IntegerField(default=0) 

# 	#stuff
# 	viewable = models.BooleanField(default=False) 
# 	joinable = models.BooleanField(default=False) 
# 	editable = models.BooleanField(default=False) 

# 	#Extra
# 	texts_per_week = models.IntegerField(default=3,validators=[MinValueValidator(0), MaxValueValidator(100)]) 
# 	time_to_declare_lost =  models.IntegerField(default=15)
# 	description =  models.CharField(max_length=1000,default='',null=True) 
# 	description_long =  models.CharField(max_length=10000,default='',null=True) 
# 	tags = models.CharField(max_length=3000,default='',null=True) 
# 	ordering_num =  models.IntegerField(default=0) 
# 	user_state =  models.CharField(max_length=100,default='activate') 
# 	number_of_texts_in_set =  models.IntegerField(default=1)
# 	delete_this = models.BooleanField(default=False) 
# 	active =  models.IntegerField(default=1) 
# 	text_interval_minute_avg =  models.IntegerField(default=10) 
# 	text_interval_minute_min =  models.IntegerField(default=15) 
# 	text_interval_minute_max =  models.IntegerField(default=1000) 
	
	
# 	def __str__(self):
# 		return self.feed_name

# class PossibleTextSTM(models.Model):
# 	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
# 	feed_name = models.CharField(max_length=300,default='user generated',null=True)
# 	unique_feed_name = models.CharField(max_length=30,default='',null=True) 
# 	show_user = models.BooleanField(default=False) 
# 	feed_id = models.IntegerField(default=0)
# 	group_name = models.CharField(max_length=120,default='basic',null=True) #basic, kt, other
# 	group_id = models.IntegerField(default=0)
# 	feed_type = models.CharField(max_length=120,default='library',null=True) #library, system, or user

# 	#unique
# 	text = models.CharField(max_length=160,default='',null=True) 
# 	text_importance = models.IntegerField(default=1,validators=[MinValueValidator(0), MaxValueValidator(100)]) #This should add up to 100% for each emotion
# 	response_type = models.CharField(max_length=100,default='Open') 
	
# 	#extra
# 	csv_id = models.IntegerField(default=0)
# 	system_text = models.IntegerField(default=0)
# 	date_created = models.DateTimeField(blank=True,null=True)
# 	date_altered = models.DateTimeField(blank=True,null=True)
	
# 	def __str__(self):
# 		return self.text

# class ActualTextSTM(models.Model):
# 	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
# 	text_id = models.IntegerField(default=0)
# 	textstore_id = models.IntegerField(default=0)
# 	feed_id = models.IntegerField(default=0)
# 	feed_name = models.CharField(max_length=300,default='',null=True) #This is the user phone number
# 	feed_type = models.CharField(max_length=120,default='user',null=True) #user or system
# 	system_text = models.IntegerField(default=0)
	
# 	text = models.CharField(max_length=160,default='',null=True) #This is the emotion, of course
# 	response = models.CharField(max_length=160,default='',null=True,blank=True) #This is the prompt type
# 	response_type = models.CharField(max_length=100,default='Open') 
	
# 	time_to_send = models.DateTimeField(blank=True,null=True)
# 	time_sent = models.DateTimeField(blank=True,null=True)
# 	simulated = models.IntegerField(default=0) #this is so that I can develop on the model, but not wait forever for texts.
# 	time_response = models.DateTimeField(blank=True,null=True)
# 	response_time = models.IntegerField(default=0)
# 	series = models.IntegerField(default=0) #This is a count with range 0-3.  0 =not series, 1-3 = series number.
# 	time_to_add = models.IntegerField(default=0)
# 	failed_series = models.IntegerField(default=0) #This is a yes/no tracking if the series failed (ie the user didn't respond).  I think this used to schedule a new prompt instead of waiting forever.
# 	ready_for_next = models.IntegerField(default=0) #This is a yes/no to determine if the next one shoudl be sent.  This is used primarily to wait for responses (in instruction and in series)
# 	consolidated = models.IntegerField(default=0)

# 	def __str__(self):
# 		return self.text



# class ActualTextSTM_SIM(models.Model):
# 	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
# 	text_id = models.IntegerField(default=0)
# 	textstore_id = models.IntegerField(default=0)
# 	feed_id = models.IntegerField(default=0)
# 	feed_name = models.CharField(max_length=300,default='',null=True) #This is the user phone number
# 	feed_type = models.CharField(max_length=120,default='user',null=True) #user or system
# 	system_text = models.IntegerField(default=0)
# 	notuser = models.IntegerField(default=0)
	
# 	text = models.CharField(max_length=160,default='',null=True) #This is the emotion, of course
# 	response = models.CharField(max_length=160,default='',null=True,blank=True) #This is the prompt type
# 	response_type = models.CharField(max_length=100,default='Open') 
	
# 	time_to_send = models.DateTimeField(blank=True,null=True)
# 	time_sent = models.DateTimeField(blank=True,null=True)
# 	simulated = models.IntegerField(default=0) #this is so that I can develop on the model, but not wait forever for texts.
# 	time_response = models.DateTimeField(blank=True,null=True)
# 	response_time = models.IntegerField(default=0)
# 	series = models.IntegerField(default=0) #This is a count with range 0-3.  0 =not series, 1-3 = series number.
# 	time_to_add = models.IntegerField(default=0)
# 	failed_series = models.IntegerField(default=0) #This is a yes/no tracking if the series failed (ie the user didn't respond).  I think this used to schedule a new prompt instead of waiting forever.
# 	ready_for_next = models.IntegerField(default=0) #This is a yes/no to determine if the next one shoudl be sent.  This is used primarily to wait for responses (in instruction and in series)
# 	consolidated = models.IntegerField(default=0)

# 	def __str__(self):
# 		return self.text







# #This is the long term storage of the texts.  this is intended to keep a log of all of the texts a person may want.
# class PossibleTextLTM(models.Model):
# 	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
# 	text = models.CharField(max_length=160,default='',null=True) #This is the emotion, of course

# 	feed_id = models.IntegerField(default=0)
# 	feed_name = models.CharField(max_length=300,default='',null=True) #This is the user phone number
# 	feed_type = models.CharField(max_length=120,default='user',null=True) #user or system
# 	text_set = models.CharField(max_length=30,default='',null=True) #This is the user phone number
# 	text_type = models.CharField(max_length=120,default='library',null=True) #user or system
# 	system_text = models.IntegerField(default=0)
# 	text_importance = models.IntegerField(default=1,validators=[MinValueValidator(0), MaxValueValidator(100)]) #This should add up to 100% for each emotion
# 	response_type = models.CharField(max_length=100,default='Open') 
# 	show_user = models.BooleanField(default=False) #Does the user want this deleted?  This doesn't actually delete, but removes the entry from being displayed or referenced
# 	date_created = models.DateTimeField(blank=True,null=True)
# 	date_altered = models.DateTimeField(blank=True,null=True)
# 	stm_id = models.IntegerField(default=0)

# 	def __str__(self):
# 		return self.text

# #




# class ActualTextLTM(models.Model):
# 	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
# 	text_id = models.IntegerField(default=0)
# 	stm_id = models.IntegerField(default=0)
# 	textstore_id = models.IntegerField(default=0)
# 	feed_id = models.IntegerField(default=0)
# 	feed_name = models.CharField(max_length=300,default='',null=True) #This is the user phone number
# 	text = models.CharField(max_length=160,default='',null=True) #This is the emotion, of course
# 	feed_type = models.CharField(max_length=120,default='user',null=True) #user or system
# 	response_type = models.CharField(max_length=100,default='Open') 
# 	response = models.CharField(max_length=160,default='',null=True) #This is the prompt type
# 	response_cat = models.CharField(max_length=160,default='',null=True) #This is the prompt type
# 	response_cat_bin = models.IntegerField(blank=True,null=True) #This is the prompt type
# 	response_dim = models.IntegerField(null=True, blank=True) #This is the reply from the user
# 	response_time = models.IntegerField(default=0)
# 	time_response = models.DateTimeField(blank=True,null=True)
# 	time_to_send = models.DateTimeField(blank=True,null=True)
# 	time_to_send_circa = models.CharField(max_length=160,default='AM',null=True)
# 	time_to_send_day = models.CharField(max_length=160,default='',null=True)
# 	time_sent = models.DateTimeField(blank=True,null=True)
# 	simulated = models.IntegerField(default=0) #this is so that I can develop on the model, but not wait forever for texts.
# 	time_to_add = models.IntegerField(default=0)
# 	series = models.IntegerField(default=0) #This is a count with range 0-3.  0 =not series, 1-3 = series number.
# 	failed_series = models.IntegerField(default=0) #This is a yes/no tracking if the series failed (ie the user didn't respond).  I think this used to schedule a new prompt instead of waiting forever.

# 	def __str__(self):
# 		return self.text		


# #This is just a log of when the user asked for a respite (break from texting)
# class Respite(models.Model):
# 	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
# 	date_request = models.DateTimeField(blank=True,null=True)
# 	respite_type = models.CharField(max_length=120,default='',null=True) #1 day, 3 day, 7 day, start again







# class Ontology(models.Model):
# 	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
# 	ontological_type = models.CharField(max_length=300,default='prompt',null=True) #I.E. instruction or prompt
# 	ontological_name= models.CharField(max_length=300,default='system',null=True) #I.E. Default, List One, Depression List
# 	prompt_set = models.CharField(max_length=300,default='',null=True) #I.E. Core, Expanded, Open
# 	prompt_set_percent = models.IntegerField(default=0,validators=[MinValueValidator(0), MaxValueValidator(100)]) #This should add up to 100% for each ontological_set
# 	prompt_set_percent_calc = models.IntegerField(default=0,validators=[MinValueValidator(0), MaxValueValidator(100)]) #This should add up to 100% for each ontological_set

# 	def __str__(self):
# 		return self.prompt_set


# class UserGenPromptFixed(models.Model):
# 	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
# 	prompt = models.CharField(max_length=160,default='',null=True) 
# 	date_created = models.DateTimeField(blank=True,null=True)
# 	hr_range = models.IntegerField(default='1') #This should add up to 100% for each emotion

# 	active = models.BooleanField(default=True) #Does the user want this sent
# 	response_type = models.CharField(blank=True,max_length=100,default='Open') #THis is the carrier
# 	show_user = models.BooleanField(default=False) #Does the user want this deleted?  This doesn't actually delete, but removes the entry from being displayed or referenced


# 	repeat_denomination = models.CharField(blank=True,max_length=100,default='day') #THis is the carrier
# 	repeat_number = models.IntegerField(default='1') #This should add up to 100% for each emotion

# 	begin_datetime =  models.DateTimeField(default=datetime.now, blank=True)
# 	end_datetime = models.DateTimeField(default=datetime(2020,1,1,0,00))

	
# 	def __str__(self):
# 		return self.prompt		



# #This is just needed to display the respo;nse types
# class ResponseTypeStore(models.Model):
# 	response_type = models.CharField(blank=True,max_length=100,default='0 to 10')
# 	ordering_num = models.IntegerField(default=0) #probability that this should be choosen	
# 	def __str__(self):
# 		return self.response_type



