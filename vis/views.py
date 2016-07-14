from django.db.models import Avg, Count, F, Case, When
from django.shortcuts import render, render_to_response


# Create your views here.
from ent.models import Emotion, Entry

def get_response_time(request):
	current_user = request.user
	#Get the response time stuff
	summary_response_time = Entry.objects.filter(user=current_user).filter(prompt_type="CORE").aggregate(response_time=Avg('response_time_seconds'))
	# tmp_num_entires = Entry.objects.filter(user=current_user).count()
	summary_response_time = summary_response_time['response_time']
	return(summary_response_time)

		
def get_response_rate(request):
	current_user = request.user
	tmp_total_num_entires = Entry.objects.filter(user=current_user).filter(prompt_type="CORE").count()
	tmp_responded_num_entires = Entry.objects.filter(user=current_user).filter(prompt_type="CORE").filter(response_time_seconds__gt=0).exclude(prompt_reply__isnull=True).count()
	if tmp_responded_num_entires > 0:
		summary_response_percent = (tmp_responded_num_entires / tmp_total_num_entires)*100
	else:
		summary_response_percent = 0
	return(summary_response_percent)

def user_vis(request):
	if request.user.is_authenticated():	
		print("USER")
		if Entry.objects.filter(user=request.user).count() > 1:
			print("has more 1 entry")

			current_user = request.user
			
			#Get the response time stuff
			summary_response_time = get_response_time(request)
			summary_response_percent = get_response_rate(request)

	# 		#Calculate the average values and counts for each emotion
			working_entry = Entry.objects.filter(user=current_user).filter(prompt_type="CORE").values('prompt').annotate(Avg('prompt_reply')).annotate(Count('prompt'))
			working_entry = working_entry.exclude(prompt_type__icontains="NUP")
			working_entry = working_entry.exclude(prompt_type__icontains="User Generated")

			latest_entry = Entry.objects.filter(user=current_user)
			latest_entry = latest_entry.exclude(prompt_type__icontains="NUP")
			latest_entry = latest_entry.exclude(prompt_type__icontains="User Generated")
			latest_entry = latest_entry.order_by('time_sent')[:5]
			
			
			#Reshape it to get something useable.  i don't like this but it might work
			# name=[]
			# value=[]
			# for we in working_entry:
			# 	# print(we['emotion'])
			# 	name.append(we['prompt'])
			# 	value.append(we['prompt_reply__avg'])
			
			print(working_entry)
			context = {
				'user': request.user,
			    'working_entry': working_entry,
			    'latest_entry': latest_entry,

			    'summary_response_time': summary_response_time,
			    'summary_response_percent': summary_response_percent,
			}
			
			return render_to_response('user_vis.html', context)
		else:
			print("has more no entry")
			context = {
				'user': request.user,
				"num_entries": Entry.objects.filter(user=request.user).count(),
			}

		
			return render_to_response('user_vis_no_entries.html',context)

	else:
		return render(request, "index_not_logged_in.html")

