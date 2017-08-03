from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from datetime import *
from django.forms import modelformset_factory
import pytz
from random import random, triangular, randint
from django.db.models import Avg, Count, F, Case, When
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.template.loader import render_to_string
from time import strptime

# FOR SIMULATION
from random import random, triangular, randint, gauss
import plotly.offline as opy
import plotly.graph_objs as go
from plotly.tools import FigureFactory as FF
import plotly.plotly as py
import numpy as np
from numpy import * 
from django.db.models import Q

# Create your views here.

from .models import TextLink, TextDescription, AlternateText, IdealText, PossibleText, ActualText, Program, Tag, Timing, UserSetting
from consumer.views import transfer_alt_texts

def reset_settings_complete(request):
	if request.user.is_superuser:
		working_settings = UserSetting.objects.all()
		for setting in working_settings:
			setting.settings_complete = False
			setting.save()

	return redirect('/admin_panel/')

def pause_all_users(request):
	if request.user.is_superuser:
		working_settings = UserSetting.objects.all()
		for setting in working_settings:
			setting.text_request_stop_tmp = setting.text_request_stop
			setting.text_request_stop = True
			setting.save()

	return redirect('/admin_panel/')

def restore_all_users(request):
	if request.user.is_superuser:
		working_settings = UserSetting.objects.all()
		for setting in working_settings:
			setting.text_request_stop = setting.text_request_stop_tmp
			setting.save()

	return redirect('/admin_panel/')	


			


