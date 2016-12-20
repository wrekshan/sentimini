from datetime import date, datetime, timedelta
from random import random, triangular, randint, gauss
from django.db.models import Avg, Count, F, Case, When
from random import shuffle
import pytz

import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse

from ent.models import UserSetting, ActualTextSTM, PossibleTextSTM, Ontology, Prompttext, UserGenPromptFixed, ActualTextLTM, FeedSetting, ActualTextSTM_SIM
import plotly.offline as opy
import plotly.graph_objs as go
from plotly.tools import FigureFactory as FF
import plotly.plotly as py
import numpy as np
from numpy import * 

from sentimini.tasks import generate_random_minutes
########### SCHEDULING AND DATA FUNCTIONS




def get_graph_data_line_chart_business_model(working_busy):
	# peepz = (1,100,1000,5000,10000,15000,20000,25000,3000)
	


	# peepz = range(0,50000,1000)

	peepz = []
	costz=[]
	texting_costz=[]
	returnz = []
	target = []

	cost_per_month = 100
	return_per_month = 0
	number_people = 1000
	while cost_per_month > return_per_month and number_people < 1000000:
		peepz.append(number_people)
		number_of_users = number_people
		number_of_free = number_of_users*(1-working_busy.con_conversation_rate_to_paid)
		number_of_paid = number_of_users*working_busy.con_conversation_rate_to_paid

		cost_free_out_day = number_of_free * working_busy.con_number_outgoing_per_free_per_day * working_busy.con_price_per_outgoing
		cost_free_in_day = number_of_free * working_busy.con_number_ingoing_per_free_per_day * working_busy.con_price_per_inccming

		cost_paid_out_day = number_of_paid * working_busy.con_number_outgoing_per_paid_per_day * working_busy.con_price_per_outgoing
		cost_paid_in_day = number_of_paid * working_busy.con_number_ingoing_per_paid_per_day * working_busy.con_price_per_inccming

		cost_day = cost_free_out_day + cost_free_in_day + cost_paid_out_day + cost_paid_in_day

		texting_cost_per_month = cost_day * 30

		return_per_month = number_of_paid*working_busy.con_return_per_paying_user_per_month

		cost_per_month = texting_cost_per_month+working_busy.static_human_cost_per_month+working_busy.static_server_cost_per_month+working_busy.static_other_cost_per_month

		texting_costz.append(int(texting_cost_per_month))
		costz.append(int(cost_per_month))
		returnz.append(int(return_per_month))

		number_people = number_people + 1000

	

	#Graph
	trace0 = go.Scatter(x = peepz,y = costz,mode = 'lines',	name = 'Total Costs')
	trace1 = go.Scatter(x = peepz,y = texting_costz,mode = 'lines',name = 'Texting Costs')
	trace2 = go.Scatter(x = peepz,y = returnz,mode = 'lines',name = 'Returns')


	data = [trace0,trace1,trace2]
	layout = go.Layout(margin={'t': 30,'l': 50},showlegend=True,xaxis={'title':'Total Number of Users'},yaxis={'title':'USD'})
	
	figure=go.Figure(data=data,layout=layout)
	div = opy.plot(figure, auto_open=False, output_type='div',show_link=False)

	#work around to remove modebar stuff
	div = div.replace('displaylogo:!0', 'displaylogo:!1')
	div = div.replace('modeBarButtonsToRemove:[]', 'modeBarButtonsToRemove:["sendDataToCloud","hoverCompareCartesian"]')



	sustainability_numbers = {
			"number_of_users": number_of_users,
			"number_of_free": int(number_of_free),
			"number_of_paid": int(number_of_paid),
			"con_conversation_rate_to_paid": str(int(100*working_busy.con_conversation_rate_to_paid)) +"%",
			"return_per_user": str(working_busy.con_return_per_paying_user_per_month)+"$",
		}		

	return div, sustainability_numbers



		








