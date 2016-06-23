from django.db import models
from django.conf import settings

# Create your models here.
class FAQ(models.Model):
	question = models.CharField(max_length=1000,default='',null=True) 
	answer = models.TextField(default='') 
	category = models.CharField(max_length=1000,default='',null=True) 
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=True) #Just a switch to show user or not
	
	def __str__(self):
		return self.question

class FAQuserquestions(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	typer = models.CharField(max_length=1000,default='FAQ',null=True) 
	question = models.CharField(max_length=1000,default='',null=True) 
	date_created = models.DateTimeField(auto_now_add=True)