def update_db_after_import(request):
	print("update_db_after_import")

	#clear away the input text from the people who signed up
	# caneval - I'M PRETTY SURE I DON'T NEED THIS ANY MORE
	working_texts = PossibleText.objects.all().exclude(user=request.user)
	for text in working_texts:
		text.input_text = ''
		text.save()

	working_timings = Timing.objects.all().exclude(user=request.user)	
	for timing in working_timings:
		timing.intended_text = ''
		timing.save()

	# Set up the program
	working_programs = Program.objects.all().filter(user=request.user)
	for program in working_programs:
		if program.intended_tags is not None:
			tags = program.intended_tags.split(',')
			for tag in tags:
				tag = tag.strip()
				if tag !='':
					if Tag.objects.all().filter(user=request.user).filter(tag=tag).count()<1:
						tmp = Tag(tag=tag,user=request.user)
						tmp.save()
					else:
						tmp = Tag.objects.all().get(tag=tag)
					program.tag.add(tmp)

		program.publish=True
		program.save()

	# Set up the timings
	working_timing = Timing.objects.all().filter(user=request.user)
	for timing in working_timing:
		timing.intended_text = timing.intended_text_input
		timing.repeat = True

		if timing.hour_start is not None:
			timing.hour_start_value = (int(str(timing.hour_start.hour))*60) + int(str(timing.hour_start.minute))

		if timing.hour_end is not None:
			timing.hour_end_value = (int(str(timing.hour_end.hour))*60) + int(str(timing.hour_end.minute))	

		
		timing.date_start = datetime.now(pytz.utc)
		timing.repeat_summary = "Repeating X times a day between " + str(timing.hour_start) + " and " + str(timing.hour_end)


		if timing.fuzzy == True:
			if timing.fuzzy_denomination == 'minutes':
				timing.iti = int(timing.iti_raw)
			elif timing.fuzzy_denomination == 'hours':
				timing.iti = int(timing.iti_raw) * 60
			elif timing.fuzzy_denomination == 'days':
				timing.iti = int(timing.iti_raw) * 60 * 24
			elif timing.fuzzy_denomination == 'weeks':
				timing.iti = int(timing.iti_raw) * 60 * 24 * 7
			elif timing.fuzzy_denomination == 'months':
				timing.iti = int(timing.iti_raw) * 60 * 24 * 7 * 4	
		else:
			if timing.repeat_in_window == None:
				timing.repeat_in_window = 1
				
			timing.repeat_summary = "Repeating on average every " + str(timing.iti_raw) + " " + timing.fuzzy_denomination + " between " + str(timing.hour_start) + " and " + str(timing.hour_end)

		timing.save()

	# Set up the texts
	working_texts = IdealText.objects.all().filter(user=request.user)
	for text in working_texts:
		text.text = text.input_text
		# Get the timing object
		print("TEXT", text.text)
		if text.intended_program != None:
			print("PROGRAM NOT NONE")
			timing = Timing.objects.all().filter(user=request.user).get(intended_text=text.text)
			text.timing = timing

			#add the tags
			tags = text.intended_tags.split(',')
			for tag in tags:
				print("----------")
				print("TAG", tag)
				if tag !='':
					if Tag.objects.all().filter(user=request.user).filter(tag=tag).count()<1:
						print("CREATE NEW")
						tmp = Tag(tag=tag,user=request.user)
						tmp.save()
					else:
						print("NOT CREATE NEW")
						tmp = Tag.objects.all().get(tag=tag)
					text.tag.add(tmp)

			#add the programs
			print("INTENDED program", text.intended_program)
			if text.intended_program != "":
				program= Program.objects.all().filter(user=request.user).get(program_name=text.intended_program)
				text.program.add(program)

			text.save()
		else:
			print("PROGRAM IS  NONE")
			timing = Timing.objects.all().filter(user=request.user).get(intended_text=text.text)
			text.timing = timing

			#add the tags
			if text.intended_tags != None:
				tags = text.intended_tags.split(',')
				for tag in tags:
					if tag !='':
						if Tag.objects.all().filter(user=request.user).filter(tag=tag).count()<1:
							tmp = Tag(tag=tag,user=request.user)
							tmp.save()
						else:
							tmp = Tag.objects.all().get(tag=tag)
						text.tag.add(tmp)

			text.save()

	# Process the alternate texts
	working_texts = IdealText.objects.all().filter(user=request.user)
	for working_text in working_texts:
		working_text.alt_text.clear()

		working_alts = AlternateText.objects.all().filter(user=request.user).filter(intended_text=working_text.text)
		for alt in working_alts:
			working_text.alt_text.add(alt)

		working_text.save()


	# Process the descriptions
	working_texts = IdealText.objects.all().filter(user=request.user)
	for working_text in working_texts:
		working_text.description.clear()
		working_text.save()

	for working_text in working_texts:
		working_descriptions = TextDescription.objects.all().filter(user=request.user).filter(intended_text=working_text.text)
		# print("DESCIRPTION ", working_descriptions)
		for description in working_descriptions:
			working_text.description.add(description)

		working_text.save()

	# ALT TEXSTS DESCRIPTION
	working_texts = AlternateText.objects.all().filter(user=request.user)	
	for working_text in working_texts:
		working_text.description.clear()
		working_text.save()


	for working_text in working_texts:
		working_descriptions = TextDescription.objects.all().filter(user=request.user).filter(intended_text=working_text.alt_text)
		for description in working_descriptions:
			working_text.description.add(description)

		working_text.save()	



	# Process the LINKS
	working_texts = IdealText.objects.all().filter(user=request.user)
	for working_text in working_texts:
		working_text.link.clear()
		working_text.save()

	for working_text in working_texts:
		working_links = TextLink.objects.all().filter(user=request.user).filter(intended_text=working_text.text)
		for link in working_links:
			working_text.link.add(link)

		working_text.save()

	# ALT TEXSTS DESCRIPTION
	working_texts = AlternateText.objects.all().filter(user=request.user)	
	for working_text in working_texts:
		working_text.link.clear()
		working_text.save()


	for working_text in working_texts:
		working_links = TextLink.objects.all().filter(user=request.user).filter(intended_text=working_text.alt_text)
		for link in working_links:
			working_text.link.add(link)

		working_text.save()		

	return redirect('/consumer/home/')


