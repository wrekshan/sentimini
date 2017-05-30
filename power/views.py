from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse
import json

# Create your views here.
def home(request):	
	context = {}
	return render(request,"POWER_home.html",context)


def get_overview_options(request):
	main_context = {} # to build out the specific html stuff
	response_data = {} # to send back to the template

	response_data["power_overview_options"] = render_to_string('POWER_overview_options.html', main_context, request=request)
	return HttpResponse(json.dumps(response_data),content_type="application/json")

def get_measure(request):
	print("GET MEASURE")
	main_context = {} # to build out the specific html stuff
	response_data = {} # to send back to the template
	
	main_context['measure_number'] = request.POST['measure_number']

	response_data["measure_option"] = render_to_string('POWER_measure.html', main_context, request=request)
	return HttpResponse(json.dumps(response_data),content_type="application/json")	

def get_output(request):
	main_context = {} # to build out the specific html stuff
	response_data = {} # to send back to the template

	response_data["power_output"] = render_to_string('POWER_output.html', main_context, request=request)
	return HttpResponse(json.dumps(response_data),content_type="application/json")	