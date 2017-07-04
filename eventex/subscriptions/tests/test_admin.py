from django.test import TestCase
from eventex.subscriptions.admin import SubscriptionModelAdmin, Subscription, admin


class SubscriptionModelAdminTest(TestCase):
	"""docstring for SubscriptionModelAdmin"""
	def test_has_action(self):
		
		model_admin = SubscriptionModelAdmin(Subscription, admin.site)
		self.assertIn('mark_as_paid', model_admin.actions)

	def test_mark_all(self):
		Subscription.objects.create(name = 'Henrique Bastos', cpf='12345678901',
									email = 'henrique@bastos.net', phone = '21-996186180')
		queryset = Subscription.objects.all()
		model_admin=SubscriptionModelAdmin(Subscription,admin.site)
		model_admin.mark_as_paid(None, queryset)
		self.assertEqual(1,Subscription.objects.filter(paid=True).count())
