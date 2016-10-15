from django.db import models
from django.conf import settings


# Create your models here.
class Sentimini_help(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	display_order = models.IntegerField(default=0)
	help_name = models.CharField(max_length=300,default="Text")
	help_content = models.TextField(max_length=10000,default="Default content")
	help_type = models.CharField(max_length=300,default="Glossary")
	major_cat = models.CharField(max_length=300,default="Settings")
	starting_item = models.IntegerField(default=0)
	
	def __str__(self):
		return self.help_name



class Measure(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	name = models.CharField(max_length=300,default="Set Name")
	measure = models.CharField(max_length=300,default="Measure Name")
	super_measure = models.CharField(max_length=300,default="Super Measure")
	measure_type = models.CharField(max_length=300,default="Dimensional")
	population = models.CharField(max_length=300,default="Group")
	minval = models.IntegerField(default=0)
	maxval = models.IntegerField(default=10)
	mean = models.IntegerField(default=5)
	sd = models.IntegerField(default=3)
	distr = models.CharField(max_length=300,default="Normal")
	response_rate = models.IntegerField(default=60)
	


class Business(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	name = models.CharField(max_length=300,default="Business Set 1")
	con_price_per_outgoing = models.DecimalField(default=.00350, max_digits=5, decimal_places=5)
	con_price_per_inccming = models.DecimalField(default=.00000,max_digits=5, decimal_places=5)
	con_number_outgoing_per_free_per_day = models.IntegerField(default=2)
	con_number_ingoing_per_free_per_day = models.IntegerField(default=1)
	con_number_outgoing_per_paid_per_day = models.IntegerField(default=10)
	con_number_ingoing_per_paid_per_day = models.IntegerField(default=6)
	con_conversation_rate_to_paid = models.DecimalField(default = .010,max_digits=3, decimal_places=3)
	con_return_per_paying_user_per_month = models.IntegerField(default=10)
	static_human_cost_per_month = models.IntegerField(default=5800)
	static_server_cost_per_month = models.IntegerField(default=150)
	static_other_cost_per_month = models.IntegerField(default=150)



class Blog(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	author = models.CharField(max_length=1000,default="William Rekshan")
	title = models.CharField(max_length=1000,default='',null=True) 
	description = models.TextField(max_length=10000,default='Default Description') 
	content = models.TextField(max_length=100000,default='Default Content Here') 
	date_created = models.DateTimeField(blank=True,null=True)
	date_altered = models.DateTimeField(blank=True,null=True)
