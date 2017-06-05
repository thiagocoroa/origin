from django import forms 

class SubscriptionForm(forms.Form):
	"""docstring for SubscriptionForm"""
	name=forms.CharField(label='Nome')
	cpf=forms.CharField(label='CPF')
	email=forms.EmailField(label='Email')
	phone=forms.CharField(label='Telefone')