def add_to_program(request):
	print("ADDING TO COLECTION")
	response_data = {}

	if 'selected_texts' in request.POST.keys():
		print("LENGTH", len(request.POST['selected_texts']))
		if len(request.POST['selected_texts']) == 0:
			working_program = Program.objects.all().get(id=request.POST['program_name'].split('_')[1])
			working_texts = PossibleText.objects.all().filter(program=working_program)
		else:
			working_texts = request.POST['selected_texts'].split(',')
		

		for text in working_texts:
			print("TEXT: ", text)
			tmp = PossibleText.objects.all().get(id=int(text.split('_')[1]))

			if PossibleText.objects.all().filter(user=request.user).filter(text=tmp.text).count()<1:
				timing = Timing.objects.all().get(id=tmp.timing.id)

				timing.pk=None
				timing.intended_text_input=""
				timing.user=request.user
				timing.save()

				tmp.pk=None
				tmp.timing=timing
				tmp.user=request.user
				tmp.input_text=''
				tmp.tmp_save=False
				tmp.date_created=datetime.now(pytz.utc)
				tmp.save()

				transfer_alt_texts(PossibleText.objects.all().get(id=int(text.split('_')[1])),tmp)
	

	response_data['message'] = "Program Added!"

	return HttpResponse(json.dumps(response_data),content_type="application/json")	



def get_hourly_count_of_prompts(request,program,tmp_date):
	tmp_hours = list(range(0,24))
	# tmp_mins = (0,15,30,45)
	tmp_mins = (0,10,20,30,40,50)

	text_out = []
	num_text_out = []
	text_color = []

	working_texts = PossibleText.objects.all().filter(program=program)

	# print("user_tz: ", user_tz)
	for hr in tmp_hours:
		for mins in tmp_mins:
			min_date = pytz.utc.localize(datetime(tmp_date.year,tmp_date.month,tmp_date.day,hr,mins))
			max_date = pytz.utc.localize(datetime(tmp_date.year,tmp_date.month,tmp_date.day,hr,(mins+9),59))
			# max_date = pytz.utc.localize(datetime(tmp_date.year,tmp_date.month,tmp_date.day,hr,(mins+14),59))

			#get the possible texts for the program
			
			actual_texts = ActualText.objects.all().filter(text__in=working_texts).filter(time_to_send__gte=min_date).filter(time_to_send__lte=max_date)

			# print("program:    ", program)
			# print("working_texts: ", working_texts)
			# print("actual_texts:  ", actual_texts)
							
			if actual_texts.count()>0:
				text_out.append(str(actual_texts.first().text))
				num_text_out.append(1)
			else:
				text_out.append(str(''))
				num_text_out.append(0)


	#This is to get the colors
	distinct_texts = list(set((text_out)))
	
	for text in text_out:

		tset_counter = 0
		for dt in distinct_texts:
			if dt == text:
				# print("THEY ARE EuQAL!!!")
				text_color.append(tset_counter)
			tset_counter = tset_counter + 1

	return text_color, num_text_out, text_out




	
	# distinct_texts = ActualText.objects.all().filter(text__in=working_texts).distinct()
	# # print("distinct_texts", distinct_texts)
	# text_color = []
	# for tmp in text_out:
	# 	# print("IN TMP LOOP", tmp)
	# 	tset_counter = 1
	# 	if tmp != "":
	# 		for w in distinct_texts:
	# 			# print("IN W LOOP", w)
	# 			# print("TMP", tmp)
	# 			if w == tmp:
	# 				print("THEY ARE EQUAL")
	# 				text_color.append(tset_counter)
	# 			tset_counter = tset_counter + 1
	# 	else:
	# 		text_color.append(0)

	# print("TEXT COLOR", text_color)
	





