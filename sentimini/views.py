from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from ent.models import UserSetting

from .forms import SignupFormWithoutAutofocus


# from sentimini.sentimini_functions import get_response_time, get_response_rate
from ent.models import ActualTextSTM



def landing_page(request):
	if request.user.is_authenticated():	
		#test is has working settings
				

		return render(request,"about.html")
	else:
		return render(request,"about.html")		


from allauth.account.views import SignupView

class SignupViewWithCustomForm(SignupView):
    form_class = SignupFormWithoutAutofocus

signup_view = SignupViewWithCustomForm.as_view()
