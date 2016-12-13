from django.db.models import Avg, Count, F, Case, When
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from datetime import datetime, timedelta
import pytz
from django import forms
from random import random, triangular, randint
from django.core import serializers

from django.forms import modelformset_factory
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
# Create your views here.

from ent.models import PossibleTextSTM, ActualTextSTM, UserSetting, ActualTextLTM, ActualTextSTM_SIM
from .models import EntryDEV, UserSettingDEV, EntryDEVSUM, EmotionToShow
from .forms import UserSettingDEVForm, UserSettingDEVForm_RUN, EmotionToShowForm, ExampleFormSetHelper

from sentimini.tasks import set_next_prompt_instruction

from sentimini.sentimini_functions import get_user_summary_info, get_table_emotion_centered, get_graph_data_line_chart, get_graph_data_by_prompt, get_graph_data_day_in_week, get_graph_data_time_of_day, get_graph_data_line_chart_smoothed, get_graph_data_by_prompt_bar, get_graph_data_histogram, get_graph_data_line_chart_plotly_smooth
from sentimini.scheduler_functions import generate_random_prompts_to_show

import csv


def get_text_summary(user,prompt_id,magic_simulated_value):
	

	texts = ActualTextLTM.objects.all().filter(user=user).filter(simulated=magic_simulated_value).filter(text_id=prompt_id)

	dim = []
	cat = []

	for text in texts:
		if text.response_dim != "" and text.response_dim is not None:
			print("DIM", text.response_dim)
			dim.append(text.response_dim)
		if text.response_cat_bin != "" and text.response_cat_bin is not None:
			print("CAT", text.response_cat_bin)
			cat.append(text.response_cat_bin)


	if len(dim) > 0:
		print("sum_dim: ", sum(dim))
		dim_avg = sum(dim) / len(dim)
		print("dim_avg: ", dim_avg)
	else:
		print("dim_avg: NA")
	
	if len(cat) > 0:
		print("sum_cat: ", sum(cat))
		cat_avg = sum(cat) / len(cat)
		print("cat_avg: ", cat_avg)
	else:
		print("cat_avg: NA")



def text_data_detail_get_context(request,prompt_id,magic_simulated_value,demo):
	magic_simulated_value = magic_simulated_value
	### Here are all the stuff that won't be user specific, but emotion specific
	user_summary_info = get_user_summary_info(request, simulated_val=magic_simulated_value)
	# emotion_name = ActualTextLTM.objects.all().filter(text_id=prompt_id)

	### Here are all the stuff that WILL be user specific, but emotion specific
	graph_data_histogram = get_graph_data_histogram(request=request,simulated_val=magic_simulated_value,prompt_id=prompt_id)

	## AM / PM

	if ActualTextLTM.objects.all().filter(user=request.user).filter(text_id=prompt_id).filter(simulated=magic_simulated_value).count() > 0:
		graph_data_time_of_day = get_graph_data_time_of_day(request=request,simulated_val=magic_simulated_value,prompt_id=prompt_id)

		## WEEKDAY
		graph_data_day_in_week = get_graph_data_day_in_week(request=request,simulated_val=magic_simulated_value,prompt_id=prompt_id)

		## TIME LINE
		graph_data_line_chart_plotly = get_graph_data_line_chart_plotly_smooth(request=request,simulated_val=magic_simulated_value,prompt_id=prompt_id,number_of_days=1)

		get_text_summary(user=request.user,prompt_id=prompt_id,magic_simulated_value = magic_simulated_value)
	else:
		graph_data_time_of_day = 0

		## WEEKDAY
		graph_data_day_in_week = 0

		## TIME LINE
		graph_data_line_chart_plotly = 0

		


	#Table
	table_latest_entry = ActualTextSTM.objects.all().filter(user=request.user).filter(feed_type="user").filter(text_id=prompt_id).filter(simulated=magic_simulated_value)
	table_latest_entry = table_latest_entry.order_by('time_sent')

	
	tmp = ActualTextLTM.objects.all().filter(user=request.user).filter(text_id=prompt_id).first()
	# you have to save 
	emotion_name = tmp.text
	print("FEED ID HERE HERE", tmp.feed_id)





	context = {
	'emotion_name': emotion_name,
	'user_summary_info': user_summary_info,
	'demo': demo,

	"graph_data_histogram": graph_data_histogram,
	"graph_data_time_of_day": graph_data_time_of_day,
	"graph_data_day_in_week": graph_data_day_in_week,
	"graph_data_line_chart_plotly": graph_data_line_chart_plotly,

	"table_latest_entry": table_latest_entry,
	"feed_id": tmp.feed_id,
	"text_id": prompt_id,
		
    }
	return context






def text_data_get_context(request,magic_simulated_value,demo):
	if ActualTextLTM.objects.filter(user=request.user).count() > 0:
		current_user = request.user

		user_summary_info = get_user_summary_info(request, simulated_val=magic_simulated_value)

		#This gets the average and stuff for emotion centered table
		table_emotion_centered = get_table_emotion_centered(request,simulated_val=magic_simulated_value)

		#This gets the average and stuff for prompt centered table
		table_latest_entry = ActualTextLTM.objects.filter(user=request.user).filter(feed_type="user").filter(simulated=magic_simulated_value)
		# table_latest_entry = table_latest_entry.order_by('-time_sent')
		
		context = {
			'user': request.user,
			'user_summary_info': user_summary_info,
			
		    'table_emotion_centered': table_emotion_centered,
		    'table_latest_entry': table_latest_entry,
		    'demo': demo,
		}

		return context


