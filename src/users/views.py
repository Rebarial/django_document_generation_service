from django.shortcuts import render, redirect
from users.forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import requests
from documents_сreating.models.documents.invoice_for_payment import DocumentInvoiceForPayment
from documents_сreating.models.organization import Organization, Status

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались!')
            return redirect('/')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы.')
    return redirect('login')


@login_required
def profile(request):
    documents_by_category = {}

    all_documents = []
    for doc in DocumentInvoiceForPayment.objects.all():
        all_documents.append({
            'type': 'Счет', 
            'instance': doc,
            'url_edit': 'invoice_edit',
            'url_add': 'invoice'
            })

    #for doc in UtdDocument.objects.all():
    #    all_documents.append({'type': 'УПД', 'instance': doc})

    #for doc in VatInvoiceDocument.objects.all():
    #    all_documents.append({'type': 'Счет-фактура', 'instance': doc})

    for doc in all_documents:
        category_type = doc['type']
        if category_type not in documents_by_category:
            documents_by_category[category_type] = {'url_add': doc['url_add'], 'url_edit': doc['url_edit'], 'elements': []}

        documents_by_category[category_type]['elements'].append(doc['instance'])


    seller_status = Status.objects.filter(name="Seller").first()

    buyer_status = Status.objects.filter(name="Buyer").first()

    counterparties = Organization.objects.filter(user=request.user, status_org__status=buyer_status)
    organizations = Organization.objects.filter(user=request.user, status_org__status=seller_status)
    return render(request, 'profile_new.html',
                  {
                    'organizations': organizations,
                    'counterparties': counterparties,
                    'documents_by_category': documents_by_category
                  }
                  )