########### VISUALIZING FUNCTIONS
# var data = [
# 						  {
# 						    z: [[1, 20, 30], [20, 1, 60], [30, 60, 1], [2, -60, 11], [88, 44, -11]],
# 						    x: ['Morning', 'Afternoon', 'Evening'],
# 						    y: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
# 						    type: 'heatmap'
# 						  }
# 						];

############################## 
############# HEAT MAP
##############################

def get_hourly_count_of_prompts(request,time_anchor):
	entries = ActualTextSTM_SIM.objects.all().filter(user=request.user)
	


	# for set in feed_name:


	# print(entries.values('feed_name'))


	# print("HOURLY COUNT:",entries.count())
	working_settings = UserSetting.objects.all().get(user=request.user)
	# print("SLEEP TIME: ",working_settings.sleep_time.hour)
	# wake_time = working_settings.sleep_time + timedelta()
	hourout = []
	feed_name_type = []
	tmp_hours = list(range(0,24))

	tmp_mins = (0,15,30,45)
	promptout = []

	user_tz = pytz.timezone(working_settings.timezone)
	# print("user_tz: ", user_tz)
	for hr in tmp_hours:
		for mins in tmp_mins:

######## REFERENCE
			# local_tz = pytz.timezone(working_settings.timezone)
			# local_sleep_time = local_tz.localize(datetime.combine(time_anchor.date(),working_settings.sleep_time))
			# local_wake_time = local_sleep_time + timedelta(0,60*60*int(working_settings.sleep_duration))

			# utc_sleep_time = local_sleep_time.astimezone(pytz.UTC)
			# utc_wake_time = local_wake_time.astimezone(pytz.UTC)
######## REFERENCE			

			# check to see that is during wake or sleep
			sleep_datetime = datetime(time_anchor.year,time_anchor.month,time_anchor.day,working_settings.sleep_time.hour,working_settings.sleep_time.minute,working_settings.sleep_time.second)
			sleep_datetime = user_tz.localize(sleep_datetime)
			# sleep_datetime = sleep_datetime.astimezone(pytz.UTC)

			wake_datetime = datetime(time_anchor.year,time_anchor.month,time_anchor.day,working_settings.wake_time.hour,working_settings.wake_time.minute,working_settings.wake_time.second)
			wake_datetime = user_tz.localize(wake_datetime)

			dtnow = datetime(time_anchor.year,time_anchor.month,time_anchor.day,hr,mins, tzinfo=pytz.timezone(working_settings.timezone))
			# dtnow = user_tz.localize(dtnow)

			min_date = datetime(time_anchor.year,time_anchor.month,time_anchor.day,hr,mins, tzinfo=pytz.timezone(working_settings.timezone))
			max_date = datetime(time_anchor.year,time_anchor.month,time_anchor.day,hr,(mins+14),59, tzinfo=pytz.timezone(working_settings.timezone))
			entries_sm = entries.all().filter(time_to_send__gte=min_date).filter(time_to_send__lte=max_date)

			# print("SLEEP:    ", utc_sleep_time)
			# print("WAKE:     ",  utc_wake_time)
			# print("PROPOSED: ", proposed_next_prompt_time)

			if working_settings.sleep_time > datetime(2016,1,12,12,00).time() and working_settings.wake_time < datetime(2016,1,12,12,00).time():
				if sleep_datetime.time() <= dtnow.time() or dtnow.time() <= wake_datetime.time() :
					if entries_sm.count()<1:
						feed_name_type.append(.2)
						promptout.append(str('Sleep'))
					else:
						promptout.append(str(entries_sm.first().text))
						feed_name_type.append(str(entries_sm.first().feed_name))
							
				elif entries_sm.count()>0:
					promptout.append(str(entries_sm.first().text))
					feed_name_type.append(str(entries_sm.first().feed_name))
				else:
					promptout.append(str(''))
					feed_name_type.append(0)

	
	#This is to get the colors
	feed_names = ActualTextSTM_SIM.objects.all().filter(user=request.user).values('feed_name').distinct()
	feed_name_type_revised = []
	for tmp in feed_name_type:
		tset_counter = 1
		if (isinstance(tmp,str)):
			for w in feed_names:
				if w['feed_name'] == tmp:
					feed_name_type_revised.append(tset_counter)
				tset_counter = tset_counter + 1
		else:
			feed_name_type_revised.append(tmp)

		
	return feed_name_type_revised, promptout



	