#program PAGE
def get_program_heatmap(request,program):
	num_text_by_date = []
	text_by_date = []
	text_color_by_date =[]
	dateout = []

	tmp_hours = (list(range(0,24)))
	tmp_mins = (0,10,20,30,40,50)
	# tmp_mins = (0,5,15,20,25,30,35,40,45,50,55)
	time_counter = []
	for hr in tmp_hours:
		for mins in tmp_mins:
			time_counter.append(str(str(hr)+ ":" +str(mins)))

	tmp_date = datetime.now(pytz.utc)
	#GO FOR A WEEK
	for tmp_counter in list(range(0,7)):
		text_color, num_text_out, text_out = get_hourly_count_of_prompts(request=request,program=program,tmp_date=tmp_date)
		num_text_by_date.append(num_text_out)
		text_by_date.append(text_out)
		text_color_by_date.append(text_color)

		#98% sure dateout has to be in only the week counter
		dateout.append(str(str(tmp_date.month) + '/' + str(tmp_date.day)))
		tmp_date = tmp_date+timedelta(days=1)


	# z = num_text_by_date
	z = text_color_by_date
	x = time_counter
	y = dateout

	y[0] = 'Today'


	colorscale = [
        # Let first 10% (0.1) of the values have color rgb(0, 0, 0)
        [0, '#FFFFFF'],
        [0.1, '#FFFFFF'],

        # Let values between 10-20% of the min and max of z
        # have color rgb(20, 20, 20)
        #RED
        [0.1, '#b71c1c'],
        [0.2, '#b71c1c'],

        # Values between 20-30% of the min and max of z
        # have color rgb(40, 40, 40)

		#blue
        [0.2, '#42a5f5'],
        [0.3, '#42a5f5'],

		#green
        [0.3, '#4caf50'],
        [0.4, '#4caf50'],
		
		#brown
        [0.4, '#795548'],
        [0.5, '#795548'],

		#grey
        [0.5, '#616161'],
        [0.6, '#616161'],

        [0.6, 'rgb(120, 120, 120)'],
        [0.7, 'rgb(120, 120, 120)'],

        [0.7, 'rgb(140, 140, 140)'],
        [0.8, 'rgb(140, 140, 140)'],

        [0.8, 'rgb(160, 160, 160)'],
        [0.9, 'rgb(160, 160, 160)'],

        [0.9, '#0097a7'],
        [1.0, '#0097a7']
    ]

	# colorscale = [[0,'#3D9970'], [1,'#001f3f']]
	trace1 = go.Heatmap(z=z, x=x, y=y, colorscale=colorscale, colorbar = {'tick0': 0,'dtick': 1 }, text = text_by_date, hoverinfo="text", showscale=False)

	# trace1 = go.Heatmap(z=z, x=x, y=y)
	data=go.Data([trace1])
	layout=go.Layout( xaxis={'title':'Hour', 'ticks': '','nticks':12,'fixedrange': True}, yaxis={'title':'Day', 'ticks': '','fixedrange': True,'autorange': 'reversed'}, margin={'t': 30} )
	figure=go.Figure(data=data,layout=layout)
	div = opy.plot(figure, auto_open=False, output_type='div',show_link=False)

	#work around to remove modebar stuff
	div = div.replace('displaylogo:!0', 'displaylogo:!1')
	div = div.replace('modeBarButtonsToRemove:[]', 'modeBarButtonsToRemove:["sendDataToCloud","hoverCompareCartesian"]')

	print("z",z)
	print("x",x)
	print("y",y)
	print("text_color_by_date",text_color_by_date)


	return div

