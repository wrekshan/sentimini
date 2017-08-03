from django.contrib import admin

# Register your models here
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import IdealText, TextLink, TextDescription, AlternateText, Quotation, QuickSuggestion, Beta, ActualText, PossibleText, Program, Timing, Tag, Carrier, UserSetting, Outgoing




class QuickSuggestionModelAdmin(admin.ModelAdmin):
	list_display = [
		"user",
		"text",
		"date",
		"added",
		"rejected",
		
	]
	list_display_links = ["date"]
	list_filter = ["user"]
	class Meta:
		model = QuickSuggestion

admin.site.register(QuickSuggestion,QuickSuggestionModelAdmin)

class QuotationModelAdmin(admin.ModelAdmin):
	list_display = [
		"user",
		"content",
		"source",
		
	]
	list_display_links = ["content"]
	list_filter = ["content"]
	class Meta:
		model = Quotation

admin.site.register(Quotation,QuotationModelAdmin)


class BetaModelAdmin(admin.ModelAdmin):
	list_display = [
		"user",
		"content",
		
	]
	list_display_links = ["content"]
	list_filter = ["content"]
	class Meta:
		model = Beta

admin.site.register(Beta,BetaModelAdmin)

class UserSettingModelAdmin(admin.ModelAdmin):
	list_display = [
		"user",
		"location",
		"timezone",
		"begin_date",
		"send_text",
		"send_text_tmp",
		"text_request_stop",
		"text_request_stop_tmp",
		"phone_input",
		"phone",
		"carrier",
		"sms_address",
		"research_check",
		"send_email_check",
		"send_text_check",
	]
	list_display_links = ["user"]
	list_filter = ["user"]
	class Meta:
		model = UserSetting

admin.site.register(UserSetting,UserSettingModelAdmin)


class OutgoingModelAdmin(admin.ModelAdmin):
	list_display = [
		"text",
		"date_sent",
	]
	list_display_links = ["date_sent"]
	list_filter = ["date_sent"]
	class Meta:
		model = Outgoing

admin.site.register(Outgoing,OutgoingModelAdmin)


class CarrierModelAdmin(admin.ModelAdmin):
	list_display = [
		"carrier",
		"sms_address",
	]
	list_display_links = ["carrier"]
	list_filter = ["carrier"]
	class Meta:
		model = Carrier

admin.site.register(Carrier,CarrierModelAdmin)


class TagModelAdmin(admin.ModelAdmin):
	list_display = [
		"user",
		"tag",
	]
	list_display_links = ["user"]
	list_filter = ["user"]
	class Meta:
		model = Tag

admin.site.register(Tag,TagModelAdmin)





class ActualTextModelAdmin(admin.ModelAdmin):
	list_display = [
		"user",
		"text",
		"alt_text",
		"text_sent",
		"time_to_send",
		"time_sent",
		"time_response",
		"response",
	]
	list_display_links = ["user"]
	list_filter = ["user","text"]
	class Meta:
		model = ActualText

admin.site.register(ActualText,ActualTextModelAdmin)



class TimingResource(resources.ModelResource):
	class Meta:
		model = Timing
		import_id_fields = ('intended_text_input',)
		# fields = ('intended_text', 'hour_start', 'hour_end','fuzzy','fuzzy_denomination','iti','iti_noise','monday','tuesday','wednesday','thursday','friday','saturday','sunday')
		fields = ('intended_text_input', 'text_type', 'hour_start', 'hour_end', 'repeat_in_window', 'fuzzy','fuzzy_denomination','iti_raw','iti_noise')


class TimingModelAdmin(ImportExportModelAdmin):
	resource_class = TimingResource   
	list_display = [
		"id",
		"user",
		"timing",
		'text_type',
		"default_timing",
		"repeat",
		"repeat_summary",
		"system_time",
		"show_user",
		"description",
		"date_start",
		"date_end",
		"hour_start",
		"hour_end",
		"fuzzy",
		"iti",
		"iti_noise",
		"repeat_in_window",
		"repeat_weeks",
		"monday",
		"tuesday",
		"wednesday",
		"thursday",
		"friday",
		"saturday",
		"sunday",
	]
	list_display_links = ["user"]
	list_filter = ["user","timing"]
	class Meta:
		model = Timing
		
