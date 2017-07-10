from django.db import models
from django.conf import settings
import pytz
from datetime import datetime, time
from decimal import *
from django.core.validators import MinValueValidator, MaxValueValidator
from django.template.defaultfilters import slugify

from ent.models import UserSetting, Collection, Timing, IdealText, PossibleText, ActualText

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
	collection = models.ManyToManyField(Collection,blank=True, related_name='person')

	def __str__(self):
		return self.phone_input

	def number_texts(self):	
		PossibleText.objects.all().filter(user=self.person).count()
		
	def number_texts_sent(self):	
		ActualText.objects.all().count()	

class Group(models.Model):
	creator = models.ForeignKey(settings.AUTH_USER_MODEL,blank=True,null=True)
	group = models.CharField(max_length=1000,default='',null=True)
	person = models.ManyToManyField(Person,blank=True)
	collection = models.ManyToManyField(Collection,blank=True,related_name='group')
	ideal_text = models.ManyToManyField(IdealText,blank=True)
	
	def __str__(self):
		return self.group		



	