def get_graph_data_simulated_heatmap(request):	
	prompts_by_date = []
	prompt_text_by_date = []
	dateout = []

	tmp_hours = (list(range(0,24)))
	tmp_mins = (0,15,30,45)
	time_counter = []
	for hr in tmp_hours:
		for mins in tmp_mins:
			time_counter.append(str(str(hr)+ ":" +str(mins)))

	tmp_date = datetime.now(pytz.utc)
	for tmp_counter in list(range(0,7)):
		number_of_prompts, promptout = get_hourly_count_of_prompts(request=request,time_anchor=tmp_date)
		# print("PROMPT: ", len(number_of_prompts))
		# print("PROMPT DAY: ", len(promptout))

		prompts_by_date.append(number_of_prompts)
		prompt_text_by_date.append(promptout)
		
		dateout.append(str(str(tmp_date.month) + '/' + str(tmp_date.day)))
		tmp_date = tmp_date+timedelta(days=1)


	z = prompts_by_date
	x = time_counter
	y = dateout

	y[0] = 'Today'

	colorscale = [[0, '#fff'], [ActualTextSTM_SIM.objects.all().filter(user=request.user).values('feed_name').distinct().count(), '#387db8']]

	trace1 = go.Heatmap(z=z, x=x, y=y, colorscale=colorscale, colorbar = {'tick0': 0,'dtick': 1 }, text = prompt_text_by_date, hoverinfo="text", showscale=False)
	data=go.Data([trace1])
	layout=go.Layout( xaxis={'title':'Hour', 'ticks': '','nticks':12,'fixedrange': True}, yaxis={'title':'Day', 'ticks': '','fixedrange': True,'autorange': 'reversed'}, margin={'t': 30} )
	figure=go.Figure(data=data,layout=layout)
	div = opy.plot(figure, auto_open=False, output_type='div',show_link=False)

	#work around to remove modebar stuff
	div = div.replace('displaylogo:!0', 'displaylogo:!1')
	div = div.replace('modeBarButtonsToRemove:[]', 'modeBarButtonsToRemove:["sendDataToCloud","hoverCompareCartesian"]')

	return div


### THIS GENERATES DATA FOR THE SUMMARY BAR CHART GRAPH
def get_graph_data_histogram(request,prompt_id,simulated_val):
	entries = ActualTextLTM.objects.all().filter(user=request.user).filter(text_id=prompt_id).filter(simulated=simulated_val)
	
	x = []
	for ent in entries:
		if ent.response != None:
			x.append(ent.response)
		

	print("HIST DATA", x)

	data = [
		go.Histogram(x=x,
			
			autobinx=False,
		    xbins=dict(
		        start= -.5,
		        end=10,
		        size=1
		    ),
		

		)
	]	

		
	
	layout = go.Layout(margin={'t': 30,'l': 30},showlegend=False, bargap=0.25,xaxis={ 'dtick':1})
	
	figure=go.Figure(data=data,layout=layout)
	div = opy.plot(figure, auto_open=False, output_type='div',show_link=False)

	#work around to remove modebar stuff
	div = div.replace('displaylogo:!0', 'displaylogo:!1')
	div = div.replace('modeBarButtonsToRemove:[]', 'modeBarButtonsToRemove:["sendDataToCloud","hoverCompareCartesian"]')
	return div


