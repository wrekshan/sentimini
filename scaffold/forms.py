# from django import forms
# from django.forms import widgets, Select, RadioSelect
# from crispy_forms.helper import FormHelper, Layout
# from crispy_forms.layout import Submit
# import pytz

# from .models import Business, Measure, Sentimini_help

# #This allows the user to input their own prompts.  Because this is a model set, I don't know how to use the help_texts/labels.  
# class Sentimini_helpFormSetHelper(FormHelper):
#     def __init__(self, *args, **kwargs):
#         super(Sentimini_helpFormSetHelper, self).__init__(*args, **kwargs)
#         self.form_method = 'post'
#         self.render_required_fields = True
#         # self.template = 'WR_table_inline_formset_UGP.html'
#         self.label_class = 'col-lg-0'
#         self.field_class = 'col-lg-12'
#         self.add_input(Submit('submit_help_formset', 'Submit'))
#         self.form_class = 'form-horizontal'


# #Main form used to set the user settings
# class Sentimini_helpForm(forms.ModelForm):

# 	class Meta:
# 		model = Sentimini_help
# 		fields = [
# 			"help_heading",
# 			"help_content",
# 			"help_type",
# 			"major_cat",
# 			"minor_cat",
# 			"level",
			

# 		]

# 		labels = {
# 			"help_heading": ('Heading'),
# 			"help_content": ('Content'),
# 			"help_type": ('Help Type'),
# 			"major_cat": ('Major Category'),
# 			"minor_cat": ('Minor Category'),
# 			"level": ('Level (if applicable)'),
			
#         }

# 		help_texts = {
		
#         }

# 	def __init__(self, *args, **kwargs):
# 		super(Sentimini_helpForm, self).__init__(*args, **kwargs)
# 		self.helper = FormHelper()
# 		self.helper.form_id = 'id-form'
# 		self.helper.form_class = 'form-horizontal'
# 		self.helper.label_class = 'col-lg-6'
# 		self.helper.field_class = 'col-lg-6'
# 		self.helper.form_method = 'post'
# 		self.helper.form_action = 'login'
# 		self.helper.add_input(Submit('submit_helpform', 'Submit'))

# #Main form used to set the user settings
# class MeasureForm(forms.ModelForm):

# 	class Meta:
# 		model = Measure
# 		fields = [
# 			"name",
# 			"measure",
# 			"super_measure",
# 			"measure_type",
# 			"population",
# 			"minval",
# 			"maxval",
# 			"mean",
# 			"sd",
# 			"distr",
# 			"response_rate",

# 		]

# 		labels = {
# 			"name": ('Name'),
# 			"measure": ('Measure'),
# 			"super_measure": ('Super Measure'),
# 			"measure_type": ('Type'),
# 			"population": ('Population'),
# 			"minval": ('Minimum'),
# 			"maxval": ('Maximum'),
# 			"mean": ('Mean'),
# 			"sd": ('Standard Deviation'),
# 			"distr": ('Distrobution Type'),
# 			"response_rate": ('Response Rate'),
#         }

# 		help_texts = {
		
#         }

# 	def __init__(self, *args, **kwargs):
# 		super(MeasureForm, self).__init__(*args, **kwargs)
# 		self.helper = FormHelper()
# 		self.helper.form_id = 'id-form'
# 		self.helper.form_class = 'form-horizontal'
# 		self.helper.label_class = 'col-lg-6'
# 		self.helper.field_class = 'col-lg-6'
# 		self.helper.form_method = 'post'
# 		self.helper.form_action = 'login'
# 		self.helper.add_input(Submit('submit_measure', 'Submit'))

# class BusinessForm_number_texts(forms.ModelForm):

# 	class Meta:
# 		model = Business
# 		fields = [
# 			"con_number_outgoing_per_free_per_day",
# 			"con_number_ingoing_per_free_per_day",
# 			"con_number_outgoing_per_paid_per_day",
# 			"con_number_ingoing_per_paid_per_day",
# 		]

