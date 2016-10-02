from django import forms
from django.forms import widgets, Select, RadioSelect
from django.contrib.admin import widgets     
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Submit, Layout, Div, Field, Fieldset, MultiField
import pytz
from datetimewidget.widgets import DateTimeWidget, DateWidget, TimeWidget

from .models import Carrier, ActualTextSTM, UserSetting, Ontology, PossibleTextSTM, ResponseTypeStore, UserGenPromptFixed, ExperienceSetting

#This allows the user to input their own prompts.  Because this is a model set, I don't know how to use the help_texts/labels.  
class ExampleFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(ExampleFormSetHelper, self).__init__(*args, **kwargs)
        self.form_method = 'post'
        self.render_required_fields = True
        self.template = 'WR_table_inline_formset_help.html'
        self.label_class = 'col-lg-0'
        self.field_class = 'col-lg-12'
        self.add_input(Submit('submit_formset', 'Submit'))
        self.form_class = 'form-horizontal'
        

class PossibleTextSTMForm_detail(forms.ModelForm):
	helper = FormHelper()
	
	response_type = forms.ChoiceField(choices=[(x, x) for x in ResponseTypeStore.objects.all().order_by('ordering_num')])
	class Meta:
		model = PossibleTextSTM
		fields = [
			"text",
			"response_type",
			"text_importance",
			"show_user",
		]

		labels = {
            'text': ('Text'),
            'response_type': ('Response Type'),
            'text_importance': ('Importance'),
            'show_user': ('Delete'),            
        }

	def __init__(self, *args, **kwargs):
		super(PossibleTextSTMForm_detail, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'id-form'

		self.helper.form_method = 'post'
		self.helper.form_action = 'login'		
		self.helper.add_input(Submit('submit_possible_text', 'Submit'))
		self.fields['text'].widget.attrs['placeholder'] = 'Add new prompt here (i.e."The world is beautiful and good")'


class PossibleTextSTMForm(forms.ModelForm):
	helper = FormHelper()
	
	response_type = forms.ChoiceField(choices=[(x, x) for x in ResponseTypeStore.objects.all().order_by('ordering_num')])
	class Meta:
		model = PossibleTextSTM
		fields = [
			"text",
			"response_type",
			"text_importance",
			"show_user",
		]

		labels = {
            'text': ('Text'),
            'response_type': ('Response Type'),
            'text_importance': ('Importance'),
            'show_user': ('Delete'),            
        }

		
        
	

	def __init__(self, *args, **kwargs):
		super(PossibleTextSTMForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'id-form'
		self.helper.form_method = 'post'
		self.helper.form_action = 'login'		
		self.fields['text'].widget.attrs['placeholder'] = 'Add new prompt here (i.e."The world is beautiful and good")'



class UserGenPromptFixedFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(UserGenPromptFixedFormSetHelper, self).__init__(*args, **kwargs)
        self.form_method = 'post'
        self.render_required_fields = True
        self.template = 'WR_table_inline_formset_UGPF.html'
        self.add_input(Submit('submit_UGPF_formset', 'Submit'))
        self.form_class = 'form-horizontal'
        


class UserGenPromptFixedForm(forms.ModelForm):
	helper = FormHelper()
	
	response_type = forms.ChoiceField(choices=[(x, x) for x in ResponseTypeStore.objects.all().order_by('ordering_num')])

	begin_datetime = forms.DateTimeField(label='Date to Send',input_formats = ['%H:%M %m/%d/%y'], required = True, widget=DateTimeWidget(usel10n=False, bootstrap_version=3, options={'showMeridian': True, 'clearBtn': False, 'format': 'hh:ii mm/dd/yy'}))
	end_datetime = forms.DateTimeField(label='Until',input_formats = ['%H:%M %m/%d/%y'], required = True, widget=DateTimeWidget(usel10n=False, bootstrap_version=3, options={'showMeridian': True, 'clearBtn': False, 'format': 'hh:ii mm/dd/yy'}))
	# begin_datetime = forms.DateField(widget=DateTimePicker(options={"format": "YYYY-MM-DD HH:mm:ss","pick12HourFormat":True,"inline": True,"sideBySide":True}))
	# begin_datetime = forms.DateField()
	# end_datetime = forms.DateField(widget=DateTimePicker(options={"format": "YYYY-MM-DD HH:mm","pickTime": True}))
	

	class Meta:
		model = UserGenPromptFixed
		fields = [
			"prompt",
			"response_type",
			"begin_datetime",
			"hr_range",
			"repeat_number",
			"repeat_denomination",
			"end_datetime",
			"show_user",
		]

		labels = {
            'prompt': ('Prompt'),
            'response_type': ('Response Type'),
            'begin_datetime': ('Date to Send'),
            'hr_range': ('Range'),
            'repeat_number': ('Repeat every'),
            'repeat_denomination': ('Unit'),
            'end_datetime': ('Until'),
            'show_user': ('Delete'),            
        }
		
        
	  

	def __init__(self, *args, **kwargs):
		super(UserGenPromptFixedForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'id-form'
		self.helper.form_method = 'post'
		self.helper.form_action = 'login'	
		self.helper.add_input(Submit('submit_UGPF_formset', 'Submit'))	
		self.fields['prompt'].widget.attrs['placeholder'] = 'Add new prompt here (i.e."The world is beautiful and good")'
		


class EmotionOntologyForm(forms.ModelForm):
	helper = FormHelper()
	
	class Meta:
		model = Ontology
		fields = [
			"prompt_set",
			"prompt_set_percent",
			
		]

		labels = {
            'prompt_set': ('Prompt Set'),
            'prompt_set_percent': ('Prompt Percent'),
        }

	def __init__(self, *args, **kwargs):
		super(EmotionOntologyForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'id-form'
		self.helper.form_class = 'form-inline'
		self.fields['prompt_set'].widget.attrs['placeholder'] = 'New Set'
		

class EmotionOntologyFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(EmotionOntologyFormSetHelper, self).__init__(*args, **kwargs)
        self.form_method = 'post'
        self.render_required_fields = True
        self.label_class = 'col-lg-4'
        self.field_class = 'col-lg-8'
        self.add_input(Submit('submit_onotoloy', 'Submit'))



class UserSettingForm_PromptRate(forms.ModelForm):
	#These are declared here to get the choice field
	class Meta:
		model = ExperienceSetting

		fields = [
			"prompts_per_week",	
		]

		labels = {
            'prompts_per_week': ('Number of texts per week'),   
        }

		help_texts = {
        	'prompts_per_week': (''),
        	
        }

	def __init__(self, *args, **kwargs):
		super(UserSettingForm_PromptRate, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.render_required_fields = True
		self.helper.label_class = 'col-lg-6'
		self.helper.field_class = 'col-lg-6'
		self.helper.form_class = 'form-horizontal'
		
		self.helper.add_input(Submit('submit_prompt_percent', 'Submit'))
		

#Main form used to set the user settings
class TimingForm(forms.ModelForm):
	#These are declared here to get the choice field
	class Meta:
		model = UserSetting

		fields = [
			"sleep_time",
			"sleep_duration",
			"prompts_per_week",
		]

		labels = {
            'sleep_time': ('Bed Time'),
            'sleep_duration': ('Time Asleep (Hours)'),
            'prompts_per_week': ('Average number of texts per week'),
        }

		help_texts = {
        	'sleep_time': (''),
        	'sleep_duration': (''),

        }

	def __init__(self, *args, **kwargs):
		super(TimingForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'id-form'
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-lg-4'
		self.helper.field_class = 'col-lg-8'
		self.helper.form_method = 'post'
		self.helper.form_action = 'login'
		self.helper.add_input(Submit('submit_timing', 'Submit'))		

#Main form used to set the user settings
class UserSettingForm_Prompt(forms.ModelForm):
	#These are declared here to get the choice field
	timezone = forms.ChoiceField(choices=[(x, x) for x in pytz.country_timezones['us']],label="Timezone")
	carrier = forms.ChoiceField(choices=[(x, x) for x in Carrier.objects.all()],label="Carrier")
	

	class Meta:
		model = UserSetting

		fields = [
			"phone",
			"carrier",
			"timezone",
		]

		labels = {
        }

		help_texts = {
			'phone': (''),
        }

	def __init__(self, *args, **kwargs):
		super(UserSettingForm_Prompt, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'id-form'
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-lg-4'
		self.helper.field_class = 'col-lg-8'
		self.helper.form_method = 'post'
		self.helper.form_action = 'login'
		self.helper.add_input(Submit('submit_contact', 'Submit'))



