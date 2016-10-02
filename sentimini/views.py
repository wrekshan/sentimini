from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from ent.models import UserSetting

from .forms import SignupFormWithoutAutofocus

from scaffold.forms import  FAQuserquestionsForm, emotion_quotationForm, emotion_instructionForm
from scaffold.models import FAQuserquestions, emotion_quotation, emotion_instruction

# from sentimini.sentimini_functions import get_response_time, get_response_rate
from ent.models import ActualTextSTM



def landing_page(request):
	if request.user.is_authenticated():	
		#test is has working settings
		if UserSetting.objects.all().filter(user=request.user).count() < 1:
			working_settings = UserSetting(user=request.user)
			working_settings.save()
		
		if Entry.objects.filter(user=request.user).count() > 1:
			# summary_response_time = get_response_time(request)
			# summary_response_percent = get_response_rate(request)

			summary_response_time = 0
			summary_response_percent = 0

		if request.method == "POST":


			form = FAQuserquestionsForm(request.POST)
			form_emo_quotations = emotion_quotationForm(request.POST)
			form_emo_instructions = emotion_instructionForm(request.POST)

			if 'form_faq' in request.POST:
				if form.is_valid():
					messages.add_message(request, messages.INFO, 'Question added!')	
					working_faq = form.save(commit=False)
					FAQuserquestions(user=request.user,typer='suggestion',question=working_faq.question).save()
					return HttpResponseRedirect('/')

			if 'form_emo_quotations' in request.POST:
				if form_emo_quotations.is_valid():
					messages.add_message(request, messages.INFO, 'Quotation added!')	
					tmp = form_emo_quotations.save(commit=False)
					emotion_quotation(email=tmp.email,emotion=tmp.emotion,quotation=tmp.quotation,author=tmp.author).save()
					
					return HttpResponseRedirect('/#quotation')

			if 'form_emo_instructions' in request.POST:
				if form_emo_instructions.is_valid():
					messages.add_message(request, messages.INFO, 'Description added!')	
					tmp = form_emo_instructions.save(commit=False)
					emotion_instruction(email=tmp.email,emotion=tmp.emotion,quotation=tmp.quotation,why=tmp.why).save()
					
					return HttpResponseRedirect('/#instruction')


		else:
			form = FAQuserquestionsForm()
			form_emo_quotations = emotion_quotationForm()
			form_emo_instructions = emotion_instructionForm()

			

		#Get some stats
		email_quot_num = emotion_quotation.objects.order_by().values('email').distinct().count()
		email_inst_num = emotion_instruction.objects.order_by().values('email').distinct().count()
		emo_quot_num = emotion_quotation.objects.all().count()
		emo_inst_num = emotion_instruction.objects.all().count()
		
		

		
		context = {
			"form": form,
			"form_emo_quotations": form_emo_quotations,
			"form_emo_instructions": form_emo_instructions,
			'emo_quot_num': emo_quot_num,
		    'emo_inst_num': emo_inst_num,
		    'email_quot_num': email_quot_num,
		    'email_inst_num': email_inst_num,
		}			

		return render(request,"impending.html",context)
	else:
		return HttpResponseRedirect('/accounts/signup/')		


from allauth.account.views import SignupView

class SignupViewWithCustomForm(SignupView):
    form_class = SignupFormWithoutAutofocus

signup_view = SignupViewWithCustomForm.as_view()
