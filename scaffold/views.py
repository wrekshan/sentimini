from django.db.models import Avg, Count, F, Case, When
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.forms import modelformset_factory
import json
from django.core.serializers.json import DjangoJSONEncoder

from .forms import  FAQuserquestionsForm, emotion_quotationForm_sm, emotion_instructionForm_sm, BETAsurveyForm, BusinessForm, BusinessForm_price, BusinessForm_number_texts, BusinessForm_user_stuff, BusinessForm_static_costs, MeasureForm, Sentimini_helpForm, Sentimini_helpFormSetHelper

from .models import FAQ, FAQuserquestions, emotion_quotation, emotion_instruction, emotion_statement_display, BETAsurvey, user_likes, Blog, Business, Measure, Sentimini_help
from ent.models import PossibleTextSTM, ActualTextSTM, ActualTextLTM
from vis.models import EntryDEV

from sentimini.sentimini_functions import get_user_summary_info, get_graph_data_histogram, get_graph_data_time_of_day, get_graph_data_day_in_week, get_graph_data_line_chart_plotly, get_graph_data_line_chart_plotly_smooth, get_graph_data_line_chart_business_model


# Create your views here.
def sentimini_help(request):
	if request.user.is_authenticated():	
		working_help = Sentimini_help.objects.all().filter(help_type="Glossary")

		context = {
			"working_help": working_help,
		}			

		return render(request,"sentimini_help.html",context)
	else:
		return HttpResponseRedirect('/accounts/signup/')



def power(request):
	if request.user.is_authenticated():	
		if Measure.objects.all().count()<1:
			working_measure = Measure(user=request.user).save()
		else:
			working_measure = Measure.objects.all().first()

		measure_form = MeasureForm(request.POST or None, instance=working_measure)

		if request.method == "POST":
			if 'submit_measure' in request.POST:
				working_measure = measure_form.save()
				return HttpResponseRedirect(reverse('scaffold:power'))
		else:
			measure_form = MeasureForm(request.POST or None, instance=working_measure)
		
		context = {
			"measure_form": measure_form,
			
		}			

		return render(request,"power.html",context)
	else:
		return HttpResponseRedirect('/accounts/signup/')




def business_model(request):
	if request.user.is_authenticated():	
		if Business.objects.all().count()<1:
			working_busy = Business(user=request.user).save()
		
		working_busy = Business.objects.all().first()



		price_form = BusinessForm_price(request.POST or None, instance=working_busy)
		number_texts_form = BusinessForm_number_texts(request.POST or None, instance=working_busy)
		user_stuff_form = BusinessForm_user_stuff(request.POST or None, instance=working_busy)
		static_costs_form = BusinessForm_static_costs(request.POST or None, instance=working_busy)

		graph_data_line_chart_business_model, sustainability_numbers = get_graph_data_line_chart_business_model(working_busy=working_busy)


		if request.method == "POST":
			if 'submit_price_business' in request.POST:
				if price_form.is_valid():
					working_busy = price_form.save()
					return HttpResponseRedirect(reverse('scaffold:business_model'))

			if 'submit_number_texts_business' in request.POST:
				if number_texts_form.is_valid():
					working_busy = number_texts_form.save()
					return HttpResponseRedirect(reverse('scaffold:business_model'))

			if 'submit_user_stuff_business' in request.POST:
				if user_stuff_form.is_valid():
					working_busy = user_stuff_form.save()
					return HttpResponseRedirect(reverse('scaffold:business_model'))

			if 'submit_static_costs_business' in request.POST:
				if static_costs_form.is_valid():
					working_busy = static_costs_form.save()
					return HttpResponseRedirect(reverse('scaffold:business_model'))
			
		else:
			price_form = BusinessForm_price(request.POST or None, instance=working_busy)
			number_texts_form = BusinessForm_number_texts(request.POST or None, instance=working_busy)
			user_stuff_form = BusinessForm_user_stuff(request.POST or None, instance=working_busy)
			static_costs_form = BusinessForm_static_costs(request.POST or None, instance=working_busy)
			

		context = {
			"sustainability_numbers": sustainability_numbers,

			"price_form": price_form,
			"number_texts_form": number_texts_form,
			"user_stuff_form": user_stuff_form,
			"static_costs_form": static_costs_form,

			"working_busy": working_busy,
			"graph_data_line_chart_business_model": graph_data_line_chart_business_model,
			
		}			

		return render(request,"business_model.html",context)
	else:
		return HttpResponseRedirect('/accounts/signup/')		



