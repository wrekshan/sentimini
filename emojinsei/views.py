from django.shortcuts import render

# from ent.models import UserSetting

def landing_page(request):
	if request.user.is_authenticated():	
		#test is has working settings
		if UserSetting.objects.all().filter(user=request.user).count() < 1:
			working_settings = UserSetting(user=request.user)
			working_settings.save()
			print("New User - Working Settings Saved")
		else:
			print("User has Settings")

	return render(request,"index.html")