def get_graph_data_line_chart_plotly_smooth(request,simulated_val,prompt_id,number_of_days):
	#Figure out the date range
	ent = ActualTextLTM.objects.all().filter(user=request.user).filter(text_id=prompt_id).filter(simulated=simulated_val).order_by("time_sent").first()

	total_dates = ActualTextLTM.objects.all().filter(user=request.user).filter(text_id=prompt_id).filter(simulated=simulated_val).order_by("time_sent")
	total_datez = []
	for tmp in total_dates:
		total_datez.append(tmp.time_sent.date())
	total_datez = sorted(set(total_datez))
	
	

	#Go through by date and average the prompts
	promptz = []
	datez = []
	averagez = []
	for tmp_date in total_datez:
		top_date = tmp_date + timedelta(days=number_of_days, hours=0,minutes=0,seconds=0)
		bottom_date = tmp_date - timedelta(days=number_of_days, hours=0,minutes=0,seconds=0)

		tmp_promptz = ActualTextLTM.objects.all().filter(user=request.user).filter(simulated=simulated_val).filter(text_id=prompt_id).filter(time_sent__gte=bottom_date).filter(time_sent__lte=top_date).values('text').distinct()

		for tmp in tmp_promptz:
			datez.append(str(tmp_date))
			promptz.append(tmp['text'])

			if ent.response_type == '0 to 10':
				ha = ActualTextLTM.objects.all().filter(user=request.user).filter(simulated=simulated_val).filter(text_id=prompt_id).filter(text=tmp['text']).filter(time_sent__gte=bottom_date).filter(time_sent__lte=top_date).aggregate(Avg('response_dim'))
				averagez.append(ha['response_dim__avg'])
			else:
				ha = ActualTextLTM.objects.all().filter(user=request.user).filter(simulated=simulated_val).filter(text_id=prompt_id).filter(text=tmp['text']).filter(time_sent__gte=bottom_date).filter(time_sent__lte=top_date).aggregate(Avg('response_cat_bin'))
				averagez.append(ha['response_cat_bin__avg'])

	# print("X: ", datez)
	# print("Y: ", averagez)

	data = [go.Scatter(x=datez,y=averagez)]


	if ent.response_type == '0 to 10':
		layout = go.Layout(margin={'t': 30,'l': 30},showlegend=False,yaxis={'range': [0,10]})
	else:
		layout = go.Layout(margin={'t': 30,'l': 30},showlegend=False,yaxis={'range': [0,1]})

	
	
	figure=go.Figure(data=data,layout=layout)
	div = opy.plot(figure, auto_open=False, output_type='div',show_link=False)

	#work around to remove modebar stuff
	div = div.replace('displaylogo:!0', 'displaylogo:!1')
	div = div.replace('modeBarButtonsToRemove:[]', 'modeBarButtonsToRemove:["sendDataToCloud","hoverCompareCartesian"]')
	return div



def get_graph_data_line_chart_plotly(request,simulated_val,prompt_id):
	entries = ActualTextSTM.objects.all().filter(user=request.user).filter(simulated=simulated_val).filter(text_id=prompt_id)
	
	x = []
	y = []
	for ent in entries:
		x.append(ent.time_to_send)
		y.append(ent.response)
		
	
	data = [go.Scatter(x=x,y=y)]

	layout = go.Layout(margin={'t': 30,'l': 30},yaxis={'range': [0,10]},showlegend=False)
	
	figure=go.Figure(data=data,layout=layout)
	div = opy.plot(figure, auto_open=False, output_type='div',show_link=False)

	#work around to remove modebar stuff
	div = div.replace('displaylogo:!0', 'displaylogo:!1')
	div = div.replace('modeBarButtonsToRemove:[]', 'modeBarButtonsToRemove:["sendDataToCloud","hoverCompareCartesian"]')
	return div