# 		labels = {
# 			"con_number_outgoing_per_free_per_day": ('Num outgoing per free per day'),
# 			"con_number_ingoing_per_free_per_day": ('Num ingoing per free per day'),
# 			"con_number_outgoing_per_paid_per_day": ('Num outgoing per paid per day'),
# 			"con_number_ingoing_per_paid_per_day": ('Num ingoing per paid per day'),
#         }

# 		help_texts = {
			
#         }

# 	def __init__(self, *args, **kwargs):
# 		super(BusinessForm_number_texts, self).__init__(*args, **kwargs)
# 		self.helper = FormHelper()
# 		self.helper.form_id = 'id-form'
# 		self.helper.form_class = 'form-horizontal'
# 		self.helper.label_class = 'col-lg-9'
# 		self.helper.field_class = 'col-lg-3'
# 		self.helper.form_method = 'post'
# 		self.helper.form_action = 'login'
# 		self.helper.add_input(Submit('submit_number_texts_business', 'Submit'))

# class BusinessForm_price(forms.ModelForm):

# 	class Meta:
# 		model = Business
# 		fields = [
# 			"con_price_per_outgoing",
# 			"con_price_per_inccming",
# 		]

# 		labels = {
# 			"con_price_per_outgoing": ('Price per outgoing'),
# 			"con_price_per_inccming": ('Price per incoming'),
#         }

# 		help_texts = {
		
#         }

# 	def __init__(self, *args, **kwargs):
# 		super(BusinessForm_price, self).__init__(*args, **kwargs)
# 		self.helper = FormHelper()
# 		self.helper.form_id = 'id-form'
# 		self.helper.form_class = 'form-horizontal'
# 		self.helper.label_class = 'col-lg-9'
# 		self.helper.field_class = 'col-lg-3'
# 		self.helper.form_method = 'post'
# 		self.helper.form_action = 'login'
# 		self.helper.add_input(Submit('submit_price_business', 'Submit'))

# class BusinessForm_number_texts(forms.ModelForm):

# 	class Meta:
# 		model = Business
# 		fields = [
# 			"con_number_outgoing_per_free_per_day",
# 			"con_number_ingoing_per_free_per_day",
# 			"con_number_outgoing_per_paid_per_day",
# 			"con_number_ingoing_per_paid_per_day",
# 		]

# 		labels = {
# 			"con_number_outgoing_per_free_per_day": ('Num outgoing per free per day'),
# 			"con_number_ingoing_per_free_per_day": ('Num ingoing per free per day'),
# 			"con_number_outgoing_per_paid_per_day": ('Num outgoing per paid per day'),
# 			"con_number_ingoing_per_paid_per_day": ('Num ingoing per paid per day'),
#         }

# 		help_texts = {
			
#         }

# 	def __init__(self, *args, **kwargs):
# 		super(BusinessForm_number_texts, self).__init__(*args, **kwargs)
# 		self.helper = FormHelper()
# 		self.helper.form_id = 'id-form'
# 		self.helper.form_class = 'form-horizontal'
# 		self.helper.label_class = 'col-lg-9'
# 		self.helper.field_class = 'col-lg-3'
# 		self.helper.form_method = 'post'
# 		self.helper.form_action = 'login'
# 		self.helper.add_input(Submit('submit_number_texts_business', 'Submit'))

# class BusinessForm_user_stuff(forms.ModelForm):

# 	class Meta:
# 		model = Business
# 		fields = [
# 			"con_conversation_rate_to_paid",
# 			"con_return_per_paying_user_per_month",
# 		]

# 		labels = {
# 			"con_conversation_rate_to_paid": ('Conversation active user to paid user'),
# 			"con_return_per_paying_user_per_month": ('Return per user per month'),
#         }

# 		help_texts = {
			
#         }

# 	def __init__(self, *args, **kwargs):
# 		super(BusinessForm_user_stuff, self).__init__(*args, **kwargs)
# 		self.helper = FormHelper()
# 		self.helper.form_id = 'id-form'
# 		self.helper.form_class = 'form-horizontal'
# 		self.helper.label_class = 'col-lg-9'
# 		self.helper.field_class = 'col-lg-3'
# 		self.helper.form_method = 'post'
# 		self.helper.form_action = 'login'
# 		self.helper.add_input(Submit('submit_user_stuff_business', 'Submit'))

