from django.contrib import admin

from .models import Carrier, Respite, Entry, UserSetting, Emotion, NewUserPrompt, UserGenPrompt, Incoming, Outgoing

# Register your models here.




class EntryModelAdmin(admin.ModelAdmin):
	list_display = [
		"id",
		"user",
		"prompt",
		"time_to_send",
		"time_sent",
		"send_next_immediately",
		"ready_for_next",
		"prompt_reply",
		"prompt_type",
		"series",
		"failed_series",
		"response_time_seconds",
		"time_created",
		"time_response",
	]
	list_display_links = ["prompt"]
	list_filter = [
		"user",
		"prompt",
	]
	class Meta:
		model = Entry

admin.site.register(Entry,EntryModelAdmin)

class UserSettingModelAdmin(admin.ModelAdmin):
	list_display = [
		"user",
		"send_text",
		"teaching_period_on",
		"text_request_stop",
		"respite_until_datetime",
		"prompts_per_day",
		"prompt_interval_minute_avg",
		"prompt_interval_minute_min",
		"prompt_interval_minute_max",
		"phone",
		"carrier",
		"sms_address",
		"timezone",
		"sleep_time",
		"sleep_duration",
		"emotion_core_rate",
		"emotion_top100_rate",
		"emotion_other_rate",
		"user_generated_prompt_rate",
		"prompt_multiple_rate",
		"instruction_rate",
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

class NewUserPromptModelAdmin(admin.ModelAdmin):
	list_display = ["prompt","prompt_type","NUP_seq","send_next_immediately"]
	list_display_links = ["prompt"]
	list_filter = ["prompt"]
	search_fields = ["prompt"]
	list_editable = ["prompt_type","NUP_seq","send_next_immediately"]
	class Meta:
		model = NewUserPrompt

admin.site.register(NewUserPrompt,NewUserPromptModelAdmin)

class UserGenPromptModelAdmin(admin.ModelAdmin):
	list_display = ["user","prompt","date_created","active","show_user"]
	list_display_links = ["user","prompt"]
	list_filter = ["user","prompt"]
	search_fields = ["user","prompt"]
	
	class Meta:
		model = UserGenPrompt

admin.site.register(UserGenPrompt,UserGenPromptModelAdmin)

class EmotionModelAdmin(admin.ModelAdmin):
	list_display = ["emotion","emotion_type"]
	list_display_links = ["emotion"]
	list_filter = ["emotion"]
	search_fields = ["emotion"]
	class Meta:
		model = Emotion

admin.site.register(Emotion,EmotionModelAdmin)