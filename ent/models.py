from django.db import models
from django.conf import settings
from datetime import datetime
from decimal import *
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

#Emotion is the model where the emotions are listed out.  Perhaps I will group them or something of that nature later.
class Emotion(models.Model):
	emotion = models.CharField(max_length=160,default='',null=True) #This is the emotion, of course
	emotion_type = models.CharField(max_length=120,default='CORE') #this is the type of emotion.
	#CORE = default set of 5-8 that I will ask about intensively
	#Top100 = set of 100 most frequently used.

	def __str__(self):
		return self.emotion

#This is to allow to add their own prompts
class UserGenPrompt(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	prompt = models.CharField(max_length=160,default='',null=True) 
	date_created = models.DateTimeField(blank=True,null=True)
	active = models.BooleanField(default=True) #Does the user want this sent
	show_user = models.BooleanField(default=False) #Does the user want this deleted?  This doesn't actually delete, but removes the entry from being displayed or referenced
	
	def __str__(self):
		return self.prompt

#These are the instructions to be given at the beginning of the texting. 
#Please note that I want to include more instructions to be periodically given.
class NewUserPrompt(models.Model):
	prompt = models.CharField(max_length=160,default='',null=True)
	prompt_type = models.CharField(max_length=120,default='',null=True) # I don't really know why I have this.
	NUP_seq = models.IntegerField(default=0) #This is to determine the order to text them.
	send_next_immediately = models.BooleanField(default=False) #This is just a switch to tell the task file to send the next one immediately (i.e. randomly generate a time.).  I'm not 100% sure why I have this right now.


#This is just a log of when the user asked for a respite (break from texting)
class Respite(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	date_request = models.DateTimeField(blank=True,null=True)
	respite_type = models.CharField(max_length=120,default='',null=True) #1 day, 3 day, 7 day, start again

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


#This is the main workhorse.  Currently I'm not sure if it is better to have a queue of messages to be sent out or to use this as the queue.  
class Entry(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)

	prompt = models.CharField(max_length=160,default='',null=True) #This is just the "ANGER" part.  I'm thinking about adding a field for the message sent
	prompt_type = models.CharField(max_length=160,default='',null=True) #This is the prompt type
	prompt_reply = models.IntegerField(null=True, blank=True) #This is the reply from the user
	
	#These are datetime objects.  Should be clear
	time_to_add = models.IntegerField(default=0)
	time_created = models.DateTimeField(blank=True,null=True)
	time_to_send = models.DateTimeField(blank=True,null=True)
	time_sent = models.DateTimeField(blank=True,null=True)
	time_response = models.DateTimeField(blank=True,null=True)
	response_time_seconds = models.IntegerField(default=0)

	ready_for_next = models.BooleanField(default=True) #This is a yes/no to determine if the next one shoudl be sent.  This is used primarily to wait for responses (in instruction and in series)
	send_next_immediately = models.BooleanField(default=False) #This is used to determine if the next one should be sent immediately.  Used primarily in instructions and series

	series = models.IntegerField(default=0) #This is a count with range 0-3.  0 =not series, 1-3 = series number.
	failed_series = models.IntegerField(default=0) #This is a yes/no tracking if the series failed (ie the user didn't respond).  I think this used to schedule a new prompt instead of waiting forever.

	#you should have a log of the settings used for each prompt.  This meanings that you'll just reference the usersettings and save that information here everytime you send out a prompt.  in this way you'll be able to log, what settings generated what prompts to do analysis
	
	def __str__(self):
		return self.prompt

#This is the other main workhorse that keeps user preferences.  
class UserSetting(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	send_text = models.BooleanField(default=False) #This is just a yes/no switch.  I think this is set when a user edits contact information and used a high level switch at the beginning of the task file
	teaching_period_on = models.BooleanField(default=True) #This is just a yes/no switch that tells the tasks to get the NUP prompts instead of the usual emotion prompts
	
	text_request_stop = models.BooleanField(default=False) # This is a yes/no switch that stops texts right before the send_email().  It is set when the tasks reads emails.

	phone = models.CharField(max_length=30,default='',null=True) #This is the user phone number
	carrier = models.CharField(blank=True,max_length=100,default='CHANGE ME') #THis is the carrier
	sms_address = models.EmailField(default='',null=True) #This is the address actually used.  Calculated from phone and carrier lookup
	timezone = models.CharField(max_length=30,default='UTC') #THis is the timezone.  User encouraged to update when travelling.  Not sure if I want a stable timezone too.

	sleep_time = models.TimeField(default=datetime(2016,1,30,22,00)) #This is the time the user sleeps.  Used to calculate deadtimes
	sleep_duration = models.DecimalField(max_digits=3,decimal_places=2,default=Decimal('8.0')) #This is the time the user wakes.  Used to calculate deadtimes

	respite_until_datetime = models.DateTimeField(blank=True,null=True) #The respite buttons change this field.  Email will only send if now greater than this value
	
	prompts_per_day = models.IntegerField(default=6) #Average number of prompts per day.  User can set this.  Used to calculate the average time between prompts
	prompt_interval_minute_avg =  models.IntegerField(default=10) # This is calculate by the number of desired prompts / time awake.  
	prompt_interval_minute_min =  models.IntegerField(default=15) # This is largely hidden from users.  Used to define triangular distrubtuion
	prompt_interval_minute_max =  models.IntegerField(default=1000) # This is largely hidden from users.  Used to define triangular distrubtuion

	#these will be the different types of emotion prompts.  These should add up to 1.  These are lower level.  If 50% of prompts are emotions, then X% are for core
	emotion_core_rate = models.DecimalField(max_digits=3, decimal_places=2,default=Decimal('0.6')) #core 8 emotions
	emotion_top100_rate = models.DecimalField(max_digits=3, decimal_places=2,default=Decimal('0.3')) #top 100 word freq emtions
	emotion_other_rate = models.DecimalField(max_digits=3, decimal_places=2,default=Decimal('0.1')) #whateverelse I think is interesting

	# These figure out the type of prompt to give.  
	user_generated_prompt_rate = models.IntegerField(default=0,validators=[MinValueValidator(0), MaxValueValidator(100)])   #Are these from the user generated prompts?
	prompt_multiple_rate = models.DecimalField(max_digits=3, decimal_places=2,default=Decimal('0.2')) #These are the proportion of time a series is given
	instruction_rate = models.DecimalField(max_digits=3, decimal_places=2,default=Decimal('0.2')) #Instructions.  This is just placeholder and I have coded this in yet.
	
	def __str__(self):
		return self.user.username

#This is a basic model that will keep summary information filled out.
class UserSummary(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	age = models.IntegerField(default=18)
	gender = models.CharField(max_length=120,default='',null=True)
	years_of_education = models.IntegerField(default=12)
	sexual_orientation = models.CharField(max_length=120,default='',null=True)
	ethnicity = models.CharField(max_length=120,default='',null=True)
