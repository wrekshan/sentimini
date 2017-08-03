from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from random import random, triangular, randint, gauss
import json
from datetime import datetime, timedelta, time, date
import pytz
from allauth.account.adapter import get_adapter, DefaultAccountAdapter
from sentimini.forms import SignupFormWithoutAutofocus
from allauth.account.forms import SignupForm


from ent.models import AlternateText, Quotation, QuickSuggestion, Beta, ActualText, PossibleText, Timing, Carrier, UserSetting, Program, Tag
from django.db.models import Q

import time
import requests
import csv

from consumer.views import get_timing_default, transfer_alt_texts
from .models import Person, Group
from ent.models import IdealText, PossibleText, ActualText, Program, UserSetting



def create_fake_users(request):
	num_users = 10
	num_groups = 3

	#Start fresh
	working_groups = Group.objects.all().filter(creator=request.user)
	for group in working_groups:
		group.delete()

	working_persons = Person.objects.all().filter(creator=request.user)	
	for person in working_persons:
		person.delete()

	#Create blank people and groups
	for i in range(0,num_groups):
		working_group = Group(creator=request.user,group=str("group number " + str(i)))
		working_group.save()

	start_number = 11111111111
	for i in range(0,num_users):
		working_person = Person(creator=request.user, phone_input=str(start_number),display_name=str("Person " + str(i)))
		start_number = start_number + 1
		working_person.save()

		if UserSetting.objects.all().filter(phone=working_person.phone_input).count()>0:
			print("USER FOUND!")
			working_setting = UserSetting.objects.all().filter(phone=working_person.phone_input)[0]
			working_person.person = working_setting.user
		else:
			print("NOT FOUND")

		working_person.save()


		for j in range(0,randint(0, num_groups)):
			working_group = Group.objects.all().filter(creator=request.user).order_by('?')[0]
			working_group.person.add(working_person)
			working_group.save()
		
	return HttpResponseRedirect('/professional/home/')


def transfer_ideal_texts(ideal_text,possible_text):
	print("TRANSFER IDEAL")
	# possible_text.save()
	possible_text.ideal_text = ideal_text
	possible_text.creator = ideal_text.user
	possible_text.timing = ideal_text.timing
	# possible_text.alt_text = ideal_text.ideal_alts
	possible_text.text = ideal_text.text
	possible_text.text_type = ideal_text.text_type
	possible_text.edit_type = ideal_text.edit_type
	possible_text.tmp_save = ideal_text.tmp_save

	if ideal_text.group != None:
		for group in ideal_text.group.all():
			possible_text.group.add(group)

	return possible_text

def save_fake_text(working_person,text):
	tmp = PossibleText(user=working_person.person)
	tmp = transfer_ideal_texts(text,tmp)

	timing = Timing.objects.all().get(id=tmp.timing.id)
	timing.pk=None
	timing.intended_text_input=""
	timing.user=working_person.person
	timing.save()

	tmp.pk=None
	tmp.edit_type="professional_actual"
	tmp.timing=timing
	tmp.user=working_person.person
	tmp.input_text=''
	tmp.tmp_save=False
	tmp.date_created=datetime.now(pytz.utc)
	tmp.save()

	return tmp
	

