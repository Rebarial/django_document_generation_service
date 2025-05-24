from documents_сreating.tools.work_with_excel import models_dict
from django.http import HttpResponse
import urllib.parse
from documents_сreating.forms import OrganizationForm, BankDetailsOrganizationForm
from documents_сreating.models import Organization, BankDetails, Status, StatusOrganization
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render
from dotenv import load_dotenv
from django.contrib.auth.decorators import login_required
import os
from django.http import JsonResponse
import requests

def main(request):
    return render(request, 'main.html')

def add_organization(request):
    if request.method == 'POST':

        prefix = request.POST.get('modal-prefix', None)
        existing_org_id = request.POST.get(f'org_id', None)
        if prefix:
            if existing_org_id:
                organization = Organization.objects.get(id=existing_org_id)
                org_form = OrganizationForm(request.POST, request.FILES, instance=organization, prefix=prefix)
            else:
                org_form = OrganizationForm(request.POST, request.FILES, prefix=prefix)

            if org_form.is_valid():

                organization = org_form.save(commit=False)
                organization.user = request.user
                organization.save()

                StatusOrganization.objects.filter(organization=organization).delete()
                selected_statuses = org_form.cleaned_data['statuses']
                for status in selected_statuses:
                    status_org_obj = StatusOrganization(organization=organization, status=status)
                    status_org_obj.save()

                status_ids = list(selected_statuses.values_list('id', flat=True))

                return JsonResponse(
                    {
                        'name': organization.name,
                        'inn': organization.inn,
                        'id': organization.id,
                        'statuses': status_ids
                    }
                )
            else:
                print("Form errors:", org_form.errors)
                errors = org_form.errors.as_json()
                return JsonResponse({'errors': errors})
        else:
            return JsonResponse({'errors': "Действие не поддерживается"})


def add_bank_organization(request):
    if request.method == 'POST':
        prefix = request.POST.get('modal-prefix', None)
        print(request.POST)

        existing_org_id = request.POST.get('org', None)
        existing_bank_id = request.POST.get('bank', None)
        print(existing_org_id)
        print(prefix)

        if prefix:
            if existing_bank_id:
                bank = BankDetails.objects.get(id=existing_bank_id)
                bank_form = BankDetailsOrganizationForm(request.POST, request.FILES, instance=bank, prefix=prefix)
            else:
                bank_form = BankDetailsOrganizationForm(request.POST, request.FILES, prefix=prefix)

            if bank_form.is_valid():
                
                

                bank = bank_form.save(commit=False)
                if existing_org_id:
                    organization = Organization.objects.get(id=existing_org_id)
                    bank.organization = organization
                bank.save()

                return JsonResponse(
                    {
                        'name': bank.name,
                        'id': bank.id,
                    }
                )
            else:
                errors = bank_form.errors.as_json()
                return JsonResponse({'errors': errors})
        else:
            return JsonResponse({'errors': "Действие не поддерживается"})
      

def fetch_organization_data(request):
    """ Возвращает данные организации по переданному ID. """
    if request.method == 'GET':
        org_id = request.GET.get('org_id')
        try:
            # Ищем организацию по переданному ID
            print(org_id)
            organization = get_object_or_404(Organization, pk=org_id)
            status_ids = list(StatusOrganization.objects.filter(organization=organization).values_list('status_id', flat=True))
            print(status_ids)
            # Получаем привязанные банковские реквизиты
            #bank_details = BankDetails.objects.filter(organization=organization).first()

            # Формируем словарь с данными организации
            print(request.build_absolute_uri(organization.stamp.url) if organization.stamp else None)
            data = {
                'name': organization.name,
                'inn': organization.inn,
                'kpp': organization.kpp,
                'is_ip': organization.is_ip,
                'ogrn': organization.ogrn,
                'address': organization.address,
                'telephone': organization.telephone,
                'fax': organization.fax,
                'director_name': organization.director_name,
                'director_position': organization.director_position,
                'accountant_name': organization.accountant_name,
                'conventional_name': organization.conventional_name,
                'statuses': status_ids,
                'stamp_url': organization.stamp.url if organization.stamp else None,
                'signature_url': organization.signature.url if organization.signature else None,
                'id': organization.id,
            }
            print(data)
            return JsonResponse(data)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({"error": "Метод не поддерживается"}, status=405)


def fetch_organization_bank_data(request):
    """ Возвращает данные банка организации по переданному ID. """
    if request.method == 'GET':
        bank_id = request.GET.get('bank_id')
        print(bank_id)
        try:
            bank = get_object_or_404(BankDetails, pk=bank_id)
            print(bank)
            data = {
                'name': bank.name,
                'bic': bank.bic,
                'address': bank.address,
                'correspondent_account': bank.correspondent_account,
                'current_account': bank.current_account,
                'id': bank.id,
            }
            print(data)
            return JsonResponse(data)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({"error": "Метод не поддерживается"}, status=405)
    

