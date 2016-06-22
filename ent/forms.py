from django import forms
from django.forms import widgets, Select, RadioSelect
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Submit
import pytz

from .models import Carrier, Entry, UserSetting, UserGenPrompt

#This allows the user to input their own prompts.  Because this is a model set, I don't know how to use the help_texts/labels.  

class UserSettingForm_PromptRate(forms.ModelForm):
	#These are declared here to get the choice field
	

	class Meta:
		model = UserSetting

		fields = [
			"user_generated_prompt_rate",	
		]

		labels = {
            'user_generated_prompt_rate': ('Prompt Percent'),   
        }

		help_texts = {
        	'user_generated_prompt_rate': ('0 = All default texts.  50 = Half default/half user generated.  100 = All user generated prompts.'),
        	
        }

	def __init__(self, *args, **kwargs):
		super(UserSettingForm_PromptRate, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.render_required_fields = True
		self.helper.label_class = 'col-lg-2'
		self.helper.field_class = 'col-lg-5'


class ExampleFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(ExampleFormSetHelper, self).__init__(*args, **kwargs)
        self.form_method = 'post'
        self.render_required_fields = True
        self.label_class = 'col-lg-3'
        self.field_class = 'col-lg-9'


class UserGenPromptForm(forms.ModelForm):
	helper = FormHelper()
	
	class Meta:
		model = UserGenPrompt
		fields = [
			"prompt",
			"show_user",
		]

		labels = {
            'prompt': ('Prompt'),
            'show_user': ('Delete'),
        }

		

	def __init__(self, *args, **kwargs):
		super(UserGenPromptForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'id-form'
		self.helper.form_class = 'form-horizontal'
		self.helper.form_method = 'post'
		self.helper.label_class = 'col-lg-1'
		self.helper.field_class = 'col-lg-10'
		self.helper.form_action = 'login'
		self.fields['prompt'].widget.attrs['placeholder'] = 'Add new prompt here (i.e."The world is beautiful and good")'
		self.helper.add_input(Submit('submit', 'Submit'))
		

#Main form used to set the user settings
class UserSettingForm_Prompt(forms.ModelForm):
	#These are declared here to get the choice field
	timezone = forms.ChoiceField(choices=[(x, x) for x in pytz.common_timezones],label="Timezone")
	carrier = forms.ChoiceField(choices=[(x, x) for x in Carrier.objects.all()],label="Carrier")
	

	class Meta:
		model = UserSetting

		fields = [
			"phone",
			"carrier",
			"sleep_time",
			"sleep_duration",
			"timezone",
			"prompts_per_day",
		
		]

		labels = {
            'sleep_time': ('Bed Time'),
            'sleep_duration': ('Time Asleep (Hours)'),
            'prompts_per_day': ('Texts per day?'),
        
        }

		help_texts = {
			'phone': (''),
        	'sleep_time': (''),
        	'sleep_duration': (''),
        	'prompts_per_day': (''),
        
        	
        }

	def __init__(self, *args, **kwargs):
		super(UserSettingForm_Prompt, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'id-form'
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-lg-3'
		self.helper.field_class = 'col-lg-9'
		self.helper.form_method = 'post'
		self.helper.form_action = 'login'
		# self.helper.add_input(Submit('submit', 'Submit'))