def create_fake_texts(request):
	num_texts = 10
	num_actual_texts = 10
	num_programs = 3


	#Start Fresh
	working_programs = Program.objects.all().filter(user=request.user)
	for program in working_programs:
		program.delete()

	working_texts = IdealText.objects.all().filter(user=request.user)	
	for text in working_texts:
		text.delete()	

	working_texts = PossibleText.objects.all().filter(creator=request.user)	
	for text in working_texts:
		text.delete()

	working_texts = ActualText.objects.all().filter(user=request.user)	
	for text in working_texts:
		text.delete()	

	#Create some blank programs
	for i in range(0,num_programs):
		working_program = Program(user=request.user,program=str("program "+str(i)), program_name=str("program "+str(i)))
		working_program.description = "This is just a description of the program."
		working_program.save()

	for i in range(0,num_texts):
		working_text = IdealText(user=request.user,edit_type="professional_ideal")
		working_text.text = str("Test text " + str(i))
		working_text.timing = get_timing_default(request)
		working_text.save()

		for j in range(0,randint(0, num_programs)):
			working_program = Program.objects.all().filter(user=request.user).order_by('?')[0]
			working_text.program.add(working_program)

		working_text.save()

	# Assign text and programs to groups

	# Texts from programs
	working_programs = Program.objects.all().filter(user=request.user)
	for i in range(0,3):
		working_program = Program.objects.all().filter(user=request.user).order_by('?')[0]
		for j in range(0,1):
			working_group = Group.objects.all().filter(creator=request.user).order_by('?')[0]
			working_group.program.add(working_program)
			working_group.save()

			for person in working_group.person.all():
				for text in working_program.ideal_texts.all():
					# tmp = Person.objects.all().get(person=person.person)
					person.ideal_text.add(text)
					person.save()
					save_fake_text(person,text)


		for j in range(0,3):
			working_person = Person.objects.all().filter(creator=request.user).order_by('?')[0]
			working_person.program.add(working_program)
			working_person.save()

			for text in working_program.ideal_texts.all():
				working_person.ideal_text.add(text)
				working_person.save()
				save_fake_text(working_person,text)

				# transfer_alt_texts(text,tmp)

	# Just some more texts
	working_texts = IdealText.objects.all().filter(user=request.user).filter(edit_type="professional_ideal")
	for j in range(0,3):
		working_person = Person.objects.all().filter(creator=request.user).order_by('?')[0]
		tmp = save_fake_text(working_person,text)
		transfer_alt_texts(text,tmp)

	#Add programs to groups
	#Add texts to groups	



	# Now just simulate the responses...will have to add time in later
	working_texts = PossibleText.objects.all().filter(creator=request.user).filter(edit_type="professional_actual")
	for text in working_texts:
		tmp = ActualText(user=text.user)
		tmp.text=text
		tmp.response = randint(0,9)
		tmp.time_sent = datetime.now()
		tmp.time_response = datetime.now()
		tmp.save()


		

	return HttpResponseRedirect('/professional/home/')	


# Create your views here.
def home(request):
	context = {}
	if request.user.is_authenticated():	
		if UserSetting.objects.all().filter(user=request.user).count() > 0:
			working_settings = UserSetting.objects.all().get(user=request.user)
			if working_settings.settings_complete == True:
				
				
				context = {
				
					}
				return render(request,"PRO_home.html",context)
			else:
				return HttpResponseRedirect('/consumer/settings/')
		else:
			return HttpResponseRedirect('/consumer/settings/')

	return render(request,"PRO_home.html",context)

def people_and_groups(request):
	context = {}
	if request.user.is_authenticated():	
		if UserSetting.objects.all().filter(user=request.user).count() > 0:
			working_settings = UserSetting.objects.all().get(user=request.user)
			if working_settings.settings_complete == True:
				
				
				context = {
				
					}
				return render(request,"PRO_people_and_groups.html",context)
			else:
				return HttpResponseRedirect('/consumer/settings/')
		else:
			return HttpResponseRedirect('/consumer/settings/')

	return render(request,"PRO_people_and_groups.html",context)	

def texts_and_programs(request):
	context = {}
	if request.user.is_authenticated():	
		if UserSetting.objects.all().filter(user=request.user).count() > 0:
			working_settings = UserSetting.objects.all().get(user=request.user)
			if working_settings.settings_complete == True:
				
				context = {
				
					}
				return render(request,"PRO_texts_and_programs.html",context)
			else:
				return HttpResponseRedirect('/consumer/settings/')
		else:
			return HttpResponseRedirect('/consumer/settings/')

	return render(request,"PRO_texts_and_programs.html",context)		

def group(request,id=None):
	context = {}
	if request.user.is_authenticated():	
		if UserSetting.objects.all().filter(user=request.user).count() > 0:
			working_settings = UserSetting.objects.all().get(user=request.user)
			working_persons = Person.objects.all().filter(creator=request.user)
			if working_settings.settings_complete == True:
				
				context = {
					'working_persons': working_persons,
					'id': id,
					'type': 'group',
				
					}
				return render(request,"PRO_specific.html",context)
			else:
				return HttpResponseRedirect('/consumer/settings/')
		else:
			return HttpResponseRedirect('/consumer/settings/')

	return render(request,"PRO_specific.html",context)

def person(request,id=None):
	context = {}
	if request.user.is_authenticated():	
		if UserSetting.objects.all().filter(user=request.user).count() > 0:
			working_settings = UserSetting.objects.all().get(user=request.user)
			working_persons = Person.objects.all().filter(creator=request.user)
			if working_settings.settings_complete == True:
				
				context = {
					'working_persons': working_persons,
					'id': id,
					'type': 'person',
					}
				return render(request,"PRO_specific.html",context)
			else:
				return HttpResponseRedirect('/consumer/settings/')
		else:
			return HttpResponseRedirect('/consumer/settings/')

	return render(request,"PRO_specific.html",context)

