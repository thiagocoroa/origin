from django.core import mail
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


class SubscribePostTest(TestCase):

	def setUp(self):
		data = dict(name='Henrique Bastos', cpf='12345678901',
			email='henrique@bastos.net', phone='21-99618-6180')
		self.response = self.client.post('/inscricao/', data)
	
	def test_post(self):
		'''o post deve redirecionar para /inscricao/'''
		self.assertEqual(302, self.response.status_code)

	def test_send_subscribe_email(self):
		self.assertEqual(1,len(mail.outbox))

	def test_subscription_email_subject(self):
		email = mail.outbox[0]
		expect = 'Confirmação de inscrição'

		self.assertEqual(expect, email.subject)
	def test_subscription_email_from(self):
		email = mail.outbox[0]
		expect = 'contato@eventex.com.br'

		self.assertEqual(expect, email.from_email)

	def test_subscription_email_to(self):
		email = mail.outbox[0]
		expect = ['contato@eventex.com.br', 'henrique@bastos.net']

		self.assertEqual(expect, email.to)

	def test_subscription_email_body(self):
		email = mail.outbox[0]

		self.assertIn('Henrique Bastos', email.body)
		self.assertIn('12345678901', email.body)
		self.assertIn('henrique@bastos.net', email.body)
		self.assertIn('21-99618-6180', email.body)

class SubscbribeInvalidPost(TestCase):
	"""POST inválido não deve redirecionar"""
	def setUp(self):
		self.response = self.client.post('/inscricao/', {})

	def test_post(self):
		self.assertEqual(200, self.response.status_code)

	def test_template(self):
		self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')

	def test_has_form(self):
		form = self.response.context['form']
		self.assertIsInstance(form, SubscriptionForm)

	def test_form_has_errors(self):
		form = self.response.context['form']
		self.assertTrue(form.errors)

class SubscribeSuccessMessage(TestCase):
	"""docstring for SubscribeSuccessMessage"""
	def test_message(self):
		data = dict(name='Henrique Bastos', cpf='12345678901',
			email='henrique@bastos.net', phone='21-99618-6180')	

		response = self.client.post('/inscricao/',data , follow=True)
		self.assertContains(response, 'Inscrição realizada com Sucesso!')