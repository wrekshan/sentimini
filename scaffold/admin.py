from django.contrib import admin

from .models import FAQ, FAQuserquestions, emotion_quotation, emotion_instruction, emotion_statement_display, Blog, Business, Measure, Sentimini_help
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
	list_display = ["user","author","title","content","the_tags","date_created","date_altered"]
	list_display_links = ["title"]
	list_filter = ["title"]
	search_fields = ["title"]
	def the_tags(self, obj):
		return "%s" % (obj.tags.all(), )
	the_tags.short_description = 'tags'

	class Meta:
		model = Blog

admin.site.register(Blog,BlogAdmin)


class FAQAdmin(admin.ModelAdmin):
	list_display = ["question","answer","category","date_created","date_updated","active"]
	list_display_links = ["question"]
	list_filter = ["category"]
	search_fields = ["question","category"]

	class Meta:
		model = FAQ

admin.site.register(FAQ,FAQAdmin)

class FAQuserquestionsAdmin(admin.ModelAdmin):
	list_display = ["user","question","date_created"]
	list_display_links = ["question"]
	list_filter = ["question"]
	search_fields = ["question"]
	class Meta:
		model = FAQuserquestions

admin.site.register(FAQuserquestions,FAQuserquestionsAdmin)




class emotion_statement_displayAdmin(admin.ModelAdmin):
	list_display = ["emotion","statement_type","show_me","number_of_likes","emotion_id","statement","author"]
	list_display_links = ["emotion"]
	list_filter = ["emotion"]
	search_fields = ["emotion"]
	class Meta:
		model = emotion_statement_display

admin.site.register(emotion_statement_display,emotion_statement_displayAdmin)



class emotion_quotationAdmin(admin.ModelAdmin):
	list_display = ["emotion","quotation","author"]
	list_display_links = ["emotion"]
	list_filter = ["emotion"]
	search_fields = ["emotion"]
	class Meta:
		model = emotion_quotation

admin.site.register(emotion_quotation,emotion_quotationAdmin)


class emotion_instructionAdmin(admin.ModelAdmin):
	list_display = ["emotion","quotation","why"]
	list_display_links = ["emotion"]
	list_filter = ["emotion"]
	search_fields = ["emotion"]
	class Meta:
		model = emotion_instruction

admin.site.register(emotion_instruction,emotion_instructionAdmin)