def get_graph_data_by_prompt_bar(request,simulated_val):
	#DIME
	entries = ActualTextLTM.objects.all().filter(user=request.user).filter(simulated=simulated_val).filter(feed_type="user")
	averagez = []
	typez = []
	countz = []
	promptz = []

	tmp_prompts = entries.order_by().values('text').distinct()
	for tmp in tmp_prompts:
		promptz.append(tmp['text'])

		ha = ActualTextLTM.objects.all().filter(user=request.user).filter(simulated=simulated_val).filter(feed_type="user").filter(text = tmp['text']).aggregate(Avg('response_dim'))
		averagez.append(ha['response_dim__avg'])

		ha = ActualTextLTM.objects.all().filter(user=request.user).filter(simulated=simulated_val).filter(feed_type="user").filter(text = tmp['text']).aggregate(Count('response_dim'))
		countz.append(ha['response_dim__count'])

	

	trace1 = go.Bar(x=averagez,y=promptz,orientation='h')
	print("GRAPH Y:", promptz)
	data=go.Data([trace1])
	layout=go.Layout()
	figure=go.Figure(data=data,layout=layout)
	div = opy.plot(figure, auto_open=False, output_type='div',show_link=False)

	#work around to remove modebar stuff
	div = div.replace('displaylogo:!0', 'displaylogo:!1')
	div_dim = div.replace('modeBarButtonsToRemove:[]', 'modeBarButtonsToRemove:["sendDataToCloud","hoverCompareCartesian"]')

	####### CATEGORICAL
	entries = ActualTextLTM.objects.all().filter(user=request.user).filter(simulated=simulated_val).filter(feed_type="user")
	averagez = []
	typez = []
	countz = []
	promptz = []

	tmp_prompts = entries.order_by().values('text').distinct()
	for tmp in tmp_prompts:
		promptz.append(tmp['text'])

		ha = ActualTextLTM.objects.all().filter(user=request.user).filter(simulated=simulated_val).filter(feed_type="user").filter(text = tmp['text']).aggregate(Avg('response_cat_bin'))
		averagez.append(ha['response_cat_bin__avg'])

		ha = ActualTextLTM.objects.all().filter(user=request.user).filter(simulated=simulated_val).filter(feed_type="user").filter(text = tmp['text']).aggregate(Count('response_cat_bin'))
		countz.append(ha['response_cat_bin__count'])

	

	trace1 = go.Bar(x=averagez,y=promptz,orientation='h')
	print("GRAPH Y:", promptz)
	data=go.Data([trace1])
	layout=go.Layout()
	figure=go.Figure(data=data,layout=layout)
	div = opy.plot(figure, auto_open=False, output_type='div',show_link=False)

	#work around to remove modebar stuff
	div = div.replace('displaylogo:!0', 'displaylogo:!1')
	div_cat = div.replace('modeBarButtonsToRemove:[]', 'modeBarButtonsToRemove:["sendDataToCloud","hoverCompareCartesian"]')

	return div_dim, div_cat

def get_graph_data_by_prompt(request,simulated_val,response_type):
	entries = ActualTextLTM.objects.all().filter(user=request.user).filter(simulated=simulated_val).filter(feed_type="user")
	# entries = entries.order_by().annotate(Count('prompt_reply'))
	# print("HERE HERE HERE", entries.aggregate(Count('prompt')))
	
	if response_type == '0 to 10':
		ents = entries.exclude(response_dim__isnull=True).order_by().values('text').distinct()
	else:
		ents = entries.exclude(response_cat_bin__isnull=True).order_by().values('text').distinct()
	# ents = entries.order_by().annotate('prompt_reply')
	data=[]
	for i in range(int(ents.count())):

		tmp = []
		working_ents = ActualTextLTM.objects.all().filter(user=request.user).filter(simulated=simulated_val).filter(feed_type="user").filter(text=ents[i]['text'])

		for ent in working_ents:
			# print("POOP: ", ent.prompt_reply)
			if response_type == '0 to 10':
				tmp.append(ent.response_dim)
			else:
				tmp.append(ent.response_cat_bin)

		trace = go.Box(
			y=tmp,
			name = ents[i]['text'],
		)
		data.append(trace)
	
	if response_type == '0 to 10':
		layout = go.Layout(margin={'t': 30,'l': 30},yaxis={'range': [0,10]},xaxis={'autorange':True},showlegend=False)
	else:
		layout = go.Layout(margin={'t': 30,'l': 30},yaxis={'range': [0,1]},xaxis={'autorange':True},showlegend=False)
	
	
	figure=go.Figure(data=data,layout=layout)
	div = opy.plot(figure, auto_open=False, output_type='div',show_link=False)

	#work around to remove modebar stuff
	div = div.replace('displaylogo:!0', 'displaylogo:!1')
	div = div.replace('modeBarButtonsToRemove:[]', 'modeBarButtonsToRemove:["sendDataToCloud","hoverCompareCartesian"]')
	return div

