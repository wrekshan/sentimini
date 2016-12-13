from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from ent.models import UserSetting

from .forms import SignupFormWithoutAutofocus


# from sentimini.sentimini_functions import get_response_time, get_response_rate
from ent.models import ActualTextSTM, FeedSetting, PossibleTextSTM, UserSetting, GroupSetting
from ent.views import update_experiences
from ent.forms import AddNewGroup_Creator_Form, KT_PossibleTextSTMForm, GroupPasscode_Form


def create_new_user_experience_group(user,feed_id,group_id,default_experience):
	if FeedSetting.objects.filter(user=user).filter(feed_type='user').filter(group_id=group_id).filter(feed_id=feed_id).count()<1:
		print("default_experience",default_experience)
		print("feed_id",feed_id)
		library_tmp = FeedSetting.objects.all().filter(feed_type=default_experience).get(feed_id=feed_id)
		group_tmp = GroupSetting.objects.all().filter(group_type=default_experience).get(id =group_id)
		FeedSetting(user=user,feed_type='user',feed_id=feed_id,group_name=group_tmp.group_name,group_id=group_id,description=library_tmp.description,feed_name=library_tmp.feed_name,user_state="disable").save()
		working_experience = FeedSetting.objects.all().filter(user=user).filter(group_id=group_id).filter(feed_type="user").get(feed_id=feed_id)

		#INITIALIZE TEXTS
		if PossibleTextSTM.objects.all().filter(group_id=group_id).filter(feed_id=feed_id).count() > 0 :
			tmp_texts = PossibleTextSTM.objects.all().filter(group_id=group_id).filter(feed_id=feed_id,feed_name=working_experience.feed_name)

			for text in tmp_texts:
				tmp_new = PossibleTextSTM(user=user,text=text.text,group_name=text.group_name,group_id=text.group_id,response_type=text.response_type,feed_id=text.feed_id,feed_name=text.feed_name,feed_type="user",text_importance=text.text_importance,date_created=text.date_created)
				tmp_new.save()




