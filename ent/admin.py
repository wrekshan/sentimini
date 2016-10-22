from django.contrib import admin

from .models import Carrier, Respite, UserSetting, Incoming, Outgoing, Ontology, Prompttext, UserGenPromptFixed, PossibleTextSTM, PossibleTextLTM, ActualTextSTM, ActualTextLTM, ExperienceSetting, ResponseTypeStore, ActualTextSTM_SIM

# Register your models here.
#NEW

from import_export import resources
from import_export.admin import ImportExportModelAdmin


class ExperienceSettingResource(resources.ModelResource):
	class Meta:
		model = ExperienceSetting
		import_id_fields = ('unique_text_set',)
		fields = ('text_set', 'ordering_num', 'unique_text_set', 'description', "description_long", 'tags', 'prompts_per_week','time_to_declare_lost','experience',)


class ExperienceSettingModelAdmin(ImportExportModelAdmin):
    resource_class = ExperienceSettingResource   
    list_filter = ["user", "experience"]

    list_display = [
		"user",
		"text_set",
		"ordering_num",
		"unique_text_set",
		"tags",
		"description",
		"description_long",
		"prompts_per_week",
		"experience",
		"id",
		"ideal_id",
		"user_state",
		"active",
		"prompt_interval_minute_avg",
		"prompt_interval_minute_min",
		"prompt_interval_minute_max",
		"time_to_declare_lost",
		"research_instr_dim_rate",
		"research_prompt_multiple_rate",
	]


admin.site.register(ExperienceSetting,ExperienceSettingModelAdmin)




class PossibleTextSTMResource(resources.ModelResource):
	class Meta:
		model = PossibleTextSTM
		import_id_fields = ('csv_id',)
		fields = ('csv_id','text','text_set', 'unique_text_set', 'text_importance', 'response_type', 'text_type',)



class PossibleTextSTMModelAdmin(ImportExportModelAdmin):
	resource_class = PossibleTextSTMResource  
	
	list_display = [
		"user",
		"text",
		"csv_id",
		"system_text",
		"experience_id",
		"text_set",
		"unique_text_set",
		"text_type",
		"text_importance",
		"response_type",
		"show_user",
		"date_created",
		"date_altered",
	]

	list_filter = ["user","text_set","text_type"]

admin.site.register(PossibleTextSTM,PossibleTextSTMModelAdmin)

class ATSMSIM_ModelAdmin(admin.ModelAdmin):
	list_display = [
		"user",
		"text_id",
		"experience_id",
		"response_time",
		"text_set",
		"textstore_id",
		"time_to_add",
		"system_text",
		"text",
		"consolidated",
		"ready_for_next",
		"series",
		"failed_series",
		"response",
		"response_type",
		"text_type",
		"time_to_send",
		"time_sent",
		"simulated",
	]
	list_display_links = ["user"]
	list_filter = ["user"]
	class Meta:
		model = ActualTextSTM_SIM

admin.site.register(ActualTextSTM_SIM,ATSMSIM_ModelAdmin)


class ResponseTypeStoreModelAdmin(admin.ModelAdmin):
	list_display = [
		"response_type",
		"ordering_num",
	]
	list_display_links = ["response_type"]
	list_filter = ["response_type"]
	class Meta:
		model = ResponseTypeStore

admin.site.register(ResponseTypeStore,ResponseTypeStoreModelAdmin)





class PossibleTextLTMModelAdmin(admin.ModelAdmin):
	list_display = [
		"user",
		"stm_id",
		"text",
		"experience_id",
		"text_set",
		"text_type",
		"text_importance",
		"response_type",
		"show_user",
		"date_created",
		"date_altered",
	]
	list_display_links = ["user"]
	list_filter = ["user"]
	class Meta:
		model = PossibleTextLTM

admin.site.register(PossibleTextLTM,PossibleTextLTMModelAdmin)