def get_display_program(request):
	main_context = {} # to build out the specific html stuff
	response_data = {} # to send back to the template

	key = 1
	program_info = {}

	working_filters = Q()

	if 'program_switch' in request.POST.keys():
		if request.POST['program_switch'] == "true":
			print("program TRUE")
			working_filters.add(Q(user=request.user),Q.AND)
			# working_program = Program.objects.all().filter(user=request.user)
			main_context['program_switch_check'] = "true"
		else:
			working_filters.add(Q(publish=True),Q.AND)
			# working_program = Program.objects.all().filter(publish=True)

	if 'program_tags' in request.POST.keys():
		working_tags = request.POST['program_tags'].split(',')
		main_context['searched_tags'] = request.POST['program_tags']

		for tag in working_tags:
			print("TAG", tag)
			print("TAG", str(tag).split("_")[0] )
			if str(tag).split("_")[0] == "tag":
				tmp = Tag.objects.all().filter(tag=str(tag).split("_")[1])
				working_filters.add(Q(tag__in=tmp),Q.AND)
			else:
				print("NAME", tag.split("_"))
				working_filters.add(Q(program=str(tag).split("_")[1]),Q.AND)

	working_program = Program.objects.all().filter(working_filters)

	for program in working_program:
		program_list = {}
		program_list = {
			"program": program,
			# "heatmap": get_program_heatmap(request=request,program=program)
		}

		program_info[key] = program_list
		key = key + 1

	program_info = tuple(program_info.items())
	main_context['program_info'] = program_info

	#These are for the search bar
	main_context['program_names'] = Program.objects.all().filter(publish=True)
	main_context['working_tags'] = Tag.objects.all().filter(program__in=program.objects.all().filter(publish=True)).distinct()



	response_data["program"] = render_to_string('program_display.html', main_context, request=request)
	
	# else
	return HttpResponse(json.dumps(response_data),content_type="application/json")	







def save_program_explicit(request):
	print("HI")

def save_program(request):
	print("SAVE program!")
	response_data = {}

	###### NAME
	if 'id' in request.POST.keys():
		print("ID IN POST")
		if request.POST['id'] != "":
			print("ID NOT NONE")
			working_program = Program.objects.all().get(id=request.POST['id'])
		else:
			print("ID NONE")
			if 'program_name' in request.POST.keys():
				print("program NAME IN POST")
				working_program = program(program=request.POST['program_name'])
				working_program.save()
	
	###### DESCRIPTION
	if 'program_description' in request.POST.keys():
		working_program.description = request.POST['program_description']

	###### TAGS
	if 'tag_vals' in request.POST.keys():
		working_tags = request.POST['tag_vals'].split(',')
		print("SAVE TEXT WORKING TAG", working_tags)
		for tag in working_tags:
			print("TAG", tag)
			if Tag.objects.all().filter(tag=tag).count()>0:
				working_tag = Tag.objects.all().get(tag=tag)
			else:
				working_tag = Tag(user=request.user, tag=tag)
				working_tag.save()

			working_program.tag.add(working_tag)
    
	print("request.POST.keys()", request.POST.keys())
	###### SELECTED TEXTS
	if 'selected_text[]' in request.POST.keys():
		print("SELECTED TEXT VAL", request.POST['selected_text[]'])

		if request.POST['selected_text[]'] != "":
			print("SELECTED TEXT VAL", request.POST['selected_text[]'])
			working_text = PossibleText.objects.all().filter(user=request.user).get(id=int(request.POST['selected_text[]']))
			working_program.texts.add(working_text)


	####### PUBLISH
	# 'publish_switch'		

	if 'publish_switch' in request.POST.keys():
		print()
		if request.POST['publish_switch'] == "true":
			working_program.publish = True
		else:
			working_program.publish = False

	working_program.save()
	print("working_program id put back: ", working_program.id)

	all_possible_texts = PossibleText.objects.all().filter(user=request.user)

	context = {
		'id': working_program.id,
		'working_program': working_program,
		'all_possible_texts': all_possible_texts,
	}
	response_data['active_texts'] = render_to_string('program_active_texts.html', context, request=request)
	response_data['id'] = working_program.id,

	return HttpResponse(json.dumps(response_data),content_type="application/json")	