def get_graph_data_time_of_day(request,simulated_val,prompt_id):
	#Probably do a check to see how many prompts there are.  
	entries = ActualTextLTM.objects.all().filter(user=request.user).filter(simulated=simulated_val).filter(text_id=prompt_id)

	ents = entries.order_by().values('time_to_send_circa').distinct()
	ent = ActualTextLTM.objects.all().filter(user=request.user).filter(text_id=prompt_id).filter(simulated=simulated_val).order_by("time_sent").first()

	# ents = entries.order_by().annotate('prompt_reply')
	if ent.response_type == '0 to 10':
		data=[]
		for i in range(int(ents.count())):

			tmp = []
			working_ents = ActualTextLTM.objects.all().filter(user=request.user).filter(simulated=simulated_val).filter(text_id=prompt_id).filter(time_to_send_circa=ents[i]['time_to_send_circa'])

			for ent in working_ents:
				# print("POOP: ", ent.prompt_reply)
				tmp.append(ent.response_dim)

			trace = go.Box(
				y=tmp,
				name = ents[i]['time_to_send_circa'],
			)
			data.append(trace)

		layout = go.Layout(margin={'t': 30,'l': 30},yaxis={'range': [0,10]},xaxis={'autorange':True},showlegend=False)

	else:
		data=[]
		for i in range(int(ents.count())):

			tmp = []
			working_ents = ActualTextLTM.objects.all().filter(user=request.user).filter(simulated=simulated_val).filter(text_id=prompt_id).filter(time_to_send_circa=ents[i]['time_to_send_circa'])

			for ent in working_ents:
				# print("POOP: ", ent.prompt_reply)
				tmp.append(ent.response_cat_bin)

			trace = go.Box(
				y=tmp,
				name = ents[i]['time_to_send_circa'],
			)
			data.append(trace)

		layout = go.Layout(margin={'t': 30,'l': 30},yaxis={'range': [0,1]},xaxis={'autorange':True},showlegend=False)

	

	figure=go.Figure(data=data,layout=layout)
	div = opy.plot(figure, auto_open=False, output_type='div',show_link=False)

	#work around to remove modebar stuff
	div = div.replace('displaylogo:!0', 'displaylogo:!1')
	div = div.replace('modeBarButtonsToRemove:[]', 'modeBarButtonsToRemove:["sendDataToCloud","hoverCompareCartesian"]')
	return div

def get_graph_data_day_in_week(request,simulated_val,prompt_id):
	#Probably do a check to see how many prompts there are.  
	entries = ActualTextLTM.objects.all().filter(user=request.user).filter(simulated=simulated_val).filter(text_id=prompt_id)

	dayzz = ("Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday")

	ent = ActualTextLTM.objects.all().filter(user=request.user).filter(text_id=prompt_id).filter(simulated=simulated_val).order_by("time_sent").first()

	if ent.response_type == '0 to 10':
		# ents = entries.order_by().annotate('prompt_reply')
		data=[]
		for i in range(0,len(dayzz)):
			tmp = []
			working_ents = ActualTextLTM.objects.all().filter(user=request.user).filter(text_id=prompt_id).filter(simulated=simulated_val).filter(time_to_send_day=dayzz[i])

			for ent in working_ents:
				tmp.append(ent.response_dim)

			trace = go.Box(
				y=tmp,
				name = dayzz[i],
			)
			data.append(trace)

		layout = go.Layout(margin={'t': 30,'l': 30},yaxis={'range': [0,10]},xaxis={'autorange':True},showlegend=False)
	else:
		# ents = entries.order_by().annotate('prompt_reply')
		data=[]
		for i in range(0,len(dayzz)):
			tmp = []
			working_ents = ActualTextLTM.objects.all().filter(user=request.user).filter(text_id=prompt_id).filter(simulated=simulated_val).filter(time_to_send_day=dayzz[i])

			for ent in working_ents:
				tmp.append(ent.response_cat_bin)

			trace = go.Box(
				y=tmp,
				name = dayzz[i],
			)
			data.append(trace)

		layout = go.Layout(margin={'t': 30,'l': 30},yaxis={'range': [0,1]},xaxis={'autorange':True},showlegend=False)


	figure=go.Figure(data=data,layout=layout)
	div = opy.plot(figure, auto_open=False, output_type='div',show_link=False)

	#work around to remove modebar stuff
	div = div.replace('displaylogo:!0', 'displaylogo:!1')
	div = div.replace('modeBarButtonsToRemove:[]', 'modeBarButtonsToRemove:["sendDataToCloud","hoverCompareCartesian"]')
	return div


