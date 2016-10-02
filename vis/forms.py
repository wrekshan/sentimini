from django import forms
from django.forms import widgets, Select, RadioSelect
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Submit
import pytz

from .models import EntryDEV, UserSettingDEV, EmotionToShow



#This allows the user to input their own prompts.  Because this is a model set, I don't know how to use the help_texts/labels.  

#Main form used to set the user settings

# class CurrentViewForm(forms.Form):
			#These are declared here to get the choice field
			# setting_name = forms.ChoiceField(choices=[],label="setting_name")


class EmotionToShowForm(forms.ModelForm):
	#These are declared here to get the choice field
	class Meta:
		model = EmotionToShow

		fields = [
			"emotion",
			"show_me_graph",
		]

		labels = {
            'emotion': ('Emotion'),
            'show_me_graph': ('Do you want to show?'),
        }

		help_texts = {
        	'emotion': (''),
        	'show_me_graph': (''),
        }

	def __init__(self, *args, **kwargs):
		super(EmotionToShowForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'id-form'
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-lg-2'
		self.helper.field_class = 'col-lg-2'
		self.helper.form_method = 'post'
		self.helper.form_action = 'login'		

class ExampleFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(ExampleFormSetHelper, self).__init__(*args, **kwargs)
        self.form_method = 'post'
        self.render_required_fields = True
        self.label_class = 'col-lg-3'
        self.field_class = 'col-lg-9'
	
class UserSettingDEVForm_RUN(forms.ModelForm):
	#These are declared here to get the choice field
	class Meta:
		model = UserSettingDEV

		fields = [
			"setting_name",
			"num_to_gen",

			
		]

		labels = {
            'setting_name': ('Setting Name'),
            'num_to_gen': ('Number to generate'),
        }

		help_texts = {
        	'setting_name': (''),
        	'num_to_gen': (''),
        }

	def __init__(self, *args, **kwargs):
		super(UserSettingDEVForm_RUN, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'id-form'
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-lg-2'
		self.helper.field_class = 'col-lg-2'
		self.helper.form_method = 'post'
		self.helper.form_action = 'login'


class UserSettingDEVForm(forms.ModelForm):
	#These are declared here to get the choice field
	class Meta:
		model = UserSettingDEV

		fields = [
			"sleep_time",
			"sleep_duration",
			"prompts_per_week",
			"prompt_interval_minute_avg",
			"prompts_per_week",
			"prompt_interval_minute_min",
			"prompt_interval_minute_max",
			"emotion_core_rate",
			"emotion_top100_rate",
			"emotion_other_rate",
			"user_generated_prompt_rate",
			"prompt_multiple_rate",
			"exp_response_rate",
			"exp_response_time_avg",
			"exp_response_time_min",
			"exp_response_time_max",
			"time_to_declare_lost",

			
		]

		labels = {
            'sleep_time': ('Bed Time'),
            'sleep_duration': ('Time Asleep (Hours)'),
        }

		help_texts = {
        	'sleep_time': (''),
        	'sleep_duration': (''),
        }

	def __init__(self, *args, **kwargs):
		super(UserSettingDEVForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'id-form'
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-lg-2'
		self.helper.field_class = 'col-lg-2'
		self.helper.form_method = 'post'
		self.helper.form_action = 'login'
		# self.helper.add_input(Submit('submit', 'Submit'))

# class UserSettingForm_Prompt_Paid(forms.ModelForm):
# 	#These are declared here to get the choice field
# 	class Meta:
# 		model = UserSettingDEV

# 		fields = [
# 			"prompts_per_week",
# 		]

# 		labels = {
#             'prompts_per_week': ('Texts per day?'),
        
#         }

# 		help_texts = {
#         	'prompts_per_week': (''),
#         }

# 	def __init__(self, *args, **kwargs):
# 		super(UserSettingForm_Prompt_Paid, self).__init__(*args, **kwargs)
# 		self.helper = FormHelper()
# 		self.helper.form_id = 'id-form'
# 		self.helper.form_class = 'form-horizontal'
# 		self.helper.label_class = 'col-sm-2'
# 		self.helper.field_class = 'col-sm-2'
# 		self.helper.form_method = 'post'
# 		self.helper.form_action = 'login'
# 		# self.helper.add_input(Submit('submit', 'Submit'))




