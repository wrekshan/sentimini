from django.db import models
from django.conf import settings
from datetime import datetime, time
from decimal import *
from django.core.validators import MinValueValidator, MaxValueValidator


#This is the major spot to keep the texts.  
class GroupSetting(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	ideal_id = models.IntegerField(default=0) 
	group_name = models.CharField(max_length=30,default='user') 
	unique_group_name = models.CharField(max_length=30,default='user') 
	group_type = models.CharField(max_length=30,default='library') 
	passcode = models.CharField(max_length=30,default='library') 
	viewable = models.BooleanField(default=False) 
	joinable = models.BooleanField(default=False) 
	editable = models.BooleanField(default=False) 
	feeds = models.CharField(max_length=30,default='user') 
	user_state =  models.CharField(max_length=100,default='activate') 

	#extra
	description =  models.CharField(max_length=1000,default='',null=True) 
	
	def __str__(self):
		return self.group_name

class FeedSetting(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	feed_name = models.CharField(max_length=300,default='',null=True) 
	unique_feed_name = models.CharField(max_length=300,default='',null=True) 
	feed_type = models.CharField(max_length=30,default='user') 
	feed_id = models.IntegerField(default=0) 
	group_name = models.CharField(max_length=120,default='basic',null=True) #basic, kt, other
	group_id = models.IntegerField(default=0) 

	#stuff
	viewable = models.BooleanField(default=False) 
	joinable = models.BooleanField(default=False) 
	editable = models.BooleanField(default=False) 

	#Extra
	texts_per_week = models.IntegerField(default=3,validators=[MinValueValidator(0), MaxValueValidator(100)]) 
	time_to_declare_lost =  models.IntegerField(default=15)
	description =  models.CharField(max_length=1000,default='',null=True) 
	description_long =  models.CharField(max_length=10000,default='',null=True) 
	tags = models.CharField(max_length=3000,default='',null=True) 
	ordering_num =  models.IntegerField(default=0) 
	user_state =  models.CharField(max_length=100,default='activate') 
	number_of_texts_in_set =  models.IntegerField(default=1)
	delete_this = models.BooleanField(default=False) 
	active =  models.IntegerField(default=1) 
	text_interval_minute_avg =  models.IntegerField(default=10) 
	text_interval_minute_min =  models.IntegerField(default=15) 
	text_interval_minute_max =  models.IntegerField(default=1000) 
	
	
	def __str__(self):
		return self.feed_name

class PossibleTextSTM(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	feed_name = models.CharField(max_length=30,default='user generated',null=True)
	unique_feed_name = models.CharField(max_length=30,default='',null=True) 
	show_user = models.BooleanField(default=False) 
	feed_id = models.IntegerField(default=0)
	group_name = models.CharField(max_length=120,default='basic',null=True) #basic, kt, other
	group_id = models.IntegerField(default=0)
	feed_type = models.CharField(max_length=120,default='library',null=True) #library, system, or user

	#unique
	text = models.CharField(max_length=160,default='',null=True) 
	text_importance = models.IntegerField(default=1,validators=[MinValueValidator(0), MaxValueValidator(100)]) #This should add up to 100% for each emotion
	response_type = models.CharField(max_length=100,default='Open') 
	
	#extra
	csv_id = models.IntegerField(default=0)
	system_text = models.IntegerField(default=0)
	date_created = models.DateTimeField(blank=True,null=True)
	date_altered = models.DateTimeField(blank=True,null=True)
	
	def __str__(self):
		return self.text

class ActualTextSTM(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	text_id = models.IntegerField(default=0)
	textstore_id = models.IntegerField(default=0)
	feed_id = models.IntegerField(default=0)
	feed_name = models.CharField(max_length=30,default='',null=True) #This is the user phone number
	feed_type = models.CharField(max_length=120,default='user',null=True) #user or system
	system_text = models.IntegerField(default=0)
	
	text = models.CharField(max_length=160,default='',null=True) #This is the emotion, of course
	response = models.CharField(max_length=160,default='',null=True,blank=True) #This is the prompt type
	response_type = models.CharField(max_length=100,default='Open') 
	
	time_to_send = models.DateTimeField(blank=True,null=True)
	time_sent = models.DateTimeField(blank=True,null=True)
	simulated = models.IntegerField(default=0) #this is so that I can develop on the model, but not wait forever for texts.
	time_response = models.DateTimeField(blank=True,null=True)
	response_time = models.IntegerField(default=0)
	series = models.IntegerField(default=0) #This is a count with range 0-3.  0 =not series, 1-3 = series number.
	time_to_add = models.IntegerField(default=0)
	failed_series = models.IntegerField(default=0) #This is a yes/no tracking if the series failed (ie the user didn't respond).  I think this used to schedule a new prompt instead of waiting forever.
	ready_for_next = models.IntegerField(default=0) #This is a yes/no to determine if the next one shoudl be sent.  This is used primarily to wait for responses (in instruction and in series)
	consolidated = models.IntegerField(default=0)

	def __str__(self):
		return self.text



class ActualTextSTM_SIM(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	text_id = models.IntegerField(default=0)
	textstore_id = models.IntegerField(default=0)
	feed_id = models.IntegerField(default=0)
	feed_name = models.CharField(max_length=30,default='',null=True) #This is the user phone number
	feed_type = models.CharField(max_length=120,default='user',null=True) #user or system
	system_text = models.IntegerField(default=0)
	
	text = models.CharField(max_length=160,default='',null=True) #This is the emotion, of course
	response = models.CharField(max_length=160,default='',null=True,blank=True) #This is the prompt type
	response_type = models.CharField(max_length=100,default='Open') 
	
	time_to_send = models.DateTimeField(blank=True,null=True)
	time_sent = models.DateTimeField(blank=True,null=True)
	simulated = models.IntegerField(default=0) #this is so that I can develop on the model, but not wait forever for texts.
	time_response = models.DateTimeField(blank=True,null=True)
	response_time = models.IntegerField(default=0)
	series = models.IntegerField(default=0) #This is a count with range 0-3.  0 =not series, 1-3 = series number.
	time_to_add = models.IntegerField(default=0)
	failed_series = models.IntegerField(default=0) #This is a yes/no tracking if the series failed (ie the user didn't respond).  I think this used to schedule a new prompt instead of waiting forever.
	ready_for_next = models.IntegerField(default=0) #This is a yes/no to determine if the next one shoudl be sent.  This is used primarily to wait for responses (in instruction and in series)
	consolidated = models.IntegerField(default=0)

	def __str__(self):
		return self.text







#This is the long term storage of the texts.  this is intended to keep a log of all of the texts a person may want.
class PossibleTextLTM(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	text = models.CharField(max_length=160,default='',null=True) #This is the emotion, of course

	feed_id = models.IntegerField(default=0)
	feed_name = models.CharField(max_length=30,default='',null=True) #This is the user phone number
	feed_type = models.CharField(max_length=120,default='user',null=True) #user or system
	text_set = models.CharField(max_length=30,default='',null=True) #This is the user phone number
	text_type = models.CharField(max_length=120,default='library',null=True) #user or system
	system_text = models.IntegerField(default=0)
	text_importance = models.IntegerField(default=1,validators=[MinValueValidator(0), MaxValueValidator(100)]) #This should add up to 100% for each emotion
	response_type = models.CharField(max_length=100,default='Open') 
	show_user = models.BooleanField(default=False) #Does the user want this deleted?  This doesn't actually delete, but removes the entry from being displayed or referenced
	date_created = models.DateTimeField(blank=True,null=True)
	date_altered = models.DateTimeField(blank=True,null=True)
	stm_id = models.IntegerField(default=0)

	def __str__(self):
		return self.text

#




class ActualTextLTM(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	text_id = models.IntegerField(default=0)
	stm_id = models.IntegerField(default=0)
	textstore_id = models.IntegerField(default=0)
	feed_id = models.IntegerField(default=0)
	feed_name = models.CharField(max_length=30,default='',null=True) #This is the user phone number
	text = models.CharField(max_length=160,default='',null=True) #This is the emotion, of course
	feed_type = models.CharField(max_length=120,default='user',null=True) #user or system
	response_type = models.CharField(max_length=100,default='Open') 
	response = models.CharField(max_length=160,default='',null=True) #This is the prompt type
	response_cat = models.CharField(max_length=160,default='',null=True) #This is the prompt type
	response_cat_bin = models.IntegerField(blank=True,null=True) #This is the prompt type
	response_dim = models.IntegerField(null=True, blank=True) #This is the reply from the user
	response_time = models.IntegerField(default=0)
	time_response = models.DateTimeField(blank=True,null=True)
	time_to_send = models.DateTimeField(blank=True,null=True)
	time_to_send_circa = models.CharField(max_length=160,default='AM',null=True)
	time_to_send_day = models.CharField(max_length=160,default='',null=True)
	time_sent = models.DateTimeField(blank=True,null=True)
	simulated = models.IntegerField(default=0) #this is so that I can develop on the model, but not wait forever for texts.
	time_to_add = models.IntegerField(default=0)
	series = models.IntegerField(default=0) #This is a count with range 0-3.  0 =not series, 1-3 = series number.
	failed_series = models.IntegerField(default=0) #This is a yes/no tracking if the series failed (ie the user didn't respond).  I think this used to schedule a new prompt instead of waiting forever.

	def __str__(self):
		return self.text		


#This is just a log of when the user asked for a respite (break from texting)
class Respite(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	date_request = models.DateTimeField(blank=True,null=True)
	respite_type = models.CharField(max_length=120,default='',null=True) #1 day, 3 day, 7 day, start again


#This is the other main workhorse that keeps user preferences.  
class UserSetting(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	begin_date = models.DateTimeField(default=datetime(2000,1,1,0,00))
	send_text = models.BooleanField(default=False) #This is just a yes/no switch.  I think this is set when a user edits contact information and used a high level switch at the beginning of the task file
	text_request_stop = models.BooleanField(default=False) # This is a yes/no switch that stops texts right before the send_email().  It is set when the tasks reads emails.
	phone_input = models.CharField(max_length=16,default='') #This is the user phone number
	phone = models.CharField(max_length=30,default='',null=True) #This is the user phone number
	carrier = models.CharField(blank=True,max_length=100,default='CHANGE ME') #THis is the carrier
	sms_address = models.EmailField(default='',null=True) #This is the address actually used.  Calculated from phone and carrier lookup
	timezone = models.CharField(max_length=30,default='UTC') #THis is the timezone.  User encouraged to update when travelling.  Not sure if I want a stable timezone too.
	sleep_time = models.TimeField(default=datetime(2016,1,30,22,00)) #This is the time the user sleeps.  Used to calculate deadtimes
	wake_time = models.TimeField(default=datetime(2016,1,30,22,00)) #This is the time the user sleeps.  Used to calculate deadtimes

	sleep_duration = models.IntegerField(default=8)
	respite_until_datetime = models.DateTimeField(blank=True,null=True) #The respite buttons change this field.  Email will only send if now greater than this value
	texts_per_week = models.IntegerField(default=3) #Average number of prompts per day.  User can set this.  Used to calculate the average time between prompts
	new_user_pages = models.IntegerField(default=0) #Average number of prompts per day.  User can set this.  Used to calculate the average time between prompts
	send_email_check = models.BooleanField(default=False)
	send_text_check = models.BooleanField(default=True)

	active_experiences = models.CharField(max_length=5000,default='',null=True) #This is the user phone number
	

	#these are for modeling the responses
	exp_response_rate = models.DecimalField(max_digits=3, decimal_places=2,default=Decimal('0.6')) #core 8 emotions
	exp_response_time_avg =  models.IntegerField(default=5)
	exp_response_time_min =  models.IntegerField(default=1)
	exp_response_time_max =  models.IntegerField(default=60)

	def __str__(self):
		return self.user.username
	






class Ontology(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	ontological_type = models.CharField(max_length=300,default='prompt',null=True) #I.E. instruction or prompt
	ontological_name= models.CharField(max_length=300,default='system',null=True) #I.E. Default, List One, Depression List
	prompt_set = models.CharField(max_length=300,default='',null=True) #I.E. Core, Expanded, Open
	prompt_set_percent = models.IntegerField(default=0,validators=[MinValueValidator(0), MaxValueValidator(100)]) #This should add up to 100% for each ontological_set
	prompt_set_percent_calc = models.IntegerField(default=0,validators=[MinValueValidator(0), MaxValueValidator(100)]) #This should add up to 100% for each ontological_set

	def __str__(self):
		return self.prompt_set


class UserGenPromptFixed(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	prompt = models.CharField(max_length=160,default='',null=True) 
	date_created = models.DateTimeField(blank=True,null=True)
	hr_range = models.IntegerField(default='1') #This should add up to 100% for each emotion

	active = models.BooleanField(default=True) #Does the user want this sent
	response_type = models.CharField(blank=True,max_length=100,default='Open') #THis is the carrier
	show_user = models.BooleanField(default=False) #Does the user want this deleted?  This doesn't actually delete, but removes the entry from being displayed or referenced


	repeat_denomination = models.CharField(blank=True,max_length=100,default='day') #THis is the carrier
	repeat_number = models.IntegerField(default='1') #This should add up to 100% for each emotion

	begin_datetime =  models.DateTimeField(default=datetime.now, blank=True)
	end_datetime = models.DateTimeField(default=datetime(2020,1,1,0,00))

	
	def __str__(self):
		return self.prompt		



#This is just needed to display the respo;nse types
class ResponseTypeStore(models.Model):
	response_type = models.CharField(blank=True,max_length=100,default='0 to 10')
	ordering_num = models.IntegerField(default=0) #probability that this should be choosen	
	def __str__(self):
		return self.response_type




#This just stores the email addresss, the @blah.com, to email texts to person
class Carrier(models.Model):
	carrier = models.CharField(blank=True,max_length=100,default='Verizon')
	sms_address = models.CharField(max_length=100,default='',null=True)
	
	def __str__(self):
		return self.carrier

#This is just a log of the incoming emails
class Incoming(models.Model):
	email_user = models.CharField(max_length=120,default='',null=True)
	email_date = models.DateTimeField(blank=True,null=True)
	email_message = models.TextField(null=True)
	email_content = models.TextField(null=True)
	processed = models.IntegerField(default=0) 

#This is just a log of the outgoing emails
class Outgoing(models.Model):
	addressee = models.CharField(max_length=120,default='',null=True)
	date_sent = models.DateTimeField(blank=True,null=True)
	message = models.TextField(null=True)
	entry_id = models.IntegerField(blank=True,null=True)



class Prompttext(models.Model):
	text = models.CharField(max_length=500,default='How much XXX is in your present moment (0-10)?',null=True) #this is the type of emotion.
	text_type = models.CharField(max_length=500,default='DIM',null=True) #this is the type.  it coudl be different.
	text_percent = models.IntegerField(default=10) #probability that this should be choosen


	def __str__(self):
		return self.text


