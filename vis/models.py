from django.db import models
from django.conf import settings
from datetime import datetime
from decimal import *
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
######THE FOLLOWING ARE USED IN THE PLAYGROUND.  THESE ARE NOT REAL DATA BUT SIMULATED DATA 
class EntryDEV(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	test_user = models.CharField(max_length=160,default='',null=True) #This is just the "ANGER" part.  I'm thinking about adding a field for the message sent

	prompt = models.CharField(max_length=160,default='',null=True) #This is just the "ANGER" part.  I'm thinking about adding a field for the message sent
	prompt_type = models.CharField(max_length=160,default='',null=True) #This is the prompt type
	prompt_reply = models.IntegerField(null=True, blank=True) #This is the reply from the user
	prompt_id = models.IntegerField(default=0)
	
	#These are datetime objects.  Should be clear
	time_to_add = models.IntegerField(default=0)
	time_created = models.DateTimeField(blank=True,null=True)
	time_to_send = models.DateTimeField(blank=True,null=True)
	time_to_send_time = models.TimeField(blank=True,null=True)
	time_to_send_circa = models.CharField(max_length=160,default='AM',null=True) #This is just the "ANGER" part.  I'm thinking about adding a field for the message sent
	time_to_send_day = models.CharField(max_length=160,default='',null=True)
	time_sent = models.DateTimeField(blank=True,null=True)
	time_response = models.DateTimeField(blank=True,null=True)
	response_time = models.IntegerField(default=0)

	ready_for_next = models.BooleanField(default=True) #This is a yes/no to determine if the next one shoudl be sent.  This is used primarily to wait for responses (in instruction and in series)
	send_next_immediately = models.BooleanField(default=False) #This is used to determine if the next one should be sent immediately.  Used primarily in instructions and series

	series = models.IntegerField(default=0) #This is a count with range 0-3.  0 =not series, 1-3 = series number.
	failed_series = models.IntegerField(default=0) #This is a yes/no tracking if the series failed (ie the user didn't respond).  I think this used to schedule a new prompt instead of waiting forever.

	#you should have a log of the settings used for each prompt.  This meanings that you'll just reference the usersettings and save that information here everytime you send out a prompt.  in this way you'll be able to log, what settings generated what prompts to do analysis
	
	def __str__(self):
		return self.prompt

#I think for a while that this might be the easiset way to create graphs.  i'll just have throwaway tables to put the working information and then make json out of that.  i have not idea though
class EntryDEVSUM(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	analysis = models.CharField(max_length=160,default='',null=True) #This is just the "ANGER" part.  I'm thinking about adding a field for the message sent
	test_user = models.CharField(max_length=160,default='',null=True) #This is just the "ANGER" part.  I'm thinking about adding a field for the message sent

	prompt = models.CharField(max_length=160,default='',null=True) #This is just the "ANGER" part.  I'm thinking about adding a field for the message sent
	time_to_send_circa = models.CharField(max_length=160,default='AM',null=True) #This is just the "ANGER" part.  I'm thinking about adding a field for the message sent
	time_to_send_day = models.CharField(max_length=160,default='',null=True) #This is just the "ANGER" part.  I'm thinking about adding a field for the message sent
	prompt_type = models.CharField(max_length=160,default='',null=True) #This is the prompt type
	prompt_reply_avg = models.FloatField(default=0.0,null=True) #This is the time the user wakes.  Used to calculate deadtimes
	prompt_reply_count = models.IntegerField(default=0)

	#you should have a log of the settings used for each prompt.  This meanings that you'll just reference the usersettings and save that information here everytime you send out a prompt.  in this way you'll be able to log, what settings generated what prompts to do analysis
	
	def __str__(self):
		return self.prompt	

# This is jsut to have a selector on the vis screen that will 
class EmotionToShow(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	emotion = models.CharField(max_length=160,default='',null=True) #This is the emotion, of course
	emotion_id = models.IntegerField(default=0)
	show_me_graph = models.BooleanField(default=True)
	show_me_user = models.BooleanField(default=True)
	
	def __str__(self):
		return self.emotion		

		#This is the other main workhorse that keeps user preferences.  
class UserSettingDEV(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	setting_name = models.CharField(max_length=300,default='default',null=True)
	num_to_gen = models.IntegerField(default=100)
	begin_date = models.DateTimeField(default=datetime(2000,1,1,0,00))
	

	sleep_time = models.TimeField(default=datetime(2016,1,30,22,00)) #This is the time the user sleeps.  Used to calculate deadtimes
	sleep_duration = models.DecimalField(max_digits=3,decimal_places=2,default=Decimal('8.0')) #This is the time the user wakes.  Used to calculate deadtimes

	respite_until_datetime = models.DateTimeField(blank=True,null=True) #The respite buttons change this field.  Email will only send if now greater than this value
	
	prompts_per_week = models.IntegerField(default=3) #Average number of prompts per day.  User can set this.  Used to calculate the average time between prompts
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

	#these are for modeling the responses
	exp_response_rate = models.DecimalField(max_digits=3, decimal_places=2,default=Decimal('0.6')) #core 8 emotions
	exp_response_time_avg =  models.IntegerField(default=5)
	exp_response_time_min =  models.IntegerField(default=1)
	exp_response_time_max =  models.IntegerField(default=60)
	time_to_declare_lost =  models.IntegerField(default=61)
	
	def __str__(self):
		return self.user.username