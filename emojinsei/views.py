from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from ent.models import UserSetting

from .forms import SignupFormWithoutAutofocus

from scaffold.forms import  FAQuserquestionsForm
from scaffold.models import FAQuserquestions

from vis.views import get_response_time, get_response_rate
from ent.models import Entry

def landing_page(request):
	if request.user.is_authenticated():	
		#test is has working settings
		if UserSetting.objects.all().filter(user=request.user).count() < 1:
			working_settings = UserSetting(user=request.user)
			working_settings.save()
		
		if Entry.objects.filter(user=request.user).count() > 1:
			summary_response_time = get_response_time(request)
			summary_response_percent = get_response_rate(request)

		if request.method == "POST":

			form = FAQuserquestionsForm(request.POST)

			if form.is_valid():
				messages.add_message(request, messages.INFO, 'Question added!')	
				working_faq = form.save(commit=False)
				FAQuserquestions(user=request.user,typer='suggestion',question=working_faq.question).save()
				return HttpResponseRedirect('/')
		else:
			form = FAQuserquestionsForm()
			print(form)

		
		context = {
			"form": form,
			'summary_response_time': summary_response_time,
		    'summary_response_percent': summary_response_percent,
		}			

		return render(request,"dashboard.html",context)
	else:
		return HttpResponseRedirect('/accounts/signup/')		


from allauth.account.views import SignupView

class SignupViewWithCustomForm(SignupView):
    form_class = SignupFormWithoutAutofocus

signup_view = SignupViewWithCustomForm.as_view()
