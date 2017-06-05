from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm

class SubscribeTest(TestCase):

	def setUp(self):

		self.response=self.client.get('/inscricao/')
	def test_get(self):
		"""inscrição deve retornar o código 200"""
		self.assertEqual(200, self.response.status_code)
	
	def test_template(self):
		"""o template deve ser o subscriptions/subscription_form.html"""
		self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')

	def test_html(self):
		"""o que deve ter no html"""
		self.assertContains(self.response,'<form')
		self.assertContains(self.response,'<input',6)
		self.assertContains(self.response,'type="text"',3)
		self.assertContains(self.response,'type="email"')
		self.assertContains(self.response,'type="submit"')

	def test_csrf(self):
		"""testando se há o CSRF"""
		self.assertContains(self.response,'csrfmiddlewaretoken')
	def test_has_form(self):
		form=self.response.context['form']
		self.assertIsInstance(form,SubscriptionForm)
	def test_form_has_fields(self):
		'''form tem que ter 4 campos'''
		form=self.response.context['form']
		self.assertSequenceEqual(['name','cpf','email','phone'],list(form.fields))