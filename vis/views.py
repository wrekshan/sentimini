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

from ent.models import PossibleTextSTM, ActualTextSTM, UserSetting, ActualTextLTM
from .models import EntryDEV, UserSettingDEV, EntryDEVSUM, EmotionToShow
from .forms import UserSettingDEVForm, UserSettingDEVForm_RUN, EmotionToShowForm, ExampleFormSetHelper

from sentimini.tasks import set_next_prompt_instruction

from sentimini.sentimini_functions import get_user_summary_info, get_table_emotion_centered, get_graph_data_line_chart, get_graph_data_by_prompt, get_graph_data_day_in_week, get_graph_data_time_of_day, get_graph_data_line_chart_smoothed, get_graph_data_by_prompt_bar
from sentimini.scheduler_functions import generate_random_prompts_to_show

import csv


def user_vis(request):
	if request.user.is_authenticated():	
		magic_simulated_value = 1
		generate_random_prompts_to_show(request,exp_resp_rate=.8,week=0,number_of_prompts=100) #set up 20 random prompts based upon the settings
		
		if ActualTextLTM.objects.filter(user=request.user).count() > 1:
			current_user = request.user

			user_summary_info = get_user_summary_info(request, simulated_val=magic_simulated_value)

			#This gets the average and stuff for emotion centered table
			table_emotion_centered = get_table_emotion_centered(request,simulated_val=magic_simulated_value)

			#This gets the average and stuff for prompt centered table
			table_latest_entry = ActualTextLTM.objects.filter(user=request.user).filter(text_type="user").filter(simulated=magic_simulated_value)
			table_latest_entry = table_latest_entry.order_by('time_sent')

			

			# for poop in formset:
				# print(poop)
			if request.GET.get('export_csv_responses'):
				print("BUTTON PRESED")
				# Create the HttpResponse object with the appropriate CSV header.
				response = HttpResponse(content_type='text/csv')
				response['Content-Disposition'] = 'attachment; filename="sentimini_responses_data.csv"'
				writer = csv.writer(response)

				headers = ["prompt","reply","time_sent"]
				writer.writerow(headers)

				for tmp in table_latest_entry:
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

				for tmp in table_emotion_centered:
					row = [tmp['text'],tmp['response__avg'],tmp['response__count']]
					writer.writerow(row)
				return response
					




			context = {
				'user': request.user,
				'user_summary_info': user_summary_info,
				
			    'table_emotion_centered': table_emotion_centered,
			    'table_latest_entry': table_latest_entry,
			}
			
			return render_to_response('visual.html', context)
		else:
			context = {
				'user': request.user,			
			}

		
			return render_to_response('visual.html',context)

	else:
		return render(request, "index_not_logged_in.html")



