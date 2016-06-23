from django.shortcuts import render, render_to_response
from chatterbot import ChatBot
from chatterbot.training.trainers import ChatterBotCorpusTrainer

from datetime import datetime
import parsedatetime as pdt

from chatterbot.training.trainers import ListTrainer

chatterbot = ChatBot("new", read_only=True)
chatterbot.set_trainer(ChatterBotCorpusTrainer)
chatterbot.train(
    "chatterbot.corpus.english.greetings",
    "chatterbot.corpus.english.conversations"
)



chatterbot.set_trainer(ListTrainer)

chatterbot.train([
    "meow",
    "do you want to see a chat picture?",
])

# chatterbot.train([
#     "Greetings!",
#     "Hello",
# ])

# chatbot = ChatBot("Ron Obvious")
# chatbot.set_trainer(ChatterBotCorpusTrainer)
# chatbot.train("chatterbot.corpus.english")

# Create your views here.

def chat(request):
	#!/usr/bin/env python

	prompt = "meow"
	chatter = chatterbot.get_response(prompt)
	context = {
			"chatter": chatter,
			"prompt": prompt,
	}		

	

	return render_to_response('chat.html',context)