def program(request,id=None):
	context = {}
	if request.user.is_authenticated():	
		if UserSetting.objects.all().filter(user=request.user).count() > 0:
			working_settings = UserSetting.objects.all().get(user=request.user)
			working_persons = Person.objects.all().filter(creator=request.user)
			working_program = Program.objects.all().filter(user=request.user).get(id=id)
			if working_settings.settings_complete == True:
				
				context = {
					'working_program': working_program,
					'working_persons': working_persons,
					'id': id,
					'type': 'program',
				
					}
				return render(request,"PRO_specific.html",context)
			else:
				return HttpResponseRedirect('/consumer/settings/')
		else:
			return HttpResponseRedirect('/consumer/settings/')

	return render(request,"PRO_specific.html",context)

def text(request,id=None):
	context = {}
	if request.user.is_authenticated():	
		if UserSetting.objects.all().filter(user=request.user).count() > 0:
			working_settings = UserSetting.objects.all().get(user=request.user)
			working_persons = Person.objects.all().filter(creator=request.user)
			if working_settings.settings_complete == True:
				
				context = {
					'working_persons': working_persons,
					'id': id,
					'type': 'text',
				
					}
				return render(request,"PRO_specific.html",context)
			else:
				return HttpResponseRedirect('/consumer/settings/')
		else:
			return HttpResponseRedirect('/consumer/settings/')

	return render(request,"PRO_specific.html",context)		


def get_summary_info(request):
	main_context = {} # to build out the specific html stuff
	response_data = {} # to send back to the template
	
	if 'type' in request.POST.keys():
		if request.POST['type'] == "program":
			working_program = Program.objects.all().filter(user=request.user).get(id=int(request.POST['id']))
			working_groups = working_program.group.all()
			working_persons = working_program.person.all()
			working_texts = working_program.ideal_texts.all()

			print("working_groups",working_groups)
			print("working_persons",working_persons)

			main_context['working_groups'] = working_groups
			main_context['working_persons'] = working_persons
			main_context['working_texts'] = working_texts
			main_context['display_name'] = working_program.program_name

			response_data['summary_info'] = render_to_string('PRO_summary_info.html', main_context, request=request)

		elif request.POST['type'] == 'person':
			working_person = Person.objects.all().get(id=int(request.POST['id']))
			working_programs = working_person.program.all()
			working_groups = working_person.group.all()
			working_texts = PossibleText.objects.all().filter(creator=request.user).filter(user=working_person.person)

			print("working_groups",working_groups)
			print("working_programs",working_programs)
			print("working_texts",working_texts)

			main_context['working_programs'] = working_programs
			main_context['working_groups'] = working_groups
			main_context['working_texts'] = working_texts
			main_context['working_person'] = working_person
			
			response_data['ideal_text_list'] = render_to_string('PRO_dt_ideal_text.html', main_context, request=request)
			response_data['summary_info'] = render_to_string('PRO_summary_person.html', main_context, request=request)
		
		elif request.POST['type'] == 'text':
			tmp = IdealText.objects.all().get(id=int(request.POST['id']))
			working_text = PossibleText.objects.all().filter(user=request.user).filter(ideal_text=tmp)
			working_texts = ActualText.objects.all().filter(text=working_text)
			main_context['working_texts'] = working_texts
			main_context['working_persons'] = tmp.person.all()

			main_context['display_name'] = working_text.text


			response_data['pro_filters'] = render_to_string('PRO_summary_info.html', main_context, request=request)

		elif request.POST['type'] == 'group':
			working_group = Group.objects.all().get(id=int(request.POST['id']))

			print("IN FILTER TEXTS", working_group.ideal_text.all())

			main_context['working_persons'] = working_group.person.all()
			main_context['working_texts'] = working_group.possible_text.all()
			main_context['working_group'] = working_group

			person_filters = Q()
			for person in working_group.person.all():
				person_filters.add(Q(user=person.person),Q.OR)

			text_filters = Q()
			for text in working_group.possible_text.all():
				text_filters.add(Q(text=text),Q.OR)

			main_context['working_texts'] = PossibleText.objects.all().filter(person_filters).filter(text_filters)


			response_data['ideal_text_list'] = render_to_string('PRO_dt_ideal_group.html', main_context, request=request)
			response_data['summary_info'] = render_to_string('PRO_summary_group.html', main_context, request=request)


	else:
		response_data['pro_filters'] = render_to_string('PRO_filters.html', main_context, request=request)
	return HttpResponse(json.dumps(response_data),content_type="application/json")



