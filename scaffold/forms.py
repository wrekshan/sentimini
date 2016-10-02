from django import forms
from django.forms import widgets, Select, RadioSelect
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Submit
import pytz

from .models import FAQuserquestions, emotion_quotation, emotion_instruction, BETAsurvey, Business, Measure, Sentimini_help

#This allows the user to input their own prompts.  Because this is a model set, I don't know how to use the help_texts/labels.  
class Sentimini_helpFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(Sentimini_helpFormSetHelper, self).__init__(*args, **kwargs)
        self.form_method = 'post'
        self.render_required_fields = True
        # self.template = 'WR_table_inline_formset_UGP.html'
        self.label_class = 'col-lg-0'
        self.field_class = 'col-lg-12'
        self.add_input(Submit('submit_help_formset', 'Submit'))
        self.form_class = 'form-horizontal'


#Main form used to set the user settings
class Sentimini_helpForm(forms.ModelForm):

	class Meta:
		model = Sentimini_help
		fields = [
			"help_heading",
			"help_content",
			"help_type",
			"major_cat",
			"minor_cat",
			"level",
			

		]

		labels = {
			"help_heading": ('Heading'),
			"help_content": ('Content'),
			"help_type": ('Help Type'),
			"major_cat": ('Major Category'),
			"minor_cat": ('Minor Category'),
			"level": ('Level (if applicable)'),
			
        }

		help_texts = {
		
        }

	def __init__(self, *args, **kwargs):
		super(Sentimini_helpForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'id-form'
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-lg-6'
		self.helper.field_class = 'col-lg-6'
		self.helper.form_method = 'post'
		self.helper.form_action = 'login'
		self.helper.add_input(Submit('submit_helpform', 'Submit'))

#Main form used to set the user settings
class MeasureForm(forms.ModelForm):

	class Meta:
		model = Measure
		fields = [
			"name",
			"measure",
			"super_measure",
			"measure_type",
			"population",
			"minval",
			"maxval",
			"mean",
			"sd",
			"distr",
			"response_rate",

		]

		labels = {
			"name": ('Name'),
			"measure": ('Measure'),
			"super_measure": ('Super Measure'),
			"measure_type": ('Type'),
			"population": ('Population'),
			"minval": ('Minimum'),
			"maxval": ('Maximum'),
			"mean": ('Mean'),
			"sd": ('Standard Deviation'),
			"distr": ('Distrobution Type'),
			"response_rate": ('Response Rate'),
        }

		help_texts = {
		
        }

	def __init__(self, *args, **kwargs):
		super(MeasureForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'id-form'
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-lg-6'
		self.helper.field_class = 'col-lg-6'
		self.helper.form_method = 'post'
		self.helper.form_action = 'login'
		self.helper.add_input(Submit('submit_measure', 'Submit'))

class BusinessForm_number_texts(forms.ModelForm):

	class Meta:
		model = Business
		fields = [
			"con_number_outgoing_per_free_per_day",
			"con_number_ingoing_per_free_per_day",
			"con_number_outgoing_per_paid_per_day",
			"con_number_ingoing_per_paid_per_day",
		]

		labels = {
			"con_number_outgoing_per_free_per_day": ('Num outgoing per free per day'),
			"con_number_ingoing_per_free_per_day": ('Num ingoing per free per day'),
			"con_number_outgoing_per_paid_per_day": ('Num outgoing per paid per day'),
			"con_number_ingoing_per_paid_per_day": ('Num ingoing per paid per day'),
        }

		help_texts = {
			
        }

	def __init__(self, *args, **kwargs):
		super(BusinessForm_number_texts, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'id-form'
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-lg-9'
		self.helper.field_class = 'col-lg-3'
		self.helper.form_method = 'post'
		self.helper.form_action = 'login'
		self.helper.add_input(Submit('submit_number_texts_business', 'Submit'))

class BusinessForm_price(forms.ModelForm):

	class Meta:
		model = Business
		fields = [
			"con_price_per_outgoing",
			"con_price_per_inccming",
		]

		labels = {
			"con_price_per_outgoing": ('Price per outgoing'),
			"con_price_per_inccming": ('Price per incoming'),
        }

		help_texts = {
		
        }

	def __init__(self, *args, **kwargs):
		super(BusinessForm_price, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'id-form'
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-lg-9'
		self.helper.field_class = 'col-lg-3'
		self.helper.form_method = 'post'
		self.helper.form_action = 'login'
		self.helper.add_input(Submit('submit_price_business', 'Submit'))

class BusinessForm_number_texts(forms.ModelForm):

	class Meta:
		model = Business
		fields = [
			"con_number_outgoing_per_free_per_day",
			"con_number_ingoing_per_free_per_day",
			"con_number_outgoing_per_paid_per_day",
			"con_number_ingoing_per_paid_per_day",
		]

		labels = {
			"con_number_outgoing_per_free_per_day": ('Num outgoing per free per day'),
			"con_number_ingoing_per_free_per_day": ('Num ingoing per free per day'),
			"con_number_outgoing_per_paid_per_day": ('Num outgoing per paid per day'),
			"con_number_ingoing_per_paid_per_day": ('Num ingoing per paid per day'),
        }

		help_texts = {
			
        }

	def __init__(self, *args, **kwargs):
		super(BusinessForm_number_texts, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'id-form'
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-lg-9'
		self.helper.field_class = 'col-lg-3'
		self.helper.form_method = 'post'
		self.helper.form_action = 'login'
		self.helper.add_input(Submit('submit_number_texts_business', 'Submit'))

class BusinessForm_user_stuff(forms.ModelForm):

	class Meta:
		model = Business
		fields = [
			"con_conversation_rate_to_paid",
			"con_return_per_paying_user_per_month",
		]

		labels = {
			"con_conversation_rate_to_paid": ('Conversation active user to paid user'),
			"con_return_per_paying_user_per_month": ('Return per user per month'),
        }

		help_texts = {
			
        }

	def __init__(self, *args, **kwargs):
		super(BusinessForm_user_stuff, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'id-form'
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-lg-9'
		self.helper.field_class = 'col-lg-3'
		self.helper.form_method = 'post'
		self.helper.form_action = 'login'
		self.helper.add_input(Submit('submit_user_stuff_business', 'Submit'))

class BusinessForm_static_costs(forms.ModelForm):

	class Meta:
		model = Business
		fields = [
			"static_human_cost_per_month",
			"static_server_cost_per_month",
			"static_other_cost_per_month",
		]

		labels = {
			"static_human_cost_per_month": ('Human cost per month'),
			"static_server_cost_per_month": ('Server cost per month'),
			"static_other_cost_per_month": ('Unforessen cost per month'),
        }

		help_texts = {

			
			
        }

	def __init__(self, *args, **kwargs):
		super(BusinessForm_static_costs, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'id-form'
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-lg-9'
		self.helper.field_class = 'col-lg-3'
		self.helper.form_method = 'post'
		self.helper.form_action = 'login'
		self.helper.add_input(Submit('submit_static_costs_business', 'Submit'))

class BusinessForm(forms.ModelForm):

	class Meta:
		model = Business
		fields = [
			"con_price_per_outgoing",
			"con_price_per_inccming",
			"con_number_outgoing_per_free_per_day",
			"con_number_ingoing_per_free_per_day",
			"con_number_outgoing_per_paid_per_day",
			"con_number_ingoing_per_paid_per_day",
			"con_conversation_rate_to_paid",
			"con_return_per_paying_user_per_month",
			"static_human_cost_per_month",
			"static_server_cost_per_month",
			"static_other_cost_per_month",
		]

		labels = {
			"con_price_per_outgoing": ('Price per outgoing'),
			"con_price_per_inccming": ('Price per incoming'),
			"con_number_outgoing_per_free_per_day": ('Num outgoing per free per day'),
			"con_number_ingoing_per_free_per_day": ('Num outgoing per free per day'),
			"con_number_outgoing_per_paid_per_day": ('Num ingoing per paid per day'),
			"con_number_ingoing_per_paid_per_day": ('Num ingoing per paid per day'),
			"con_conversation_rate_to_paid": ('Conversation active user to paid user'),
			"con_return_per_paying_user_per_month": ('Return per user per month'),
			"static_human_cost_per_month": ('Human cost per month'),
			"static_server_cost_per_month": ('Server cost per month'),
			"static_other_cost_per_month": ('Unforessen cost per month'),
        }

		help_texts = {
			"con_price_per_outgoing": ('Plivio Price Assumed: .0035$'),
			"con_price_per_inccming": ('Plivio Price Assumed: .0000$'),
			"con_number_outgoing_per_free_per_day": ('Num outgoing per free per day'),
			"con_number_ingoing_per_free_per_day": ('Num outgoing per free per day'),
			"con_number_outgoing_per_paid_per_day": ('Num ingoing per paid per day'),
			"con_number_ingoing_per_paid_per_day": ('Num ingoing per paid per day'),
			"con_conversation_rate_to_paid": (''),
			"con_return_per_paying_user_per_month": (''),
			"static_human_cost_per_month": ('Human cost per month'),
			"static_server_cost_per_month": ('Server cost per month'),
			"static_other_cost_per_month": ('Unforessen cost per month'),
			
        }

	def __init__(self, *args, **kwargs):
		super(BusinessForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'id-form'
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-lg-10'
		self.helper.field_class = 'col-lg-2'
		self.helper.form_method = 'post'
		self.helper.form_action = 'login'
		self.helper.add_input(Submit('submit_business', 'Submit'))



class BETAsurveyForm(forms.ModelForm):

	class Meta:
		model = BETAsurvey
		fields = [
			"how_many_prompts",
			"text_topics",
			"how_many_prompts",
			"desired_dollars",
			"max_dollars",
			"new_features",
			"new_directions",
		]

		labels = {
            'how_many_prompts': ('How many texts are you willing to recieve per day?'),
            'text_topics': ('What would you like to recieve texts about?'),
            'desired_dollars': ('How much would you like to pay for this service?'),
            'max_dollars': ('How much would you be willing to pay for this service?'),
            'new_features': ('Are there any features that you would like to see?'),
            'new_directions': ('Are there any new directions you would like to see?'),

        }

		help_texts = {
			'how_many_prompts': (''),
        }

	def __init__(self, *args, **kwargs):
		super(BETAsurveyForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'id-form'
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-lg-6'
		self.helper.field_class = 'col-lg-6'
		self.helper.form_method = 'post'
		self.helper.form_action = 'login'
		self.helper.add_input(Submit('submit_BETA', 'Submit'))

#Main form used to set the user settings
class FAQuserquestionsForm(forms.ModelForm):
	
	class Meta:
		model = FAQuserquestions

		fields = [
			"question",
		]

		labels = {
            'question': (''),
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


class emotion_quotationForm(forms.ModelForm):
	class Meta:
		model = emotion_quotation

		fields = [
			"email",
			"emotion",
			"author",
			"quotation",
			
		]

		labels = {
            'email': ('What is your email?'),
			'emotion': ('What is the emotion?'),
            'quotation': ('What is the quotation?'),
            'author': ('Who is the author?'),
        }

		help_texts = {
			'email': (''),
			'emotion': (''),
            'quotation': (''),
            'author': (''),
        }

		

	def __init__(self, *args, **kwargs):
		super(emotion_quotationForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'id-form'
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-lg-3'
		self.helper.field_class = 'col-lg-9'
		self.helper.form_method = 'post'
		self.helper.form_action = 'login'

class emotion_instructionForm(forms.ModelForm):
	class Meta:
		model = emotion_instruction

		fields = [
			"email",
			"emotion",
			"why",
			"quotation",
			
		]

		labels = {
            'email': ('What is your email?'),
            'emotion': ('What is the emotion?'),
            'quotation': ('Describe this emotion to your 16 year old self.'),
            'why': ('Why did you choose this emotion?'),
        }

		help_texts = {
			'email': (''),
			'emotion': (''),
            'quotation': (''),
            'why': (''),
        }

		

	def __init__(self, *args, **kwargs):
		super(emotion_instructionForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'id-form'
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-lg-3'
		self.helper.field_class = 'col-lg-9'
		self.helper.form_method = 'post'
		self.helper.form_action = 'login'
		self.helper.add_input(Submit('form_emo_instructions', 'Submit'))

class emotion_quotationForm_sm(forms.ModelForm):
	class Meta:
		model = emotion_quotation

		fields = [
			"quotation",
			"author",
		]

		labels = {
            'quotation': ('What is quotation?'),
            'author': ('Who is the author?'),
        }

		help_texts = {
            'quotation': (''),
            'author': (''),
        }

		

	def __init__(self, *args, **kwargs):
		super(emotion_quotationForm_sm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'id-form'
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-lg-3'
		self.helper.field_class = 'col-lg-9'
		self.helper.form_method = 'post'
		self.helper.form_action = 'login'
		self.helper.add_input(Submit('form_emo_quotations', 'Submit'))

class emotion_instructionForm_sm(forms.ModelForm):
	class Meta:
		model = emotion_instruction

		fields = [

			"quotation",
			
		]

		labels = {
            'quotation': ('Describe this emotion to your 16 year old self.'),
        }

		help_texts = {
            'quotation': (''),
        }

		

	def __init__(self, *args, **kwargs):
		super(emotion_instructionForm_sm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'id-form'
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-lg-3'
		self.helper.field_class = 'col-lg-9'
		self.helper.form_method = 'post'
		self.helper.form_action = 'login'
		self.helper.add_input(Submit('form_emo_instructions', 'Submit'))