def karuna_training(request,id=1):
	if request.user.is_authenticated():	
		if GroupSetting.objects.all().filter(user=request.user).filter(unique_group_name="NC_KT_1").filter(group_type="user").count()<1:

			working_group = GroupSetting.objects.all().get(id=id)
			working_feed = FeedSetting.objects.all().filter(feed_type="library").filter(group_id=id).get(unique_feed_name="basic_KT_feed")
			form_group_passcode = GroupPasscode_Form(request.POST or None)
			text_for_user = "Please enter the passcode.  If you do not know, please email me at william@sentimini.com"

			if 'submit_group_passcode' in request.POST:
				print("PASSCODE SUB")
				if form_group_passcode.is_valid():	
					tmp = form_group_passcode.save()
					working_user_group = GroupSetting(user=request.user,ideal_id=working_group.ideal_id,group_name=working_group.group_name,unique_group_name=working_group.unique_group_name,group_type="user",description=working_group.description)
					working_user_group.passcode = tmp.passcode
					working_user_group.save()
					create_new_user_experience_group(user=request.user,feed_id=working_feed.feed_id,group_id=working_group.group_id,default_experience='library')
					HttpResponseRedirect('/karuna_training')

			context = {
			"form_group_passcode": form_group_passcode,
			"working_group": working_group,
			"text_for_user": text_for_user,
			}
			return render(request, "groups_enter_passcode.html", context)
		else:
			working_group = GroupSetting.objects.all().get(id=id)
			working_user_group = GroupSetting.objects.all().filter(unique_group_name="NC_KT_1").filter(group_type="user").get(user=request.user)
		
			if not working_group.passcode == working_user_group.passcode:
				form_group_passcode = GroupPasscode_Form(request.POST or None, instance = working_user_group)
				text_for_user = "Please enter the passcode.  If you do not know, please email me at william@sentimini.com"

				if 'submit_group_passcode' in request.POST:
					if form_group_passcode.is_valid():	
						tmp = form_group_passcode.save()
						tmp.save()
						
				
						HttpResponseRedirect('/karuna_training')

				context = {
				"form_group_passcode": form_group_passcode,
				"working_group": working_group,
				"text_for_user": text_for_user,
				}
				return render(request, "groups_enter_passcode.html", context)
			else:
				working_group = GroupSetting.objects.all().get(id=id)
				working_feed = FeedSetting.objects.all().filter(feed_type="library").filter(group_id=id).get(unique_feed_name="basic_KT_feed")

				if FeedSetting.objects.all().filter(user=request.user).filter(feed_type="user").filter(group_id=id).filter(feed_name="basic_KT_feed").count() < 1:
					create_new_user_experience_group(user=request.user,feed_id=working_feed.feed_id,group_id=working_group.id,default_experience='library')

				if FeedSetting.objects.all().filter(user=request.user).count()>0:
					update_experiences(user=request.user)

					basic_feed = FeedSetting.objects.all().filter(feed_name="Default Basic Feed").get(id = 62)
					working_group = GroupSetting.objects.all().get(id=id)
					working_user_feeds = FeedSetting.objects.all().filter(user=request.user).filter(feed_type="user").filter(group_id = id)
					working_library_feeds_tmp = FeedSetting.objects.all().filter(feed_type="user").filter(group_id = id)
					working_library_feeds = working_library_feeds_tmp | working_user_feeds

					for exp in working_library_feeds:
						if working_library_feeds.filter(feed_id=exp.feed_id).count() > 1:
							tmp_remove = working_library_feeds.filter(feed_type="library").get(feed_id=exp.feed_id)
							working_library_feeds = working_library_feeds.exclude(id=tmp_remove.id)


					working_user_texts = PossibleTextSTM.objects.all().filter(group_id=id).filter(unique_feed_name="basic_KT_feed")
					form_group_settings = AddNewGroup_Creator_Form(request.POST or None, instance = working_group)

					form_new_text = KT_PossibleTextSTMForm(request.POST or None)

					if request.GET.get('create_new_feed'):
						print("CREATING NEW FEED PRESSED")
						FeedSetting(user=request.user,feed_type='user',feed_name="New Set",group_name=working_group.group_name,group_id=working_group.id,user_state="disable").save()

						working_experience = FeedSetting.objects.all().filter(user=request.user).filter(group_id=working_group.id).filter(feed_type="user").get(feed_name="New Set")
						working_experience.feed_id = working_experience.id
						working_experience.save()

						return HttpResponseRedirect('/ent/text_set_detail/'+str(working_experience.id))


					if request.method == "POST":
						if 'submit_new_group' in request.POST:
							if form_group_settings.is_valid():	
								tmp = form_group_settings.save()
								tmp.save()
							
							HttpResponseRedirect('/ent/group_detail/'+str(id))	

						if 'submit_new_text' in request.POST:
							if form_new_text.is_valid():	
								tmp = form_new_text.save()

								tmp.user=request.user
								tmp.group_id=working_group.id
								tmp.group_name=str(working_group.group_name)
								tmp.feed_id = basic_feed.id
								tmp.unique_feed_name = basic_feed.unique_feed_name
								tmp.feed_name = basic_feed.feed_name
								tmp.feed_type = basic_feed.feed_type
								tmp.save()
							
							HttpResponseRedirect('/karuna_training')

						# elif 'submit_prompt_percent' in request.POST:
						# 	if form_exp_timing.is_valid():
						# 		form_exp_timing.save()
						# 		HttpResponseRedirect('/ent/kt_group')


				
					context = {
						"form_group_settings": form_group_settings,
						"working_group": working_group,
						"form_new_text": form_new_text,
						"working_user_texts": working_user_texts,
						"working_user_feeds": working_user_feeds,
						"working_library_feeds": working_library_feeds,
					}

					return render(request, "karuna_training.html", context)
	else:
		return HttpResponseRedirect('/accounts/signup/')


def landing_page(request):
	if request.user.is_authenticated():	
		return HttpResponseRedirect(reverse('scaffold:about'))
	else:
		library_experiences = FeedSetting.objects.all().filter(feed_type='library').filter(group_id=0)
		number_of_users = UserSetting.objects.all().count()
		

		context = {
		"library_experiences": library_experiences,
		"number_of_users": number_of_users,

		}
		return render(request,"landing.html",context)


def feed_view(request,id=None):
	ideal_experience = FeedSetting.objects.all().get(id=id)
	working_user_gen = PossibleTextSTM.objects.all().filter(show_user=False).filter(feed_type="library").filter(feed_id=id)
	number_of_texts = working_user_gen.count()
	text_per_week = ideal_experience.texts_per_week

	context = {
	"working_user_gen": working_user_gen,
	"ideal_experience": ideal_experience,
	"number_of_texts": number_of_texts,
	"text_per_week": text_per_week,
	}
	return render(request,"feed_view.html",context)


from allauth.account.views import SignupView

class SignupViewWithCustomForm(SignupView):
    form_class = SignupFormWithoutAutofocus

signup_view = SignupViewWithCustomForm.as_view()