def get_pro_filters(request):
	main_context = {} # to build out the specific html stuff
	response_data = {} # to send back to the template
	response_data['quick_actions'] = render_to_string('PRO_quick_actions.html', main_context, request=request)
	print("KEYS HERE....", request.POST.keys())
	if 'type' in request.POST.keys():
		if request.POST['type'] == "program":
			working_program = Program.objects.all().filter(user=request.user).get(id=int(request.POST['id']))
			working_groups = working_program.group.all()
			working_persons = working_program.person.all()
			working_texts = working_program.ideal_texts.all()

			print("working_groups",working_groups)
			print("working_persons",working_persons)

			main_context['working_groups'] = working_groups
			main_context['working_persons'] = working_persons
			main_context['working_texts'] = working_texts
			response_data['pro_filters'] = render_to_string('PRO_filters_actual_texts.html', main_context, request=request)

		elif request.POST['type'] == 'person':
			working_person = Person.objects.all().get(id=int(request.POST['id']))
			working_programs = working_person.program.all()
			working_groups = working_person.group.all()
			working_texts = PossibleText.objects.all().filter(creator=request.user).filter(user=working_person.person)

			print("working_groups",working_groups)
			print("working_programs",working_programs)

			main_context['working_programs'] = working_programs
			main_context['working_texts'] = working_texts
			response_data['pro_filters'] = render_to_string('PRO_filters_actual_texts.html', main_context, request=request)
		
		elif request.POST['type'] == 'text':
			tmp = IdealText.objects.all().get(id=int(request.POST['id']))
			working_text = PossibleText.objects.all().filter(user=request.user).filter(ideal_text=tmp)
			working_texts = ActualText.objects.all().filter(text=working_text)
			main_context['working_texts'] = working_texts
			main_context['working_persons'] = tmp.person.all()

			response_data['pro_filters'] = render_to_string('PRO_filters_actual_texts.html', main_context, request=request)

		elif request.POST['type'] == 'group':
			working_group = Group.objects.all().get(id=int(request.POST['id']))

			print("IN FILTER TEXTS", working_group.ideal_text.all())


			main_context['working_persons'] = working_group.person.all()
			main_context['working_texts'] = working_group.ideal_text.all()
			response_data['pro_filters'] = render_to_string('PRO_filters_actual_texts.html', main_context, request=request)

			# working_texts = ActualText.objects.all().filter(person__in=working_group.person.all())
			# main_context['working_texts'] = working_texts


			
			# for text in working_group.ideal_texts.all():
				# working_filters.add(Q(text=),Q.OR)


	else:
		response_data['pro_filters'] = render_to_string('PRO_filters.html', main_context, request=request)
	return HttpResponse(json.dumps(response_data),content_type="application/json")

def get_actual_text_feed(request):
	main_context = {} # to build out the specific html stuff
	response_data = {} # to send back to the template

	if request.POST['type'] == 'person':
		working_person = Person.objects.all().get(id=int(request.POST['id']))
		working_texts = ActualText.objects.all().filter(user=working_person.person)
		main_context['working_texts'] = working_texts
		
		print("MODEL THING:", working_person.number_texts_sent())
	
	elif request.POST['type'] == 'program':
		working_program = Program.objects.all().filter(user=request.user).get(id=int(request.POST['id']))
		working_groups = working_program.group.all()
		working_persons = working_program.person.all()

		text_filters = Q()
		for text in working_program.texts.all():
			text_filters.add(Q(text=text),Q.OR)
		
		main_context['working_texts'] = ActualText.objects.all().filter(text_filters)
	
	elif request.POST['type'] == 'group':
		working_group = Group.objects.all().get(id=int(request.POST['id']))
		
		person_filters = Q()
		for person in working_group.person.all():
			person_filters.add(Q(user=person.person),Q.OR)

		text_filters = Q()
		for text in working_group.possible_text.all():
			text_filters.add(Q(text=text),Q.OR)

		main_context['working_texts'] = ActualText.objects.all().filter(person_filters).filter(text_filters)
	
	elif request.POST['type'] == 'text':
		working_text = IdealText.objects.all().get(id=int(request.POST['id']))
		text_filters = Q()
		for text in working_text.possible_text.all():
			text_filters.add(Q(text=text),Q.OR)

		main_context['working_texts'] = ActualText.objects.all().filter(text_filters)


	
	response_data['actual_text_list'] = render_to_string('PRO_dt_actual_text.html', main_context, request=request)	
	return HttpResponse(json.dumps(response_data),content_type="application/json")

