from django import forms
from django.forms import widgets, Select, RadioSelect
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Submit
import pytz

from .models import FAQuserquestions

#This allows the user to input their own prompts.  Because this is a model set, I don't know how to use the help_texts/labels.  


#Main form used to set the user settings
class FAQuserquestionsForm(forms.ModelForm):
	
	class Meta:
		model = FAQuserquestions

		fields = [
			"question",
		]

		labels = {
            'question': ('Ask a question!'),
        }

		help_texts = {
			'question': (''),
        }

	def __init__(self, *args, **kwargs):
		super(FAQuserquestionsForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'id-form'
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-lg-3'
		self.helper.field_class = 'col-lg-9'
		self.helper.form_method = 'post'
		self.helper.form_action = 'login'
		# self.helper.add_input(Submit('submit', 'Submit'))