def open_data(request):
	if request.user.is_authenticated():	
	
		
		context = {
			
		}			

		return render(request,"open_data.html",context)
	else:
		return HttpResponseRedirect('/accounts/signup/')



def about(request):
	if request.user.is_authenticated():	
		#FAQ STUFF
		#don't forget to add form for user generated question
		faq_usage = FAQ.objects.all().filter(category="Usage")
		faq_concept = FAQ.objects.all().filter(category="Concept")

		if request.method == "POST":
			form = FAQuserquestionsForm(request.POST)
			BETAform = BETAsurveyForm(request.POST)
			if 'submit_FAQ' in request.POST:
				if form.is_valid():
					messages.add_message(request, messages.INFO, 'Question added!')	
					working_faq = form.save(commit=False)
					FAQuserquestions(user=request.user,question=working_faq.question).save()
					return HttpResponseRedirect(reverse('scaffold:about'))
			elif 'submit_BETA' in request.POST:
				if BETAform.is_valid():
					messages.add_message(request, messages.INFO, 'BETA added!')	
					working_faq = BETAform.save()
					# BETAsurvey(user=request.user,question=working_faq.question).save()
					return HttpResponseRedirect(reverse('scaffold:about'))
		else:
			form = FAQuserquestionsForm()
			BETAform = BETAsurveyForm()

		context = {
			"faq_usage": faq_usage,
			"faq_concept": faq_concept,
			"form": form,
			"BETAform": BETAform,
		}			

		return render(request,"about.html",context)
	else:
		return HttpResponseRedirect('/accounts/signup/')




def blog(request):
	if request.user.is_authenticated():	
		blogs = Blog.objects.all()
		featured_blog = Blog.objects.all().get(id=1)
		
		context = {
			"featured_blog": featured_blog,
			"blogs": blogs,
		}			

		return render(request,"blog.html",context)
	else:
		return HttpResponseRedirect('/accounts/signup/')

def blog_detail(request,id=None):
	if request.user.is_authenticated():	
		blogs = Blog.objects.all()
		featured_blog = Blog.objects.all().get(id=id)
		
		context = {
			"featured_blog": featured_blog,
			"blogs": blogs,
		}			

		return render(request,"blog.html",context)
	else:
		return HttpResponseRedirect('/accounts/signup/')



def emotion(request):
	if request.user.is_authenticated():	
		#Produce a list of each emotion type
		working_emotions = Emotion.objects.all()
		emo_summary_list=[]

		core_list = []
		expanded_list = []
		open_list = []
		interest_list=[]
		user_list=[]

		for emo in working_emotions:
			if emo.prompt_set == 'CORE':
				core_list.append({'prompt_id':emo.id,'prompt':emo.emotion,'type':emo.prompt_set,'user_count': Entry.objects.filter(user=request.user).filter(simulated=1).filter(prompt_id=emo.id).count()})
			elif emo.prompt_set== 'expanded':
				expanded_list.append({'prompt_id':emo.id,'prompt':emo.emotion,'type':emo.prompt_set,'user_count': Entry.objects.filter(user=request.user).filter(simulated=1).filter(prompt_id=emo.id).count()})
			elif emo.prompt_set== 'open':
				open_list.append({'prompt_id':emo.id,'prompt':emo.emotion,'type':emo.prompt_set,'user_count': Entry.objects.filter(user=request.user).filter(simulated=1).filter(prompt_id=emo.id).count()})
			elif emo.prompt_set== 'interest':
				interest_list.append({'prompt_id':emo.id,'prompt':emo.emotion,'type':emo.prompt_set,'user_count': Entry.objects.filter(user=request.user).filter(simulated=1).filter(prompt_id=emo.id).count()})


		if Entry.objects.filter(user=request.user).filter(simulated=1).count() > 1:
			latest_entry = Entry.objects.filter(user=request.user).filter(simulated=1)
			latest_entry = latest_entry.exclude(prompt_type__icontains="user")
			latest_entry = latest_entry.order_by('time_sent')


			context = {
			    'core_list': core_list,
			    'expanded_list': expanded_list,
			    'open_list': open_list,
			    'interest_list': interest_list,
		    }
	    
		
		return render(request,"emotion.html", context)
	else:
		return HttpResponseRedirect('/accounts/signup/')



