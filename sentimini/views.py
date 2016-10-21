from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from ent.models import UserSetting

from .forms import SignupFormWithoutAutofocus


# from sentimini.sentimini_functions import get_response_time, get_response_rate
from ent.models import ActualTextSTM, ExperienceSetting, PossibleTextSTM
from ent.forms import PreUser_PossibleTextSTMForm



def landing_page(request):
	if request.user.is_authenticated():	
		return HttpResponseRedirect(reverse('scaffold:about'))
	else:
		library_experiences = ExperienceSetting.objects.all().filter(experience='library')
		

		context = {
		"library_experiences": library_experiences,

		}
		return render(request,"landing.html",context)


def feed_view(request,id=None):
	ideal_experience = ExperienceSetting.objects.all().get(id=id)
	working_user_gen = PossibleTextSTM.objects.all().filter(show_user=False).filter(text_type="library").filter(experience_id=id)
	number_of_texts = working_user_gen.count()
	text_per_week = ideal_experience.prompts_per_week

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