def get_pro_feed(request):
	main_context = {} # to build out the specific html stuff
	response_data = {} # to send back to the template

	if 'viewer' in request.POST.keys():
		if request.POST['viewer'] == "Program":
			working_program = Program.objects.all().filter(user=request.user).get(id=int(request.POST['id']))
			working_persons = Person.objects.all().filter(creator=request.user)

			working_texts = working_program.ideal_texts.all()
			main_context['working_texts'] = working_texts
			response_data['text_list'] = render_to_string('PRO_list_text.html', main_context, request=request)
		elif request.POST['viewer'] == "Text":
			working_text = IdealText.objects.all().filter(user=request.user).get(id=int(request.POST['id']))
			working_persons = Person.objects.all().filter(creator=request.user)
			working_user_texts = PossibleText.objects.all().filter(creator=request.user).filter(text=working_text.text)
			working_texts = ActualText.objects.all().filter(text__ideal_text=working_text)
			main_context['working_texts'] = working_texts
			response_data['text_list'] = render_to_string('PRO_list_actual_text.html', main_context, request=request)	
	elif 'basic_view_change' in request.POST.keys():
		print("BASIC VEW CHANGE")
		if request.POST['basic_view'] == 'text_view':
			main_context['working_texts'] = IdealText.objects.all().filter(user=request.user).filter(edit_type="professional_ideal")
			response_data['pro_feed'] = render_to_string('PRO_list_text.html', main_context, request=request)
		if request.POST['basic_view'] == 'program_view':
			main_context['working_programs'] = Program.objects.all().filter(user=request.user)
			response_data['pro_feed'] = render_to_string('PRO_list_program.html', main_context, request=request)
		if request.POST['basic_view'] == 'person_view':
			main_context['working_persons'] = Person.objects.all().filter(creator=request.user)
			response_data['pro_feed'] = render_to_string('PRO_list_person.html', main_context, request=request)
		if request.POST['basic_view'] == 'group_view':
			main_context['working_groups'] = Group.objects.all().filter(creator=request.user)
			response_data['pro_feed'] = render_to_string('PRO_list_group.html', main_context, request=request)			


	else:
		working_persons = Person.objects.all().filter(creator=request.user)
		working_groups = Group.objects.all().filter(creator=request.user)
		working_texts = IdealText.objects.all().filter(user=request.user).filter(edit_type="professional_ideal")
		working_programs = Program.objects.all().filter(user=request.user)

		main_context['working_persons'] = working_persons
		main_context['working_groups'] = working_groups
		main_context['working_texts'] = working_texts
		main_context['working_programs'] = working_programs

		response_data['group_list'] = render_to_string('PRO_list_group.html', main_context, request=request)
		response_data['person_list'] = render_to_string('PRO_list_person.html', main_context, request=request)
		response_data['program_list'] = render_to_string('PRO_list_program.html', main_context, request=request)
		response_data['text_list'] = render_to_string('PRO_list_text.html', main_context, request=request)
	return HttpResponse(json.dumps(response_data),content_type="application/json")

def get_people_and_group_side(request):
	main_context = {} # to build out the specific html stuff
	response_data = {} # to send back to the template

	response_data['people_and_group_side'] = render_to_string('PRO_people_and_group_side.html', main_context, request=request)
	return HttpResponse(json.dumps(response_data),content_type="application/json")

def get_add_new(request):
	main_context = {} # to build out the specific html stuff
	response_data = {} # to send back to the template
	print("ADDING PERSON!!!!")

	if request.POST['type'] == "person_create":
		response_data['add_new'] = render_to_string('PRO_add_person.html', main_context, request=request)
	if request.POST['type'] == "group_create":
		response_data['add_new'] = render_to_string('PRO_add_person.html', main_context, request=request)
	if request.POST['type'] == "text_create":
		response_data['add_new'] = render_to_string('PRO_add_person.html', main_context, request=request)
	if request.POST['type'] == "program_create":
		response_data['add_new'] = render_to_string('PRO_add_person.html', main_context, request=request)		
	return HttpResponse(json.dumps(response_data),content_type="application/json")