def get_create_program(request):
	main_context = {} # to build out the specific html stuff
	response_data = {} # to send back to the template

	main_context['working_tags'] =  Tag.objects.all()

	if 'id' in request.POST.keys():
		print("ID HERE", request.POST['id'])
		if request.POST['id'] != None:
			if request.POST['id'] != '':
				main_context['editing_program'] = Program.objects.all().filter(user=request.user).get(id=int(request.POST['id']))


				tmp_tags = Program.objects.all().filter(user=request.user).get(id=int(request.POST['id'])).tag

				tags = []
				for tag in tmp_tags.all():
					tags.append(tag.tag)

				main_context['tags'] = tags
			

	main_context['working_program'] = Program.objects.all()
	main_context['all_possible_texts'] = PossibleText.objects.all().filter(user=request.user).exclude(text__exact='')

	response_data["program"] = render_to_string('program_create.html', main_context, request=request)
	
	# else
	return HttpResponse(json.dumps(response_data),content_type="application/json")	

def program_create_scaffold(request,id=None):
	if request.user.is_authenticated():	

		context = {
			"working_program": Program.objects.all(),
			"id": id,
		}			

		return render(request,"program_create_scaffold.html",context)
	else:

		context = {
			"working_program": Program.objects.all().filter(publish=True),
			
		}			

		return render(request,"programs_not_user.html",context)


def add_new_text(request,id=None):
	if request.user.is_authenticated():	

		working_texts = PossibleText.objects.all()


		context = {
			"working_texts": working_texts,
			"id": id,
		}			

		return render(request,"add_new_texts.html",context)
	else:
		context = {
			
		}			

		return render(request,"add_new_texts.html",context)



def program(request):
	if request.user.is_authenticated():	

		context = {
			"working_program": Program.objects.all(),
		}			

		return render(request,"program.html",context)
	else:
		context = {
			
		}			

		return render(request,"program.html",context)



#This is used in scheduling fuzzy texts.  Changes the date object to within the timewindow
def time_window_check(text,possible_date):
	working_settings = UserSetting.objects.all().get(user=text.user)
	user_timezone = pytz.timezone(working_settings.timezone)
	
	# date_today = datetime.now(pytz.utc).astimezone(user_timezone)
	# time_window = user_timezone.localize(datetime.combine(date_today, text.timing.hour_end)) - user_timezone.localize(datetime.combine(date_today, text.timing.hour_start))
	# scheduled_date = user_timezone.localize(datetime.combine(date_today, text.timing.hour_start))

	# This is new a should work
	date_today = datetime.now(pytz.utc).astimezone(user_timezone)

	starting_time = user_timezone.localize(datetime.combine(date_today, text.timing.hour_start))
	starting_time = starting_time.astimezone(pytz.UTC)

	ending_time = user_timezone.localize(datetime.combine(date_today, text.timing.hour_end))
	ending_time = ending_time.astimezone(pytz.UTC)


	# OLD AND I THINK LEADS TO BAD TIMING
	# starting_time = user_timezone.localize(datetime.combine(possible_date.date(),text.timing.hour_start))
	# ending_time = user_timezone.localize(datetime.combine(possible_date.date(),text.timing.hour_end))

	# print("starting_time",starting_time)
	# print("possible_date",possible_date)
	# print("ending_time",ending_time)


	if not starting_time < possible_date < ending_time:
		if possible_date < starting_time:
			# print("LESS THAN START TIME")
			window_diff = starting_time - possible_date
			possible_date = possible_date + timedelta(hours=0,minutes=0,seconds=window_diff.seconds*2)
		else:
			# print("MORE THAN START TIME")
			date_today = datetime.now(pytz.utc).astimezone(user_timezone)

			time_window = user_timezone.localize(datetime.combine(date_today, text.timing.hour_end)) - user_timezone.localize(datetime.combine(date_today, text.timing.hour_start))
			scheduled_date = starting_time + timedelta(hours=24) 
			if text.timing.iti > time_window.total_seconds():
				seconds_to_add = randint(0,time_window.total_seconds())
			else:
				seconds_to_add = randint(0,(60*text.timing.iti))
			

			possible_date = scheduled_date + timedelta(0,seconds_to_add)
			
	return(possible_date)


