from django.db.models import Avg, Count, F, Case, When
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.forms import modelformset_factory
import json
from django.core.serializers.json import DjangoJSONEncoder

from .forms import  BusinessForm, BusinessForm_price, BusinessForm_number_texts, BusinessForm_user_stuff, BusinessForm_static_costs, MeasureForm

from .models import Blog, Business, Measure, Sentimini_help
from ent.models import PossibleTextSTM, ActualTextSTM, ActualTextLTM, ActualTextSTM_SIM, FeedSetting, UserSetting
from vis.models import EntryDEV

from sentimini.sentimini_functions import get_user_summary_info, get_graph_data_histogram, get_graph_data_time_of_day, get_graph_data_day_in_week, get_graph_data_line_chart_plotly, get_graph_data_line_chart_plotly_smooth, get_graph_data_line_chart_business_model
from sentimini.scheduler_functions import figure_out_timing

# Create your views here.
def upload_feed_data(request):
	if request.user.is_authenticated():	
		library_experiences = FeedSetting.objects.all().filter(feed_type='library')

		for exp in library_experiences:
			exp.number_of_texts_in_set = PossibleTextSTM.objects.all().filter(feed_type='library').filter(feed_name=exp.feed_name).count()
			#figure out timing
			exp.text_interval_minute_avg, exp.text_interval_minute_min, exp.text_interval_minute_max = figure_out_timing(user=request.user,text_per_week=exp.texts_per_week)
			exp.save()

		print("UPLOAD")

		if request.GET.get('reset_texts_to_send'):
			# Get and delete unsent texts
			texts = ActualTextSTM.objects.filter(time_sent=None).filter(feed_type="user").filter(simulated=0)
			texts.delete()

			# You actually don't have to schedule them because they should be scheduled in the peridoci tasks
			

					
			return HttpResponseRedirect('/scaffold/upload_feed_data/')



		
		if request.GET.get('update_experience_settings'):
			working_experience = FeedSetting.objects.all().exclude(feed_type='user')

			for exp in working_experience:
				exp.number_of_texts_in_set = PossibleTextSTM.objects.all().filter(feed_type='library').filter(unique_feed_name=exp.unique_feed_name).count()
				print("COUNT:", exp.number_of_texts_in_set )
				#figure out timing
				exp.text_interval_minute_avg, exp.text_interval_minute_min, exp.text_interval_minute_max = figure_out_timing(user=request.user,text_per_week=exp.texts_per_week)
	
				if exp.feed_id == 0:
					exp.feed_id = exp.id

				exp.save()
					
			return HttpResponseRedirect('/scaffold/upload_feed_data/')


		if request.GET.get('update_new_possible_texts'):
			working_texts = PossibleTextSTM.objects.all().exclude(feed_type='user')

			print("TEXT COUNT", working_texts.count() )

			for text in working_texts:
				if text.feed_id == 0:
					print("TEXT ID ZERO")
					print(text.unique_feed_name)

					tmp_exp = FeedSetting.objects.all().exclude(feed_type='user').get(unique_feed_name=text.unique_feed_name)
					text.feed_id = tmp_exp.feed_id
					text.save()

			return HttpResponseRedirect('/scaffold/upload_feed_data/')	

		context = {
			"library_experiences": library_experiences,
			
		}			

		return render(request,"upload_feed_data.html",context)
	else:
		print("UPLOAD NOT AUTH")
		return render(request,"upload_feed_data.html")


def sentimini_help(request):
	if request.user.is_authenticated():	
		working_help = Sentimini_help.objects.all().filter(help_type="Glossary")
		working_faq = Sentimini_help.objects.all().filter(help_type="FAQ")

		context = {
			"working_help": working_help,
			"working_faq": working_faq,
		}			

		return render(request,"sentimini_help.html",context)
	else:
		working_help = Sentimini_help.objects.all().filter(help_type="Glossary")
		working_faq = Sentimini_help.objects.all().filter(help_type="FAQ")

		context = {
			"working_help": working_help,
			"working_faq": working_faq,
		}	
		return render(request,"sentimini_help.html",context)



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
		



def open_data(request):
	if request.user.is_authenticated():	
	
		
		context = {
			
		}			

		return render(request,"open_data.html",context)
	else:
		return render(request,"open_data.html")



def about(request):
	if request.user.is_authenticated():	
		#FAQ STUFF
		#don't forget to add form for user generated question
		number_of_users = UserSetting.objects.all().count()


		
		context = {
		"number_of_users": number_of_users,
			
		}			

		return render(request,"about.html",context)
	else:
		return render(request,"about.html")




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
		blogs = Blog.objects.all()
		featured_blog = Blog.objects.all().get(id=1)
		
		context = {
			"featured_blog": featured_blog,
			"blogs": blogs,
		}	
		return render(request,"blog.html",context)

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
		blogs = Blog.objects.all()
		featured_blog = Blog.objects.all().get(id=id)
		
		context = {
			"featured_blog": featured_blog,
			"blogs": blogs,
		}	
		return render(request,"blog.html",context)



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



	
	



	# print("prompt_id :", prompt_id)
	# print("TEST COUNT:",  ActualTextLTM.objects.all().filter(user=user).filter(simulated=magic_simulated_value).filter(text_id=prompt_id).count())


