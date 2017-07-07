from django.contrib import admin

# Register your models here.
from .models import Person, Group
class PersonModelAdmin(admin.ModelAdmin):
	list_display = [
		"creator",
		"person",
		"phone_input",
		"verified",
		"accepted",
		
	]
	list_display_links = ["creator"]
	list_filter = ["creator"]
	class Meta:
		model = Person

admin.site.register(Person,PersonModelAdmin)

class GroupModelAdmin(admin.ModelAdmin):
	list_display = [
		"creator",
		"group",		
	]
	list_display_links = ["creator"]
	list_filter = ["creator"]
	class Meta:
		model = Group

admin.site.register(Group,GroupModelAdmin)