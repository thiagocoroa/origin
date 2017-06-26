from django.core import mail
from django.test import TestCase
from django.shortcuts import resolve_url as r 
from eventex.subscriptions.models import Subscription
from eventex.subscriptions.forms import SubscriptionForm

class SubscriptionsNew(TestCase):

	def setUp(self):
		self.response=self.client.get(r('subscriptions:new'))
	def test_get(self):
		"""inscrição deve retornar o código 200"""
		self.assertEqual(200, self.response.status_code)
	
	def test_template(self):
		"""o template deve ser o subscriptions/subscription_form.html"""
		self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')
	def test_html(self):
		"""o HTML deve ter essas input tags"""
		tags = (('<form',1),
				('<input',6),
				('type="text"',3),
				('type="email"',1),
				('type="submit"',1))
		for text, count in tags:
			with self.subTest():
				self.assertContains(self.response, text, count)
	def test_csrf(self):
		"""testando se há o CSRF"""
		self.assertContains(self.response,'csrfmiddlewaretoken')
	def test_has_form(self):
		form=self.response.context['form']
		self.assertIsInstance(form,SubscriptionForm)
	


class SubscriptionsNewPostValid(TestCase):

	def setUp(self):
		data = dict(name='Henrique Bastos', cpf='12345678901',
			email='henrique@bastos.net', phone='21-99618-6180')
		self.response = self.client.post(r('subscriptions:new'), data)
	
	def test_post(self):
		'''o post deve redirecionar para /inscricao/1/'''
		self.assertRedirects(self.response, r('subscriptions:detail', 1))

	def test_send_subscribe_email(self):
		self.assertEqual(1,len(mail.outbox))

	def test_save_subscription(self):
		self.assertTrue(Subscription.objects.exists())

class SubscriptionsNewPostInvalid(TestCase):
	"""POST inválido não deve redirecionar"""

	def setUp(self):
		self.response = self.client.post(r('subscriptions:new'), {})

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
	
	def test_dont_save_subscription(self):
		self.assertFalse(Subscription.objects.exists())