def fetch_bank_from_organization(request):
    if request.method == 'GET':
        org_id = request.GET.get('org_id')
        try:
            banks = BankDetails.objects.filter(organization__id=org_id).values('id', 'name')
            list_result = [entry for entry in banks]
            print(banks)
            print(list_result)
            data = {
                'banks': list_result
                }
            print(data)
            return JsonResponse(data)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({"error": "Метод не поддерживается"}, status=405)
    

DADATA_API_KEY = os.getenv("DADATA_API_KEY")

def find_company_by_inn(request):

    inn = request.GET.get("inn")

    url = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/findById/party"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Token {DADATA_API_KEY}"
    }
    data = {"query": inn}

    try:
        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            result = response.json()
            if result["suggestions"]:
                company_info = result["suggestions"][0]["data"]
                if company_info["opf"]["short"] not in 'ИП':
                    name_company = result["suggestions"][0]["value"]
                    address = company_info.get("address", {}).get("value", "")
                    position_at_work = company_info.get("management", {}).get("post", "")
                    supervisor = company_info.get("management", {}).get("name", "")
                    return JsonResponse({
                                    "success": True,
                                    "type": "Юридическое лицо",
                                    "name": name_company,
                                    "kpp": company_info.get("kpp", ""),
                                    "ogrn": company_info.get("ogrn", ""),
                                    "address": address,
                                    "position_at_work": position_at_work,
                                    "supervisor": supervisor,
                                })
                elif company_info["opf"]["short"] == "ИП":
                    name_company = result["suggestions"][0]["value"]
                    address = company_info["address"].get("value", "")
                    return JsonResponse({
                                    "success": True,
                                    "type": "Индивидуальный предприниматель",
                                    "name": name_company,
                                    "ogrn": company_info.get("ogrn", ""),
                                    "address": address,
                                })

    except requests.RequestException as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


def find_bank_by_bic(request):
    bic = request.GET.get("bic")
    if not bic:
        return JsonResponse({"success": False, "error": "БИК не указан"}, status=400)

    url = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/findById/bank"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Token {DADATA_API_KEY}"
    }
    data = {"query": bic}
    try:
        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            result = response.json()
            if result["suggestions"]:
                bank_info = result["suggestions"][0]["data"]
                return JsonResponse({
                    "success": True,
                    "bank_name": bank_info.get("name", {}).get("payment", ""),
                    "address": bank_info.get("address", {}).get("value", ""),
                    "correspondent_account": bank_info.get("correspondent_account", ""),

                })
            else:
                return JsonResponse({"success": False, "error": "Банк не найден"}, status=404)
        else:
            return JsonResponse({"success": False, "error": "Ошибка Dadata API"}, status=response.status_code)

    except requests.RequestException as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


