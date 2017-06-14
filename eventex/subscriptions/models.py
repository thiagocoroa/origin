from django.db import models


class Subscription(models.Model):
	"""docstring for Subscription"""
	name = models.CharField(max_length=100)
	cpf = models.CharField(max_length=11)
	email = models.EmailField()
	phone = models.CharField(max_length=20)
	created_at = models.DateTimeField(auto_now=True)