from django.contrib import admin

# Register your models here
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import ActualText, PossibleText, Collection, Timing, Tag, Carrier, UserSetting, Outgoing


#This is the other main workhorse that keeps user preferences.  
class UserSettingModelAdmin(admin.ModelAdmin):
	list_display = [
		"user",
		"begin_date",
		"send_text",
		"send_text_tmp",
		"text_request_stop",
		"phone_input",
		"phone",
		"carrier",
		"sms_address",
		"timezone",
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
		import_id_fields = ('intended_text',)
		# fields = ('intended_text', 'hour_start', 'hour_end','fuzzy','fuzzy_denomination','iti','iti_noise','monday','tuesday','wednesday','thursday','friday','saturday','sunday')
		fields = ('intended_text', 'hour_start', 'hour_end','fuzzy','fuzzy_denomination','iti_raw','iti_noise')


class TimingModelAdmin(ImportExportModelAdmin):
	resource_class = TimingResource   

	list_display = [
		"id",
		"user",
		"timing",
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



class PossibleTextResource(resources.ModelResource):
	class Meta:
		model = PossibleText
		import_id_fields = ('text',)
		fields = ('intended_collection', 'text', 'intended_tags')


class PossibleTextModelAdmin(ImportExportModelAdmin):
	resource_class = PossibleTextResource   

	list_display = [
		"id",
		"active",
		"user",
		"text",
		"date_created",
	]
	list_display_links = ["user"]
	list_filter = ["user","text"]
	class Meta:
		model = PossibleText
		
admin.site.register(PossibleText,PossibleTextModelAdmin)



class CollectionResource(resources.ModelResource):
	class Meta:
		model = Collection
		import_id_fields = ('collection_name',)
		fields = ('collection', 'collection_name', 'intended_tags', 'description')


class CollectionModelAdmin(ImportExportModelAdmin):
	resource_class = CollectionResource   


	list_display = [
		"id",
		"user",
		"collection",
	]
	list_display_links = ["user"]
	list_filter = ["user","collection"]
	class Meta:
		model = Collection
		
admin.site.register(Collection,CollectionModelAdmin)