def get_table_emotion_centered(request,simulated_val):
	averagez = []
	countz = []
	averagez_bin = []
	countz_bin = []
	totz_bin = []
	promptz = []
	prompt_idz = []
	feed_namez = []

	tmp_prompts = ActualTextLTM.objects.all().filter(user=request.user).filter(simulated=simulated_val).filter(feed_type="user").order_by().values('text').distinct()

	for tmp in tmp_prompts:
		example_tmp = ActualTextLTM.objects.all().filter(user=request.user).filter(simulated=simulated_val).filter(feed_type="user").filter(text=tmp['text']).first()

		promptz.append(tmp['text'])
		prompt_idz.append(example_tmp.text_id)
		ha = ActualTextLTM.objects.all().filter(user=request.user).filter(simulated=simulated_val).filter(text = tmp['text']).aggregate(Avg('response_dim'))
		averagez.append(ha['response_dim__avg'])

		ha = ActualTextLTM.objects.all().filter(user=request.user).filter(simulated=simulated_val).filter(text = tmp['text']).aggregate(Count('response_dim'))
		countz.append(ha['response_dim__count'])

		ha = ActualTextLTM.objects.all().filter(user=request.user).filter(simulated=simulated_val).filter(text = tmp['text']).aggregate(Avg('response_cat_bin'))
		averagez_bin.append(100*ha['response_cat_bin__avg'])

		ha = ActualTextLTM.objects.all().filter(user=request.user).filter(simulated=simulated_val).filter(text = tmp['text']).aggregate(Count('response_cat_bin'))
		countz_bin.append(ha['response_cat_bin__count'])

		ha = ActualTextLTM.objects.all().filter(user=request.user).filter(simulated=simulated_val).filter(text = tmp['text']).aggregate(Count('response'))
		totz_bin.append(ha['response__count'])

		feed_namez.append(example_tmp.feed_name)

	working_entry = []
	for i in range(0,len(promptz)):
		working_entry.append({'text': promptz[i],'response__count': totz_bin[i],'text_id': prompt_idz[i], 'feed_name': feed_namez[i], 'response_dim__avg': averagez[i], 'response_dim__count': countz[i], 'response_cat_bin__avg': averagez_bin[i], 'response_cat_bin__count': countz_bin[i]})
		# working_entry.append({'text': promptz[i],'text_id': prompt_idz[i]})

	print("WORKING ENTRY", working_entry)
	return working_entry		


def get_graph_data_line_chart(request,simulated_val):
	entries_by_date = ActualTextLTM.objects.all().filter(user=request.user).filter(simulated=simulated_val)
	entries_by_dates = json.dumps( [{'date': o.time_to_send, 'prompt': o.text, 'prompt_reply': o.response} for o in entries_by_date], cls=DjangoJSONEncoder)
	return entries_by_dates