def get_text_summary(user,prompt_id):
	magic_simulated_value = 1

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

	
	



	# print("prompt_id :", prompt_id)
	# print("TEST COUNT:",  ActualTextLTM.objects.all().filter(user=user).filter(simulated=magic_simulated_value).filter(text_id=prompt_id).count())


def emotion_detail(request,prompt_id=None):
	if request.user.is_authenticated():	
		magic_simulated_value = 1
		if ActualTextLTM.objects.filter(user=request.user).count() > 1:

			### Here are all the stuff that won't be user specific, but emotion specific
			user_summary_info = get_user_summary_info(request, simulated_val=magic_simulated_value)
			emotion_name = PossibleTextSTM.objects.all().get(id=prompt_id)

			


			### Here are all the stuff that WILL be user specific, but emotion specific
			graph_data_histogram = get_graph_data_histogram(request=request,simulated_val=magic_simulated_value,prompt_id=prompt_id)

			## AM / PM
			graph_data_time_of_day = get_graph_data_time_of_day(request=request,simulated_val=magic_simulated_value,prompt_id=prompt_id)

			## WEEKDAY
			graph_data_day_in_week = get_graph_data_day_in_week(request=request,simulated_val=magic_simulated_value,prompt_id=prompt_id)

			## TIME LINE
			graph_data_line_chart_plotly = get_graph_data_line_chart_plotly_smooth(request=request,simulated_val=magic_simulated_value,prompt_id=prompt_id,number_of_days=1)

			get_text_summary(user=request.user,prompt_id=prompt_id)


			#Table
			table_latest_entry = ActualTextLTM.objects.all().filter(user=request.user).filter(text_type="user")
			table_latest_entry = table_latest_entry.order_by('time_sent')




			context = {
			'emotion_name': emotion_name,
			'user_summary_info': user_summary_info,


			"graph_data_histogram": graph_data_histogram,
			"graph_data_time_of_day": graph_data_time_of_day,
			"graph_data_day_in_week": graph_data_day_in_week,
			"graph_data_line_chart_plotly": graph_data_line_chart_plotly,

			"table_latest_entry": table_latest_entry,

			 #    'latest_entry': latest_entry,
			 #    'entries_by_date': entries_by_date,
			 #    'entries_circa': entries_circa,
			 #    'entries_day': entries_day,
			 #    'histogramz': histogramz,
			 #    'number_of_entries': number_of_entries,
			 #    'number_of_responses': number_of_responses,
			 #    'response_rate': response_rate,
			 #    'emotion_percent': emotion_percent,
			 #    "core_list": core_list,
				# "top_list": top_list,
				# "other_list": other_list,
				# "emo_instruct": emo_instruct,
				# "emo_quot": emo_quot,
				
		    }

		else:
			context = {
			
		    }
	    
		
		return render(request,"emotion_detail.html", context)
	else:
		return HttpResponseRedirect('/accounts/signup/')
