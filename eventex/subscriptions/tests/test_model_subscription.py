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
			phone='21-99686180')
		self.obj.save()

	def test_create(self):
		self.assertTrue(Subscription.objects.exists())

	def test_created_at(self):
		self.assertIsInstance(self.obj.created_at, datetime)

	