def get_graph_data_line_chart_smoothed(request,simulated_val,number_of_days):
	#Figure out the date range
	total_dates = ActualTextLTM.objects.all().filter(user=request.user).filter(simulated=simulated_val).order_by("time_sent")
	total_datez = []
	for tmp in total_dates:
		total_datez.append(tmp.time_sent.date())
	total_datez = sorted(set(total_datez))
	
	

	#Go through by date and average the prompts
	promptz = []
	datez = []
	averagez = []
	for tmp_date in total_datez:
		top_date = tmp_date + timedelta(days=number_of_days, hours=0,minutes=0,seconds=0)
		bottom_date = tmp_date - timedelta(days=number_of_days, hours=0,minutes=0,seconds=0)

		tmp_promptz = ActualTextSTM.objects.all().filter(user=request.user).filter(simulated=simulated_val).filter(time_sent__gte=bottom_date).filter(time_sent__lte=top_date).values('text').distinct()

		for tmp in tmp_promptz:
			datez.append(str(tmp_date))
			promptz.append(tmp['text'])
			
			# ha = ActualTextSTM.objects.all().filter(user=request.user).filter(simulated=simulated_val).filter(text=tmp['text']).filter(time_sent__gte=bottom_date).filter(time_sent__lte=top_date).aggregate(Avg('response'))
			# averagez.append(ha['response__avg'])

	#format for json
	tmp_dumb = []
	for i in range(0,len(promptz)):
		# tmp_dumb.append({'datez': datez[i],'prompt': promptz[i], 'averagez': averagez[i]})
		tmp_dumb.append({'datez': datez[i],'prompt': promptz[i]})

	return json.dumps(tmp_dumb)





def get_user_summary_info(request,simulated_val):
	# summary_response_time = get_response_time(request)
	# summary_response_percent = get_response_rate(request)

	summary_response_time = 0
	summary_response_percent = 0

	#Number of responses
	number_of_replies = ActualTextLTM.objects.filter(user=request.user).exclude(response=None).count()
	number_of_texts = ActualTextLTM.objects.filter(user=request.user).count()


	working_settings = UserSetting.objects.get(user=request.user)
	timediff_since_begin = datetime.now(pytz.utc) - working_settings.begin_date


	user_sum = {'user': request.user,'summary_response_time': summary_response_time,'summary_response_percent': summary_response_percent,'number_of_replies': number_of_replies,'number_of_texts': number_of_texts,'timediff_since_begin': timediff_since_begin.days,}
	return user_sum


def get_graph_data_simulated(request,simulated_val,dayer=1):
	entries = ActualTextLTM.objects.all().filter(user=request.user).filter(simulated=simulated_val)
	tmp_prompts = entries.order_by().values('text').distinct()
	tmp_hours = list(range(0,24))

	dayzz = ("Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday")

	dy = dayzz[dayer]
	day_counter = dayer

	dayout = []
	hourout = []
	promptout = []
	countout = []
	dater = []

	#Get the first day of the simulated values
	
	local_tz = pytz.timezone('UTC')
	

	for hr in tmp_hours:
		min_date = datetime(2020,1,day_counter+1,hr,0)
		local_tzz = local_tz.localize(min_date)
		min_date = local_tzz.astimezone(pytz.UTC)


		max_date = datetime(2020,1,day_counter+1,hr,59,59)
		local_tzz = local_tz.localize(max_date)
		max_date = local_tzz.astimezone(pytz.UTC)


		entries_sm = entries.all().filter(time_to_send__gte=min_date).filter(time_to_send__lte=max_date)
		
		if entries_sm.count() < 1:
			dayout.append(dy)
			hourout.append(hr)
			promptout.append('')
			countout.append(0.000000000000000000000000000001)
			dater.append(str(dy)+str(' ')+str(hr)+str(':00'))

		else:
			for ent in entries_sm:
				dayout.append(dy)
				hourout.append(hr)
				promptout.append(ent.prompt)
				countout.append(1)
				dater.append(str(dy)+str(' ')+str(hr)+str(':00'))


	tmp_dumb = []
	for i in range(0,len(promptout)):
		tmp_dumb.append({'prompt': promptout[i], 'count': countout[i], 'dayout': dayout[i],'hourout': hourout[i],'dater': dater[i]})
	
	return json.dumps(tmp_dumb)
