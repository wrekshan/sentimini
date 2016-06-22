from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .forms import  FAQuserquestionsForm
from .models import FAQ, FAQuserquestions
# Create your views here.
def faq(request):
	if request.user.is_authenticated():	
		#don't forget to add form for user generated question
		faq_usage = FAQ.objects.all().filter(category="Usage")
		faq_concept = FAQ.objects.all().filter(category="Concept")

		if request.method == "POST":
			form = form = FAQuserquestionsForm(request.POST)
			if form.is_valid():
				messages.add_message(request, messages.INFO, 'Question added!')	
				working_faq = form.save(commit=False)
				FAQuserquestions(user=request.user,question=working_faq.question).save()
				return HttpResponseRedirect(reverse('scaffold:faq'))
		else:
			form = FAQuserquestionsForm()

		
		context = {
			"faq_usage": faq_usage,
			"faq_concept": faq_concept,
			"form": form,
		}			

		return render(request,"faq.html",context)
	else:
		return HttpResponseRedirect('/accounts/signup/')
