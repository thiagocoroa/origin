from django.conf import settings
from django.core import mail
from eventex.subscriptions.models import Subscription
from django.contrib import messages 
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from eventex.subscriptions.forms import SubscriptionForm

def subscribe(request):
    if request.method == 'POST':
        return create(request)
    else:
        return new(request)

def create(request):
    form = SubscriptionForm(request.POST)

    if not form.is_valid():
        return render(request, 'subscriptions/subscription_form.html',
            {'form': form})
    #envia o email
    _send_mail('Confirmação de inscrição',
        settings.DEFAULT_FROM_EMAIL,
        form.cleaned_data['email'],
        'subscriptions/subscription_email.txt',
        form.cleaned_data)
    
    Subscription.objects.create(**form.cleaned_data)
    #mensagem de sucesso    
    messages.success(request, 'Inscrição realizada com Sucesso!')

    return HttpResponseRedirect('/inscricao/')
    
def new(request):
    return render(request, 'subscriptions/subscription_form.html',{'form':SubscriptionForm()})

def _send_mail(subject, from_, to, template_name, context):
    body = render_to_string(template_name, context)
    mail.send_mail(subject,body,from_,[from_, to])