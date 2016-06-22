from django.shortcuts import render

# Create your views here.
def faq(request):
	if request.user.is_authenticated():	
	#don't forget to add form for user generated question

		context = {
					"pizza": "pizza",
				}

		return render(request,"faq.html",context)
	else:
		return HttpResponseRedirect('/accounts/signup/')

