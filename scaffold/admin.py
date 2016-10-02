from django.contrib import admin

from .models import Blog, Business, Measure, Sentimini_help
# Register your models here.
class Sentimini_helpAdmin(admin.ModelAdmin):
	list_display = ["user","help_heading","help_content","help_type","major_cat","minor_cat","level"]
	list_display_links = ["help_heading"]
	list_filter = ["user"]
	search_fields = ["user"]

	class Meta:
		model = Sentimini_help

admin.site.register(Sentimini_help,Sentimini_helpAdmin)


class MeasureAdmin(admin.ModelAdmin):
	list_display = ["user","name","measure","super_measure","super_measure","population","minval","maxval","mean","sd","distr","response_rate"]
	list_display_links = ["user"]
	list_filter = ["user"]
	search_fields = ["user"]

	class Meta:
		model = Measure

admin.site.register(Measure,MeasureAdmin)


class BusinessAdmin(admin.ModelAdmin):
	list_display = ["user","con_price_per_outgoing","con_number_outgoing_per_free_per_day"]
	list_display_links = ["user"]
	list_filter = ["user"]
	search_fields = ["user"]

	class Meta:
		model = Business

admin.site.register(Business,BusinessAdmin)


class BlogAdmin(admin.ModelAdmin):
	list_display = ["user","author","title","content","date_created","date_altered"]
	list_display_links = ["title"]
	list_filter = ["title"]
	search_fields = ["title"]

	class Meta:
		model = Blog

admin.site.register(Blog,BlogAdmin)