# class BusinessForm_static_costs(forms.ModelForm):

# 	class Meta:
# 		model = Business
# 		fields = [
# 			"static_human_cost_per_month",
# 			"static_server_cost_per_month",
# 			"static_other_cost_per_month",
# 		]

# 		labels = {
# 			"static_human_cost_per_month": ('Human cost per month'),
# 			"static_server_cost_per_month": ('Server cost per month'),
# 			"static_other_cost_per_month": ('Unforessen cost per month'),
#         }

# 		help_texts = {

			
			
#         }

# 	def __init__(self, *args, **kwargs):
# 		super(BusinessForm_static_costs, self).__init__(*args, **kwargs)
# 		self.helper = FormHelper()
# 		self.helper.form_id = 'id-form'
# 		self.helper.form_class = 'form-horizontal'
# 		self.helper.label_class = 'col-lg-9'
# 		self.helper.field_class = 'col-lg-3'
# 		self.helper.form_method = 'post'
# 		self.helper.form_action = 'login'
# 		self.helper.add_input(Submit('submit_static_costs_business', 'Submit'))

# class BusinessForm(forms.ModelForm):

# 	class Meta:
# 		model = Business
# 		fields = [
# 			"con_price_per_outgoing",
# 			"con_price_per_inccming",
# 			"con_number_outgoing_per_free_per_day",
# 			"con_number_ingoing_per_free_per_day",
# 			"con_number_outgoing_per_paid_per_day",
# 			"con_number_ingoing_per_paid_per_day",
# 			"con_conversation_rate_to_paid",
# 			"con_return_per_paying_user_per_month",
# 			"static_human_cost_per_month",
# 			"static_server_cost_per_month",
# 			"static_other_cost_per_month",
# 		]

# 		labels = {
# 			"con_price_per_outgoing": ('Price per outgoing'),
# 			"con_price_per_inccming": ('Price per incoming'),
# 			"con_number_outgoing_per_free_per_day": ('Num outgoing per free per day'),
# 			"con_number_ingoing_per_free_per_day": ('Num outgoing per free per day'),
# 			"con_number_outgoing_per_paid_per_day": ('Num ingoing per paid per day'),
# 			"con_number_ingoing_per_paid_per_day": ('Num ingoing per paid per day'),
# 			"con_conversation_rate_to_paid": ('Conversation active user to paid user'),
# 			"con_return_per_paying_user_per_month": ('Return per user per month'),
# 			"static_human_cost_per_month": ('Human cost per month'),
# 			"static_server_cost_per_month": ('Server cost per month'),
# 			"static_other_cost_per_month": ('Unforessen cost per month'),
#         }

# 		help_texts = {
# 			"con_price_per_outgoing": ('Plivio Price Assumed: .0035$'),
# 			"con_price_per_inccming": ('Plivio Price Assumed: .0000$'),
# 			"con_number_outgoing_per_free_per_day": ('Num outgoing per free per day'),
# 			"con_number_ingoing_per_free_per_day": ('Num outgoing per free per day'),
# 			"con_number_outgoing_per_paid_per_day": ('Num ingoing per paid per day'),
# 			"con_number_ingoing_per_paid_per_day": ('Num ingoing per paid per day'),
# 			"con_conversation_rate_to_paid": (''),
# 			"con_return_per_paying_user_per_month": (''),
# 			"static_human_cost_per_month": ('Human cost per month'),
# 			"static_server_cost_per_month": ('Server cost per month'),
# 			"static_other_cost_per_month": ('Unforessen cost per month'),
			
#         }

# 	def __init__(self, *args, **kwargs):
# 		super(BusinessForm, self).__init__(*args, **kwargs)
# 		self.helper = FormHelper()
# 		self.helper.form_id = 'id-form'
# 		self.helper.form_class = 'form-horizontal'
# 		self.helper.label_class = 'col-lg-10'
# 		self.helper.field_class = 'col-lg-2'
# 		self.helper.form_method = 'post'
# 		self.helper.form_action = 'login'
# 		self.helper.add_input(Submit('submit_business', 'Submit'))


