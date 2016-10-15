from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from ent.models import UserSetting

from .forms import SignupFormWithoutAutofocus


# from sentimini.sentimini_functions import get_response_time, get_response_rate
from ent.models import ActualTextSTM
from ent.forms import PreUser_PossibleTextSTMForm



def landing_page(request):
	if request.user.is_authenticated():	
		return HttpResponseRedirect(reverse('scaffold:about'))
	else:
		return HttpResponseRedirect(reverse('scaffold:about'))


from allauth.account.views import SignupView

class SignupViewWithCustomForm(SignupView):
    form_class = SignupFormWithoutAutofocus

signup_view = SignupViewWithCustomForm.as_view()