class ActualTextSTMModelAdmin(admin.ModelAdmin):
	list_display = [
		"user",
		"response_type",
		"text_id",
		"experience_id",
		"text_set",
		"textstore_id",
		"time_to_add",
		"system_text",
		"text",
		"consolidated",
		"ready_for_next",
		"series",
		"failed_series",
		"response",
		"text_type",
		"time_to_send",
		"time_sent",
		"simulated",
	]
	list_display_links = ["user"]
	list_filter = ["user","text_set","text_type"]
	class Meta:
		model = ActualTextSTM

admin.site.register(ActualTextSTM,ActualTextSTMModelAdmin)


class ActualTextLTMModelAdmin(admin.ModelAdmin):
	list_display = [
		"user",
		"text_id",
		"stm_id",
		"experience_id",
		"text_set",
		"textstore_id",
		"text",
		"time_to_send_circa",
		"time_to_send_day",
		"series",
		"failed_series",
		"text_type",
		"response_type",
		"response",
		"response_cat",
		"response_cat_bin",
		"response_dim",
		"time_response",
		"time_to_send",
		"time_sent",
		"simulated",
	]
	list_display_links = ["user"]
	list_filter = ["user"]
	class Meta:
		model = ActualTextLTM

admin.site.register(ActualTextLTM,ActualTextLTMModelAdmin)





class UserSettingModelAdmin(admin.ModelAdmin):
	list_display = [
		"user",
		"active_experiences",
		"new_user_pages",
		"begin_date",
		"send_text",
		"text_request_stop",
		"respite_until_datetime",
		"prompts_per_week",
		"phone",
		"carrier",
		"sms_address",
		"timezone",
		"sleep_time",
		"sleep_duration",
	]
	list_display_links = ["user"]
	list_filter = ["user"]
	class Meta:
		model = UserSetting

admin.site.register(UserSetting,UserSettingModelAdmin)


class RespiteModelAdmin(admin.ModelAdmin):
	list_display = ["user","date_request","respite_type"]
	list_display_links = ["user"]
	list_filter = ["user"]
	search_fields = ["user"]
	class Meta:
		model = Respite

admin.site.register(Respite,RespiteModelAdmin)

class CarrierModelAdmin(admin.ModelAdmin):
	list_display = ["carrier","sms_address"]
	list_display_links = ["carrier","sms_address"]
	list_filter = ["carrier","sms_address"]
	class Meta:
		model = Carrier

admin.site.register(Carrier,CarrierModelAdmin)


class IncomingModelAdmin(admin.ModelAdmin):
	list_display = ["email_user","email_date","email_content","processed"]
	list_display_links = ["email_user"]
	list_filter = ["email_user"]
	search_fields = ["email_user"]
	class Meta:
		model = Incoming

admin.site.register(Incoming,IncomingModelAdmin)

class OutgoingModelAdmin(admin.ModelAdmin):
	list_display = ["addressee","date_sent","message","entry_id"]
	list_display_links = ["addressee"]
	list_filter = ["addressee"]
	search_fields = ["addressee"]
	class Meta:
		model = Outgoing

admin.site.register(Outgoing,OutgoingModelAdmin)



class OntologyModelAdmin(admin.ModelAdmin):
	list_display = ["ontological_name","ontological_type","prompt_set","prompt_set_percent"]
	list_display_links = ["ontological_name"]
	list_filter = ["ontological_name"]
	search_fields = ["ontological_name"]
	class Meta:
		model = Ontology

admin.site.register(Ontology,OntologyModelAdmin)


class PrompttextModelAdmin(admin.ModelAdmin):
	list_display = ["text","text_type","text_percent"]
	list_display_links = ["text"]
	list_filter = ["text"]
	search_fields = ["text"]
	class Meta:
		model = Prompttext

admin.site.register(Prompttext,PrompttextModelAdmin)

class UserGenPromptFixedModelAdmin(admin.ModelAdmin):
	list_display = ["id","user","prompt","date_created","begin_datetime","end_datetime", "repeat_denomination", "repeat_number"]
	list_display_links = ["user","prompt"]
	list_filter = ["user","prompt"]
	search_fields = ["user","prompt"]
	
	class Meta:
		model = UserGenPromptFixed

admin.site.register(UserGenPromptFixed,UserGenPromptFixedModelAdmin)







