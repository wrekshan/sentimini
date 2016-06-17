from django import forms
from django.forms import widgets, Select, RadioSelect
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Submit
import pytz

from .models import Carrier, Entry, UserSetting, UserGenPrompt

#This allows the user to input their own prompts.  Because this is a model set, I don't know how to use the help_texts/labels.  

class UserGenPromptForm(forms.ModelForm):
	helper = FormHelper()
	
	class Meta:
		model = UserGenPrompt
		fields = [
			"prompt",
			"active",
			"show_user",
		]

		labels = {
            'prompt': ('When do you usually go to bed?'),
            'active': ('How many hours do you usually sleep?'),
            'show_user': ('Delete'),
        }

		help_texts = {
			'prompt': ('When do you usually go to bed?'),
            'active': ('How many hours do you usually sleep?'),
            'show_user': ('On average, how many prompts do you want per day?'),
        }

	def __init__(self, *args, **kwargs):
		super(UserGenPromptForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'id-form'
		self.helper.form_class = 'form-horizontal'
		self.helper.form_method = 'post'
		self.helper.form_action = 'login'
		self.helper.add_input(Submit('submit', 'Submit'))
		self.helper.layout = Layout(
            Field('prompt'),
            Field('active'),
            Field('show_user'),
        )

#Main form used to set the user settings
class UserSettingForm_Prompt(forms.ModelForm):
	#These are declared here to get the choice field
	timezone = forms.ChoiceField(choices=[(x, x) for x in pytz.common_timezones],label="What timezone are you currently in? (Please update this if you travel)")
	carrier = forms.ChoiceField(choices=[(x, x) for x in Carrier.objects.all()],label="Carrier (this is needed to be able to text you)")
	

	class Meta:
		model = UserSetting

		fields = [
			"phone",
			"carrier",
			"sleep_time",
			"sleep_duration",
			"timezone",
			"prompts_per_day",
			"user_generated_prompt_rate",	
		]

		labels = {
            'sleep_time': ('When do you usually go to bed?'),
            'sleep_duration': ('How many hours do you usually sleep?'),
            'prompts_per_day': ('On average, how many prompts do you want per day?'),
            'user_generated_prompt_rate': ('Percentage of prompts from user generated list?'),   
        }

		help_texts = {
			'phone': ('CHANGE THIS: No dashes or anything yet.  Just XXXXXXXXXX'),
        	'sleep_time': ('CHANGE THIS: We try not to text you when you are asleep'),
        	'sleep_duration': ('CHANGE THIS: We try not to text you when you are asleep'),
        	'prompts_per_day': ('ADVANCED OPTION: Please note that this is only an average'),
        	'user_generated_prompt_rate': ('ADVANCED OPTION: 0 = All emotion questions, 100 = All user generated prompts'),
        	
        }

	def __init__(self, *args, **kwargs):
		super(UserSettingForm_Prompt, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'id-form'
		self.helper.form_class = 'form-horizontal'
		self.helper.form_method = 'post'
		self.helper.form_action = 'login'
		self.helper.add_input(Submit('submit', 'Submit'))



