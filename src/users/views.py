from django.shortcuts import render, redirect
from users.forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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
    #for doc in InvoiceDocument.objects.all():
    #    all_documents.append({'type': 'Счет', 'instance': doc})

    #for doc in UtdDocument.objects.all():
    #    all_documents.append({'type': 'УПД', 'instance': doc})

    #for doc in VatInvoiceDocument.objects.all():
    #    all_documents.append({'type': 'Счет-фактура', 'instance': doc})

    for doc in all_documents:
        documents_by_category.setdefault(doc['type'], []).append(doc['instance'])

    #counterparties = Buyer.objects.filter(user=request.user)
    #organizations = InformationOrganization.objects.filter(user=request.user)
    return render(request, 'profile_new.html',
                  {
    #                  'organizations': organizations,
     #                 'counterparties': counterparties,
                      'documents_by_category': documents_by_category
                  }
                  )
