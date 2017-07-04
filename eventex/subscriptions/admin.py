from django.contrib import admin
from eventex.subscriptions.models import Subscription
from django.utils.timezone import now

class SubscriptionModelAdmin(admin.ModelAdmin):
	"""docstring for SubscriptionModelAdmin"""
	list_display=('name','email','phone','cpf','created_at', 'subscribed_today','paid')
	date_hierarchy='created_at'	
	search_fields=('name','email','cpf','created_at')
	list_filter = ('paid','created_at',)
	actions = ['mark_as_paid']


	def subscribed_today(self,obj):
		return obj.created_at == now().date()
	subscribed_today.short_description = 'inscrito hoje'
	subscribed_today.boolean = True


	def mark_as_paid(self, request, queryset):
		queryset.update(paid=True)

	mark_as_paid.short_description='Marcar como pago'

admin.site.register(Subscription,SubscriptionModelAdmin)