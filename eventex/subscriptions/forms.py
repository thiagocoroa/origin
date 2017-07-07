from django import forms 
from django.core.exceptions import ValidationError



def validate_cpf(value):
	if not value.isdigit():
		raise ValidationError('CPF deve contar apenas com números', 'digits')
	if len(value)!=11:
		raise ValidationError('CPF deve conter 11 dígitos', 'length')


class SubscriptionForm(forms.Form):
	"""docstring for SubscriptionForm"""
	name=forms.CharField(label='Nome')
	cpf=forms.CharField(label='CPF', validators=[validate_cpf])
	email=forms.EmailField(label='Email', required=False)
	phone=forms.CharField(label='Telefone', required=False)

	def clean_name(self):

		name = self.cleaned_data['name']

		'''words = []
		for w in name.split():
			words.append(w.capitalize())'''

		words = [w.capitalize() for w in name.split()]
		return ' '.join(words)

	def clean(self):
		if not self.cleaned_data.get('email') and not self.cleaned_data.get('phone'):
			raise ValidationError('Informe seu telefone ou seu email.')
		return self.cleaned_data