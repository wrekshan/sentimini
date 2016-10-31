from django import forms
from django.forms import widgets, Select, RadioSelect
from django.contrib.admin import widgets     
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Submit, Layout, Div, Field, Fieldset, MultiField
import pytz
from datetimewidget.widgets import DateTimeWidget, DateWidget, TimeWidget

from .models import Carrier, ActualTextSTM, UserSetting, Ontology, PossibleTextSTM, ResponseTypeStore, UserGenPromptFixed, FeedSetting, GroupSetting

#This allows the user to input their own prompts.  Because this is a model set, I don't know how to use the help_texts/labels.  

class GroupPasscode_Form(forms.ModelForm):
	helper = FormHelper()
	
	class Meta:
		model = GroupSetting
		fields = [
			"passcode",
		]

		labels = {
            
        }

	def __init__(self, *args, **kwargs):
		super(GroupPasscode_Form, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		# self.helper.label_class = 'col-lg-4'
		# self.helper.field_class = 'col-lg-8'
		# self.helper.form_class = 'form-horizontal'
		# self.fields['description'].widget.attrs['placeholder'] = 'Want to describe this in any way?'
		# self.fields['number_of_texts_in_set'].widget.attrs['readonly'] = True
		self.helper.add_input(Submit('submit_group_passcode', 'Submit Group Passcode'))	



class AddNewGroup_Creator_Form(forms.ModelForm):
	helper = FormHelper()
	
	class Meta:
		model = GroupSetting
		fields = [
			"group_name",
			"description",
			"passcode",
			"viewable",
			"joinable",
			"editable",
		]

		labels = {
            
        }

	def __init__(self, *args, **kwargs):
		super(AddNewGroup_Creator_Form, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		# self.helper.label_class = 'col-lg-4'
		# self.helper.field_class = 'col-lg-8'
		# self.helper.form_class = 'form-horizontal'
		# self.fields['description'].widget.attrs['placeholder'] = 'Want to describe this in any way?'
		# self.fields['number_of_texts_in_set'].widget.attrs['readonly'] = True
		self.helper.add_input(Submit('submit_new_group', 'Submit Group Details'))	




class TextSetFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(TextSetFormSetHelper, self).__init__(*args, **kwargs)
        self.form_method = 'post'
        self.render_required_fields = True
        self.template = 'WR_table_inline_formset_help.html'
        self.label_class = 'col-lg-0'
        self.field_class = 'col-lg-12'
        self.add_input(Submit('submit_formset', 'Submit Text Edits'))
        self.form_class = 'form-horizontal'


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
		self.fields['text'].widget.attrs['placeholder'] = 'Add new text here (i.e."The world is beautiful and good")'


#Main form used to set the user settings
class ContactSettingsForm(forms.ModelForm):
	#These are declared here to get the choice field
	timezone = forms.ChoiceField(choices=[(x, x) for x in pytz.country_timezones['us']],label="Timezone")
	carrier = forms.ChoiceField(choices=[(x, x) for x in Carrier.objects.all()],label="Carrier")
	sleep_time = forms.DateTimeField(label='Bed Time',input_formats = ['%H:%M'], required = True, widget=TimeWidget(usel10n=False, bootstrap_version=3, options={'minuteStep': 15, 'startView': 1, 'showMeridian': True, 'clearBtn': False, 'format': 'hh:ii'}))
	wake_time = forms.DateTimeField(label='Wake Time',input_formats = ['%H:%M'], required = True, widget=TimeWidget(usel10n=False, bootstrap_version=3, options={'minuteStep': 15, 'startView': 1, 'showMeridian': True, 'clearBtn': False, 'format': 'hh:ii'}))

	class Meta:
		model = UserSetting

		fields = [
			"phone_input",
			"carrier",
			"timezone",
			"sleep_time",
			"wake_time",
			"send_text_check",
			"send_email_check",
		]

		labels = {
			'send_email_check': ('Send through email'),
            'send_text_check': ('Send through text'),
            'sleep_time': ('Bed Time'),
            'wake_time': ('Wake Time'),
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


class NewUserForm(forms.ModelForm):
	#These are declared here to get the choice field
	timezone = forms.ChoiceField(choices=[(x, x) for x in pytz.country_timezones['us']],label="Timezone")
	carrier = forms.ChoiceField(choices=[(x, x) for x in Carrier.objects.all()],label="Carrier")
	sleep_time = forms.DateTimeField(label='Bed Time',input_formats = ['%H:%M'], required = True, widget=TimeWidget(usel10n=False, bootstrap_version=3, options={'minuteStep': 15, 'startView': 1, 'showMeridian': True, 'clearBtn': False, 'format': 'hh:ii'}))
	wake_time = forms.DateTimeField(label='Wake Time',input_formats = ['%H:%M'], required = True, widget=TimeWidget(usel10n=False, bootstrap_version=3, options={'minuteStep': 15, 'startView': 1, 'showMeridian': True, 'clearBtn': False, 'format': 'hh:ii'}))
	

	class Meta:
		model = UserSetting

		fields = [
			"phone_input",
			"carrier",
			"timezone",
			"wake_time",
			"sleep_time",
			
		]

		labels = {
			'phone_input': ('Phone Number'),
			'sleep_time': ('Bed Time'),
			'sleep_duration': ('Hours of sleep'),
		
        }

		help_texts = {
				
        }

	def __init__(self, *args, **kwargs):
		super(NewUserForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'id-form'
		# self.helper.form_class = 'form-horizontal'
		# self.helper.label_class = 'col-lg-4'
		# self.helper.field_class = 'col-lg-8'
		self.helper.form_method = 'post'
		self.helper.form_action = 'login'
		self.fields['phone_input'].widget.attrs['placeholder'] = '(123) 456-7890'
		self.helper.add_input(Submit('submit_contact', 'Submit'))

class NewUser_PossibleTextSTMForm(forms.ModelForm):
	helper = FormHelper()
	
	response_type = forms.ChoiceField(label="How will you respond to this?",choices=[(x, x) for x in ResponseTypeStore.objects.all().order_by('ordering_num')])
	class Meta:
		model = PossibleTextSTM
		fields = [
			"text",
			"response_type",
			"text_importance",
		]

		labels = {
            'text': ('Text'),
            'response_type': ('How will you respond to this?'),
            'text_importance': ('How important is this?'),
        }

		help_texts = {
			'text_importance': ('0 (not important/infrequent) to 10 (very important/frequenty)'),
		}

	def __init__(self, *args, **kwargs):
		super(NewUser_PossibleTextSTMForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'id-form'
		self.helper.form_method = 'post'
		# self.helper.label_class = 'col-lg-4'
		# self.helper.field_class = 'col-lg-8'
		self.helper.form_action = 'login'		
		self.fields['text'].widget.attrs['placeholder'] = 'Add new text here (i.e."The world is beautiful and good")'
		self.helper.add_input(Submit('submit_new_text', 'Submit text'))
		

class AddNewTextSetForm_full(forms.ModelForm):
	helper = FormHelper()
	
	class Meta:
		model = FeedSetting
		fields = [
			"feed_name",
			"texts_per_week",
		]

		labels = {
            'feed_name': ('Text Set Name'),
            'description': ('Description'),
            'texts_per_week': ('Texts per Week'),
        }

	def __init__(self, *args, **kwargs):
		super(AddNewTextSetForm_full, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		
		# self.helper.label_class = 'col-lg-4'
		# self.helper.field_class = 'col-lg-8'
		# self.helper.form_class = 'form-horizontal'
		self.fields['feed_name'].widget.attrs['placeholder'] = 'Mindfulness or Dream or Something'
		# self.fields['description'].widget.attrs['placeholder'] = 'Want to describe this in any way?'
		# self.fields['number_of_texts_in_set'].widget.attrs['readonly'] = True
		self.helper.add_input(Submit('submit_feed_description', 'Submit Feed Descriptions'))	


class AddNewTextSetForm_fullFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(AddNewTextSetForm_fullFormSetHelper, self).__init__(*args, **kwargs)
        self.form_method = 'post'
        self.render_required_fields = True
        self.template = 'feed_name_table_inline_formset.html'
        self.label_class = 'col-lg-0'
        self.field_class = 'col-lg-12'
        self.add_input(Submit('submit_new_feed_name', 'Add new text set'))
        self.form_class = 'form-horizontal'


class ExperienceTimingForm(forms.ModelForm):
	#These are declared here to get the choice field
	class Meta:
		model = FeedSetting

		fields = [
			"texts_per_week",	
		]

		labels = {
            'texts_per_week': ('Number of Texts Per Week'),   
        }

		help_texts = {
        	'texts_per_week': (''),
        	
        }

	def __init__(self, *args, **kwargs):
		super(ExperienceTimingForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.render_required_fields = True
		self.helper.label_class = 'col-lg-5'
		self.helper.field_class = 'col-lg-7'
		self.helper.form_class = 'form-horizontal'
		self.helper.add_input(Submit('submit_prompt_percent', 'Submit'))
		
class KT_PossibleTextSTMForm(forms.ModelForm):
	helper = FormHelper()
	
	response_type = forms.ChoiceField(label="How will you respond to this?",choices=[(x, x) for x in ResponseTypeStore.objects.all().order_by('ordering_num')])
	class Meta:
		model = PossibleTextSTM
		fields = [
			"text",
			"response_type",
		]

		labels = {
            'text': ('Text'),
            'response_type': ('How will you respond to this?'),

        }

		help_texts = {
			'text_importance': ('0 (not important/infrequent) to 10 (very important/frequenty)'),
		}

	def __init__(self, *args, **kwargs):
		super(KT_PossibleTextSTMForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'id-form'
		self.helper.form_method = 'post'
		# self.helper.label_class = 'col-lg-4'
		# self.helper.field_class = 'col-lg-8'
		self.helper.form_action = 'login'		
		self.fields['text'].widget.attrs['placeholder'] = 'Add new text here (i.e."The world is beautiful and good")'
		self.helper.add_input(Submit('submit_new_text', 'Submit text'))\


###### OLD BUT INTERESTING
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
		self.fields['prompt'].widget.attrs['placeholder'] = 'Add new text here (i.e."The world is beautiful and good")'