def text_data(request):
	if request.user.is_authenticated():	
		if UserSetting.objects.all().get(user=request.user).new_user_pages < 2:
			return HttpResponseRedirect('/ent/new_user/')

		context = text_data_get_context(request=request, magic_simulated_value=0,demo=0)

		if request.GET.get('export_csv_responses'):
			print("BUTTON PRESED")
			# Create the HttpResponse object with the appropriate CSV header.
			response = HttpResponse(content_type='text/csv')
			response['Content-Disposition'] = 'attachment; filename="sentimini_responses_data.csv"'
			writer = csv.writer(response)

			headers = ["text","response","response_type","time_sent"]
			writer.writerow(headers)


			for tmp in context['table_latest_entry']:
				row = [tmp.text,tmp.response,tmp.response_type,tmp.time_sent]
				writer.writerow(row)
			return response


		if request.GET.get('export_csv_text_centered'):
			print("BUTTON PRESED")
			# Create the HttpResponse object with the appropriate CSV header.
			response = HttpResponse(content_type='text/csv')
			response['Content-Disposition'] = 'attachment; filename="sentimini_text_centered_data.csv"'
			writer = csv.writer(response)

			headers = ["text","response_average","response_counts"]
			writer.writerow(headers)

			for tmp in context['table_emotion_centered']:
				row = [tmp['text'],tmp['response__avg'],tmp['response__count']]
				writer.writerow(row)
			return response

		return render(request,'visual.html', context)

	else:
		return HttpResponseRedirect('/accounts/signup/')



def text_data_detail(request,prompt_id=None):
	if request.user.is_authenticated():	
		#### IS THERE A NEED FOR A SIMULATION
		magic_simulated_value = 0

		

		if ActualTextLTM.objects.filter(user=request.user).filter(text_id=prompt_id).count() > 1:

			context = text_data_detail_get_context(request=request,prompt_id=prompt_id,magic_simulated_value=magic_simulated_value,demo=0)

			table_latest_entry = ActualTextSTM.objects.all().filter(user=request.user).filter(feed_type="user").filter(text_id=prompt_id).filter(simulated=0)
			table_latest_entry = table_latest_entry.order_by('time_sent')



			if request.GET.get('export_csv_responses'):
				print("BUTTON PRESED")
				# Create the HttpResponse object with the appropriate CSV header.
				response = HttpResponse(content_type='text/csv')
				response['Content-Disposition'] = 'attachment; filename="sentimini_responses_data.csv"'
				writer = csv.writer(response)

				headers = ["text","time_sent","feed_name","response"]
				writer.writerow(headers)

				for tmp in table_latest_entry:
					row = [tmp.text,tmp.time_sent,tmp.feed_name,tmp.response]
					writer.writerow(row)
				return response


			return render(request,"text_data_detail_only_table.html", context)

		else:
			tmp = PossibleTextSTM.objects.all().filter(user=request.user).get(id=prompt_id)

			
			

			context = {
				"emotion_name": tmp.text,
				"feed_id": tmp.feed_id,
				"group_id": tmp.group_id,
				"text_id": prompt_id,

			
		    }
	    
			return render(request,"text_data_detail_only_table.html", context)
	else:
		return HttpResponseRedirect('/accounts/signup/')


def text_data_detail_demo(request,prompt_id=None):
	if request.user.is_authenticated():	
		#### IS THERE A NEED FOR A SIMULATION
		magic_simulated_value = 1
		

		if ActualTextLTM.objects.filter(user=request.user).count() > 1:

			context = text_data_detail_get_context(request=request,prompt_id=prompt_id,magic_simulated_value=1,demo=1)

		else:
			context = {
			
		    }
	    
		return render(request,"text_data_detail.html", context)
	else:
		return HttpResponseRedirect('/accounts/signup/')


def text_data_demo(request):
	if request.user.is_authenticated():	
		if ActualTextLTM.objects.filter(user=request.user).filter(simulated=1).count() > 1:
			for ltm in ActualTextLTM.objects.filter(user=request.user).filter(simulated=1):
				ltm.delete()

		if ActualTextSTM_SIM.objects.filter(user=request.user).filter(simulated=1).count() > 1:
			for ltm in ActualTextSTM_SIM.objects.filter(user=request.user).filter(simulated=1):
				ltm.delete()

		generate_random_prompts_to_show(request,exp_resp_rate=.8,week=0,number_of_prompts=100) #set up 20 random prompts based upon the settings

		context = text_data_get_context(request=request, magic_simulated_value=1,demo=1)

		if request.GET.get('export_csv_responses'):
			print("BUTTON PRESED")
			# Create the HttpResponse object with the appropriate CSV header.
			response = HttpResponse(content_type='text/csv')
			response['Content-Disposition'] = 'attachment; filename="sentimini_responses_data.csv"'
			writer = csv.writer(response)

			headers = ["prompt","reply","time_sent"]
			writer.writerow(headers)

			for tmp in context.table_latest_entry:
				row = [tmp.prompt,tmp.prompt_reply,tmp.time_sent]
				writer.writerow(row)
			return response


		if request.GET.get('export_csv_text_centered'):
			print("BUTTON PRESED")
			# Create the HttpResponse object with the appropriate CSV header.
			response = HttpResponse(content_type='text/csv')
			response['Content-Disposition'] = 'attachment; filename="sentimini_text_centered_data.csv"'
			writer = csv.writer(response)

			headers = ["text","response_average","response_counts"]
			writer.writerow(headers)

			for tmp in context.table_emotion_centered:
				row = [tmp['text'],tmp['response__avg'],tmp['response__count']]
				writer.writerow(row)
			return response

		return render_to_response('visual.html', context)

	else:
		return HttpResponseRedirect('/accounts/signup/')