#Checks for specific repeat.  Is it on or before date?
def date_check_fun(text,tmp_date):
	date_check = 0

	if text.timing.date_start is not None and text.timing.date_end is not None:
		if tmp_date.date() >= text.timing.date_start and tmp_date.date() <= text.timing.date_end:
			date_check = 1
		else:
			date_check = 0

	if text.timing.date_start is not None:
		if tmp_date.date() >= text.timing.date_start:
			date_check = 1
		else:
			date_check = 0	

	if text.timing.date_end is not None:
		if tmp_date.date() <= text.timing.date_end:
			date_check = 1
		else:
			date_check = 0			

	return date_check			

#Checks for specific repeat.  Is it on dow of week?
def dow_check_fun(text,tmp_date):
	dow_check = 0
	current_day = tmp_date.strftime("%A")

	if current_day == "Monday" and text.timing.monday == True:
		dow_check = 1
	else:
		dow_check = 0	

	if current_day == "Tuesday" and text.timing.tuesday == True:
		dow_check = 1
	else:
		dow_check = 0

	if current_day == "Wednesday" and text.timing.wednesday == True:
		dow_check = 1
	else:
		dow_check = 0	

	if current_day == "Thursday" and text.timing.thursday == True:
		dow_check = 1
	else:
		dow_check = 0

	if current_day == "Friday" and text.timing.friday == True:
		dow_check = 1
	else:
		dow_check = 0

	if current_day == "Saturday" and text.timing.saturday == True:
		dow_check = 1
	else:
		dow_check = 0

	if current_day == "Sunday" and text.timing.sunday == True:
		dow_check = 1
	else:
		dow_check = 0

	return dow_check


def simulate_reponses(request):
	actual_texts = ActualText.objects.all().filter(user=request.user)

	response_rate = 70
	response_time = 15

	for text in actual_texts:
		text.time_sent = text.time_to_send
		if randint(0,99) < response_rate:
			tmp_RT = gauss(response_time,response_time*1.2)
			if tmp_RT < 0:
				tmp_RT = randint(0,2)
		
			text.time_response = text.time_to_send + timedelta(0,tmp_RT)
			text.response = randint(0,10)

		text.save()

#THis is just an easy way to build out the tasks
def simulate(request):
	# actual_texts = ActualText.objects.all().filter(user=request.user)
	# actual_texts.delete()


	#Specific Timings
	working_texts = PossibleText.objects.all().filter(active=True).filter(timing__fuzzy=False).filter(timing__date_start__lte=pytz.utc.localize(datetime.now()))
	for text in working_texts:
		if text.timing.dow_check() == 1:
			if ActualText.objects.all().filter(text=text).filter(time_sent__isnull=True).count()<1:
				time_window = pytz.utc.localize(datetime.combine(date.today(), text.timing.hour_end)) - pytz.utc.localize(datetime.combine(date.today(), text.timing.hour_start))
				scheduled_date = datetime.combine(date.today(), text.timing.hour_start)
				seconds_to_add = randint(0,time_window.total_seconds())

				atext = ActualText(user=request.user,text=text)
				atext.time_to_send = scheduled_date + timedelta(0,seconds_to_add)
				atext.save()

	#Fuzzy Timings
	# working_texts = PossibleText.objects.all().filter(active=True).filter(timing__fuzzy=True).filter(timing__date_start__lte=pytz.utc.localize(datetime.now()))
	working_texts = PossibleText.objects.all().filter(active=True).filter(timing__fuzzy=True)
	for text in working_texts:
		if ActualText.objects.all().filter(text=text).filter(time_sent__isnull=True).count()<1:

			# Get the timing info
			ITI_noise_tmp = text.timing.iti_noise/100
			ITI_mean = text.timing.iti
			max_minutes = ITI_mean + (ITI_mean*ITI_noise_tmp)
			min_minutes = ITI_mean - (ITI_mean*ITI_noise_tmp)

			# Add seconds
			seconds_to_add = 60 * int(triangular(min_minutes, max_minutes, ITI_mean))
			possible_date = pytz.utc.localize(datetime.now()) + timedelta(0,seconds_to_add)

			possible_date = time_window_check(text,possible_date)
			date_check = date_check_fun(text,possible_date)

			print("DATE CHECK", date_check)

			if date_check == 1:
				atext = ActualText(user=request.user,text=text,time_to_send=possible_date)
				atext.save()
					





	print("DOW CHECK", text.timing.dow_check())


	# filter(date_end__gt=pytz.utc.localize(datetime.now()))
	print("COUNT", working_texts.count())
	return redirect('admin_panel')