def inn_autocomplete(request):
    query = request.GET.get('query', '').strip()

    if len(query) < 3:
        return JsonResponse({"suggestions": []})

    url = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/party"
    headers = {
        "Authorization": f"Token {DADATA_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "query": query,
        "count": 5,
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        results = response.json().get("suggestions", [])
        suggestions = [{"value": item["value"], "inn": item["data"]["inn"]} for item in results if item["data"]["state"]["status"] == 'ACTIVE']
        return JsonResponse({"suggestions": suggestions})

    return JsonResponse({"suggestions": []})


def bank_autocomplete(request):
    query = request.GET.get('query', '').strip()

    if len(query) < 3:
        return JsonResponse({"suggestions": []})

    url = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/bank"
    headers = {
        "Authorization": f"Token {DADATA_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "query": query,
        "count": 5,
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        results = response.json().get("suggestions", [])
        suggestions = [{"value": item["value"], "bic": item["data"]["bic"]} for item in results]
        return JsonResponse({"suggestions": suggestions})

    return JsonResponse({"suggestions": []})


def create_pdf(doc_name, doc):
    print(doc_name, doc)
    print(models_dict[doc_name]['engine'])
    pdf_document = models_dict[doc_name]['engine'].create_pdf_document(doc, None)
    response = HttpResponse(pdf_document.read(), content_type='application/pdf')
    filename = urllib.parse.quote(f'Счет на оплату №{doc.number} от {doc.date}.pdf', safe='')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response

def create_excel(doc_name, doc):
    excel_document = models_dict[doc_name]['engine'].create_excel_document(doc, None)
    response = HttpResponse(excel_document.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    filename = urllib.parse.quote(f'Счет на оплату №{doc.number} от {doc.date}.xlsx', safe='')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response

def download_pdf(request, doc_name, doc_id):
    if doc_id:
        document = models_dict[doc_name]['model'].objects.get(id = doc_id)
        return create_pdf(doc_name=doc_name, doc=document)
    
def download_excel(request, doc_name, doc_id):
    if doc_id:
        document = models_dict[doc_name]['model'].objects.get(id = doc_id)
        return create_excel(doc_name=doc_name, doc=document)
    
@login_required
def edit_organization(request, id_org):
    organization = Organization.objects.get(id=id_org)
    bank_details = BankDetails.objects.filter(organization=organization).first()

    if request.method == 'POST':
        org_form = OrganizationForm(request.POST, request.FILES, instance=organization, prefix='organization')
        bank_form = BankDetailsOrganizationForm(request.POST, instance=bank_details, prefix='bank')

        if org_form.is_valid():
            organization = org_form.save(commit=False)
            organization.user = request.user
            organization.save()

            if any(bank_form.data.get('bank-' + field) for field in bank_form.fields):
                for field in bank_form.fields.values():
                    field.required = True
                if bank_form.is_valid():
                    bank_details_edit = bank_form.save(commit=False)
                    bank_details_edit.organization = organization
                    bank_details_edit.save()
                else:
                    return render(request, 'add_organization_new.html', {
                        'org_form': org_form,
                        'bank_form': bank_form
                    })

            return redirect('profile')

    else:
        org_form = OrganizationForm(instance=organization, prefix='organization')
        bank_form = BankDetailsOrganizationForm(instance=bank_details, prefix='bank')

    return render(request, 'add_organization_new.html', {
        'org_form': org_form,
        'bank_form': bank_form,
    })

def search_counterparty(request):
    query = request.GET.get('q', '')
    if query:
        buyer_status = Status.objects.filter(name="Buyer").first()
        results = Organization.objects.filter(
            name__icontains=query,
            status_org__status=buyer_status
        ) | Organization.objects.filter(
            inn__icontains=query,
            status_org__status=buyer_status
        )
        data = [{
            'id': c.id,
            'naming': c.name,
            'inn': c.inn
        } for c in results]
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)

def inn_autocomplete(request):
    query = request.GET.get('query', '').strip()

    if len(query) < 3:
        return JsonResponse({"suggestions": []})

    url = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/party"
    headers = {
        "Authorization": f"Token {DADATA_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "query": query,
        "count": 5,
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        results = response.json().get("suggestions", [])
        suggestions = [{"value": item["value"], "inn": item["data"]["inn"]} for item in results if item["data"]["state"]["status"] == 'ACTIVE']
        print(suggestions)
        return JsonResponse({"suggestions": suggestions})

    return JsonResponse({"suggestions": []})

def add_counterparty_from_profile(request):
    if request.method == 'POST':
        counterparty_form = OrganizationForm(request.POST, prefix='counterparty')
        counterparty_bank_form = BankDetailsOrganizationForm(request.POST, prefix='counterparty_bank')

        if counterparty_form.is_valid():
            organization = counterparty_form.save(commit=False)
            organization.user = request.user
            # organization.save()

            if any(counterparty_bank_form.data.get('counterparty_bank-' + field) for field in
                   counterparty_bank_form.fields):
                for field in counterparty_bank_form.fields.values():
                    field.required = True
                if counterparty_bank_form.is_valid():
                    organization.save()
                    bank_details = counterparty_bank_form.save(commit=False)
                    bank_details.organization = organization
                    bank_details.save()
                else:
                    return render(request, 'add_counterparty_new.html', {
                        'counterparty_form': counterparty_form,
                        'counterparty_bank_form': counterparty_bank_form
                    })

            organization.save()
            return redirect('profile')
    else:
        counterparty_form = OrganizationForm(initial={'statuses': [2]}, prefix='counterparty')
        counterparty_bank_form = BankDetailsOrganizationForm(prefix='counterparty_bank')

    return render(request, 'add_organization_new.html',
                  {'org_form': counterparty_form,
                   'bank_form': counterparty_bank_form})

def add_organization_from_profile(request):
    if request.method == 'POST':
        org_form = OrganizationForm(request.POST, request.FILES, prefix='organization')
        bank_form = BankDetailsOrganizationForm(request.POST, prefix='bank')
        org_form.statuses[1] = True
        if org_form.is_valid():
            organization = org_form.save(commit=False)
            organization.user = request.user
            organization.save()

            if any(bank_form.data.get('bank-' + field) for field in bank_form.fields):
                for field in bank_form.fields.values():
                    field.required = True
                if bank_form.is_valid():
                    bank_details = bank_form.save(commit=False)
                    bank_details.organization = organization
                    bank_details.save()
                else:
                    return render(request, 'add_organization_new.html', {
                        'org_form': org_form,
                        'bank_form': bank_form
                    })

            return redirect('profile')

    else:
        org_form = OrganizationForm(initial={'statuses': [1]}, prefix='organization')
        bank_form = BankDetailsOrganizationForm(prefix='bank')

    return render(request, 'add_organization_new.html', {
        'org_form': org_form,
        'bank_form': bank_form
    })

