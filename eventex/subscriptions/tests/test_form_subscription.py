from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm



class SubscriptionFormTest(TestCase):

	def test_form_has_fields(self):
		'''form tem que ter 4 campos'''
		form = SubscriptionForm()
		expected =['name','cpf','email','phone']
		self.assertSequenceEqual(expected,list(form.fields))

	def test_cpf_is_digit(self):
		data = dict(name = 'Henrique Bastos', cpf = 'abcd5678901',
					email = 'henrique@bastos.net', phone = '21-996186180')
		form = SubscriptionForm(data)
		form.is_valid()
	
		self.assertFormErrorCode(form, 'cpf', 'digits')

	def test_cpf_is_11_digits(self):
		form = self.make_validated_form(cpf='1234')
		self.assertFormErrorCode(form, 'cpf', 'length')

	def assertFormErrorCode(self, form, field, code):
		errors = form.errors.as_data()
		errors_list = errors[field]
		exception = errors_list[0]
		self.assertEqual(code, exception.code)

	def assertFormErrorMsg(self, form, field, msg):
		
		errors = form.errors
		errors_list = errors[field]
		self.assertListEqual([msg], errors_list)

	def make_validated_form(self,**kwargs):
		valid = dict(name = 'Henrique Bastos', cpf = '12345678901',
			email = 'henrique@bastos.net', phone = '21-996186180')
		data = dict(valid, **kwargs)
		form = SubscriptionForm(data)
		form.is_valid()
		return form