admin.site.register(Timing,TimingModelAdmin)


class TextLinknResource(resources.ModelResource):
	class Meta:
		model = TextLink
		import_id_fields = ('input_text',)
		fields = ('intended_text','intended_text_type', 'link', 'link_display', 'input_text')


class TextLinkModelAdmin(ImportExportModelAdmin):
	resource_class = TextLinknResource   

	list_display = [
		"id",
		"link",
		"link_display",
		"intended_text_type",
		"intended_text",
		"input_text",
	]
	
	list_display_links = ["link_display"]
	list_filter = ["intended_text_type"]
	class Meta:
		model = TextLink
		
admin.site.register(TextLink,TextLinkModelAdmin)

class TextDescriptionResource(resources.ModelResource):
	class Meta:
		model = TextDescription
		import_id_fields = ('input_text',)
		fields = ('intended_text','intended_text_type', 'description','input_text')


class TextDescriptionModelAdmin(ImportExportModelAdmin):
	resource_class = TextDescriptionResource   

	list_display = [
		"id",
		"description",
		"intended_text_type",
		"intended_text",
		"input_text",
	]
	
	list_display_links = ["description"]
	list_filter = ["intended_text_type"]
	class Meta:
		model = TextDescription
		
admin.site.register(TextDescription,TextDescriptionModelAdmin)

class IdealTextResource(resources.ModelResource):
	class Meta:
		model = IdealText
		import_id_fields = ('input_text',)
		fields = ('input_text', 'text_type','intended_program', 'quick_suggestion','intended_tags')


class IdealTextModelAdmin(ImportExportModelAdmin):
	resource_class = IdealTextResource   

	list_display = [
		"id",
		"tmp_save",
		"text_type",
		"quick_suggestion",
		"user",
		"input_text",
		"text",
		"date_created",
	]
	list_display_links = ["user"]
	list_filter = ["user","text"]
	class Meta:
		model = IdealText
		
admin.site.register(IdealText,IdealTextModelAdmin)

class PossibleTextResource(resources.ModelResource):
	class Meta:
		model = PossibleText
		import_id_fields = ('input_text',)
		fields = ('input_text', 'text_type','intended_program', 'quick_suggestion','intended_tags')


class PossibleTextModelAdmin(ImportExportModelAdmin):
	resource_class = PossibleTextResource   

	list_display = [
		"id",
		"active",
		"tmp_save",
		"edit_type",
		"text_type",
		"quick_suggestion",
		"user",
		"input_text",
		"text",
		"date_created",
	]
	list_display_links = ["user"]
	list_filter = ["user","text","edit_type"]
	class Meta:
		model = PossibleText
		
admin.site.register(PossibleText,PossibleTextModelAdmin)


class AlternateTextResource(resources.ModelResource):
	class Meta:
		model = AlternateText
		import_id_fields = ('input_text',)
		fields = ('intended_text', 'alt_text', 'input_text')



#This is the other main workhorse that keeps user preferences.  
class AlternateTextModelAdmin(ImportExportModelAdmin):
	resource_class = AlternateTextResource   
	
	list_display = [
		"user",
		"alt_text",
		"intended_text",
	]
	list_display_links = ["alt_text"]
	list_filter = ["user"]
	class Meta:
		model = AlternateText

admin.site.register(AlternateText,AlternateTextModelAdmin)



class ProgramResource(resources.ModelResource):
	class Meta:
		model = Program
		import_id_fields = ('program_name',)
		fields = ('program', 'program_name', 'ordering', 'intended_tags', 'author', 'description', 'long_description')


class ProgramModelAdmin(ImportExportModelAdmin):
	resource_class = ProgramResource   


	list_display = [
		"id",
		"user",
		"program",
		"ordering",
	]
	list_display_links = ["user"]
	list_filter = ["user","program"]
	class Meta:
		model = Program
		
admin.site.register(Program,ProgramModelAdmin)


