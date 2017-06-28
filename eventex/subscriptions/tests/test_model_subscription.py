from datetime import datetime
from django.test import TestCase 
from eventex.subscriptions.models import Subscription

class SubscriptionModelTest(TestCase):
	"""docstring for SubscriptionModelTest"""
	def setUp(self):
		self.obj = Subscription(
			name='Henrique Bastos',
			cpf='12345678901',
			email='henrique@bastos.net',
			phone='21-99686180',)
		self.obj.save()

	def test_create(self):
		self.assertTrue(Subscription.objects.exists())

	def test_created_at(self):
		self.assertIsInstance(self.obj.created_at, datetime)

	def test_str(self):
		self.assertEqual('Henrique Bastos', str(self.obj))

	def test_paid_false(self):
		self.assertEqual(False, self.obj.paid)