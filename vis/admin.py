from django.contrib import admin
from .models import EntryDEV, UserSettingDEV, EntryDEVSUM, EmotionToShow

# Register your models here.
class EntryDEVSUMModelAdmin(admin.ModelAdmin):
	list_display = [
		"id",
		"user",
		"analysis",
		"time_to_send_day",
		"test_user",
		"prompt",
		"prompt_type",
		"prompt_reply_avg",
		"prompt_reply_count",
	]
	list_display_links = ["prompt"]
	list_filter = [
		"user",
		"prompt",
	]
	class Meta:
		model = EntryDEVSUM

admin.site.register(EntryDEVSUM,EntryDEVSUMModelAdmin)

class EmotionToShowModelAdmin(admin.ModelAdmin):
	list_display = [
		"user",
		"emotion",
		"emotion_id",
		"show_me_graph",
	]
	list_display_links = ["emotion_id"]
	list_filter = [
		"user",
		"emotion",
	]
	class Meta:
		model = EmotionToShow

admin.site.register(EmotionToShow,EmotionToShowModelAdmin)


class EntryDEVModelAdmin(admin.ModelAdmin):
	list_display = [
		"id",
		"user",
		"prompt",
		"prompt_id",
		"time_to_send_circa",
		"time_to_send",
		"time_sent",
		"send_next_immediately",
		"ready_for_next",
		"prompt_reply",
		"prompt_type",
		"series",
		"failed_series",
		"response_time",
		"time_created",
		"time_response",
	]
	list_display_links = ["prompt"]
	list_filter = [
		"user",
		"prompt",
	]
	class Meta:
		model = EntryDEV

admin.site.register(EntryDEV,EntryDEVModelAdmin)

class UserSettingDEVModelAdmin(admin.ModelAdmin):
	list_display = [
		"user",
		"setting_name",
		"exp_response_rate",
		"exp_response_time_avg",
		"exp_response_time_min",
		"exp_response_time_max",
		"time_to_declare_lost",
		"num_to_gen",
		"begin_date",
		"prompts_per_week",
		"text_interval_minute_avg",
		"text_interval_minute_min",
		"text_interval_minute_max",
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
		model = UserSettingDEV

admin.site.register(UserSettingDEV,UserSettingDEVModelAdmin)