#note that this is to simulate
def simulate_old(request):
	actual_texts = ActualText.objects.all().filter(user=request.user)
	actual_texts.delete()
	working_texts = PossibleText.objects.all().filter(user=request.user)
	simulation_days = 90

	#Generate the texts
	for text in working_texts:
		if text.timing.repeat == False:
			# Get the times for the single text
			time_window = pytz.utc.localize(datetime.combine(date.today(), text.timing.hour_end)) - pytz.utc.localize(datetime.combine(date.today(), text.timing.hour_start))
			scheduled_date = datetime.combine(text.timing.date_start, text.timing.hour_start)
			seconds_to_add = randint(0,time_window.total_seconds())

			#initial and determine when to send
			atext = ActualText(user=request.user,text=text)
			atext.time_to_send = scheduled_date + timedelta(0,seconds_to_add)
			atext.save()
			# print("Single Text Save!")
		else:
			#Repeats
			if text.timing.fuzzy == True:
				print("FUZZY", text.text)
				
				ITI_noise_tmp = text.timing.iti_noise/100
				ITI_mean = text.timing.iti
				max_minutes = ITI_mean + (ITI_mean*ITI_noise_tmp)
				min_minutes = ITI_mean - (ITI_mean*ITI_noise_tmp)

				start_date = datetime.now(pytz.utc)
				latest_date = pytz.utc.localize(datetime.combine(start_date.date(), text.timing.hour_start))
				time_passed = latest_date - start_date

				easy_counter = 1
				while easy_counter < simulation_days:
				# while (time_passed.days) < 8:
					seconds_to_add = 60 * int(triangular(min_minutes, max_minutes, ITI_mean))
					possible_date = latest_date + timedelta(0,seconds_to_add)

					possible_date = time_window_check(text,possible_date)
					date_check = date_check_fun(text,possible_date)

					print(date_check)

					if date_check == 1:
						atext = ActualText(user=request.user,text=text,time_to_send=possible_date)
						atext.save()
					
					# Flow control options
					latest_date = possible_date
					easy_counter = easy_counter + 1
			else:
				print("SPECIFIC REPEAT ", text.text)
				tmp_date = datetime.now(pytz.utc)
				for day_count in range(0,simulation_days):
					schedule_text_switch = 0

					#Date check
					date_check = date_check_fun(text,tmp_date)
					
					#Day of week check	
					dow_check = dow_check_fun(text,tmp_date)	
					

					#Check for the different conditions
					if dow_check == 1 and date_check == 1:
						# Schedule the texts!
						for i in range(0,text.timing.repeat_in_window):

							time_window = datetime.combine(tmp_date.date(), text.timing.hour_end) - datetime.combine(tmp_date.date(), text.timing.hour_start)
							scheduled_date = datetime.combine(tmp_date.date(), text.timing.hour_start)
							seconds_to_add = randint(0,time_window.total_seconds())

							#initial and determine when to send
							atext = ActualText(user=request.user,text=text)
							atext.time_to_send = scheduled_date + timedelta(0,seconds_to_add)
							atext.save()

					
					#flow control
					tmp_date = tmp_date + timedelta(days=1)


	simulate_reponses(request)
	return redirect('feed')
	



def about(request):
	if request.user.is_authenticated():	

		working_texts = PossibleText.objects.all()

		context = {
			"working_texts": working_texts,
		}			

		return render(request,"landing.html",context)
	else:
		context = {
			
		}			

		return render(request,"landing.html",context)






