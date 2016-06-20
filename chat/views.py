from django.shortcuts import render, render_to_response
# from chatterbot import ChatBot
# from chatterbot.training.trainers import ChatterBotCorpusTrainer

from datetime import datetime
import parsedatetime as pdt



# Create your views here.

def chat(request):
	#!/usr/bin/env python


	cal = pdt.Calendar()
	now = datetime.now()
	time_string = "pause 1 hour"

	dater = cal.parseDT(time_string, now)[0]

	differ = now - dater
	differ = differ.total_seconds()

	print(differ)

	if -100 < differ < 100:
		print("hmmm")



	

	return render_to_response('index_not_logged_in.html')

