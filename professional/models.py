from django.db import models
from django.conf import settings
import pytz
from datetime import datetime, time
from decimal import *
from django.core.validators import MinValueValidator, MaxValueValidator
from django.template.defaultfilters import slugify

from ent.models import UserSetting, Program, Timing, IdealText, PossibleText, ActualText

# Create your models here.
class Person(models.Model):
	creator = models.ForeignKey(settings.AUTH_USER_MODEL,blank=True,null=True,related_name='pro_user')
	person = models.ForeignKey(settings.AUTH_USER_MODEL,blank=True,null=True)
	display_name = models.CharField(max_length=100,default='')
	first_name = models.CharField(max_length=100,default='')
	last_name = models.CharField(max_length=100,default='')
	phone_input = models.CharField(max_length=16,default='')
	verified = models.BooleanField(default=False)
	accepted = models.BooleanField(default=False)
	program = models.ManyToManyField(Program,blank=True, related_name='person')
	ideal_text  = models.ManyToManyField(IdealText,blank=True, related_name='person')

	def __str__(self):
		return self.phone_input

	def number_texts(self):	
		return PossibleText.objects.all().filter(creator=self.creator).filter(user=self.person).count()
		
	def number_texts_sent(self):
		working_texts = PossibleText.objects.all().filter(creator=self.creator).filter(user=self.person)
		return ActualText.objects.all().filter(text__in=working_texts).count()

	def number_texts_replies(self):	
		working_texts = PossibleText.objects.all().filter(creator=self.creator).filter(user=self.person)
		return ActualText.objects.all().filter(text__in=working_texts).filter(response__isnull=False).count()	

	def response_rate(self):
		working_texts = PossibleText.objects.all().filter(creator=self.creator).filter(user=self.person)
		sent = ActualText.objects.all().filter(text__in=working_texts).count()
		response = ActualText.objects.all().filter(text__in=working_texts).filter(response__isnull=False).count()
		if sent > 0:
			return 100*(round(response/sent,2))
		else:
			return "NA"

class Group(models.Model):
	creator = models.ForeignKey(settings.AUTH_USER_MODEL,blank=True,null=True)
	group = models.CharField(max_length=1000,default='',null=True)
	person = models.ManyToManyField(Person,blank=True,related_name='group')
	program = models.ManyToManyField(Program,blank=True,related_name='group')
	ideal_text = models.ManyToManyField(IdealText,blank=True,related_name='group')
	possible_text = models.ManyToManyField(PossibleText,blank=True,related_name='group')
	
	def __str__(self):
		return self.group		



	