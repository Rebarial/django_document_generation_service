from django.shortcuts import render, redirect
from users.forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import requests

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


def find_company_by_inn(request):
    # inn = request.GET.get("inn")
    # if not inn:
    #     return JsonResponse({"success": False, "error": "ИНН не указан"}, status=400)
    #
    # fns_url = f"https://api-fns.ru/api/egr?req={inn}&key=0e1ed851511ec34bdc069ef66f1278e6495d646a"
    # response = requests.get(fns_url)
    #
    # if response.status_code == 200:
    #     data = response.json()
    #     if "items" in data:
    #         company_data = data["items"][0]
    #
    #         if "ЮЛ" in company_data:
    #             company = company_data["ЮЛ"]
    #             return JsonResponse({
    #                 "success": True,
    #                 "type": "Юридическое лицо",
    #                 "name": company.get("НаимСокрЮЛ", ""),
    #                 "kpp": company.get("КПП", ""),
    #                 "ogrn": company.get("ОГРН", ""),
    #                 "address": company.get("Адрес", {}).get("АдресПолн", ""),
    #                 "position_at_work": company.get("Руководитель", {}).get("Должн", ""),
    #                 "supervisor": company.get("Руководитель", {}).get("ФИОПолн", ""),
    #             })
    #
    #         elif "ИП" in company_data:
    #             company = company_data["ИП"]
    #             address = company.get("Адрес", "")
    #             if address:
    #                 address_all = address.get("АдресПолн", "")
    #             else:
    #                 address_all = address
    #             return JsonResponse({
    #                 "success": True,
    #                 "type": "Индивидуальный предприниматель",
    #                 "name": company.get("ФИОПолн", ""),
    #                 "ogrn": company.get("ОГРНИП", ""),
    #                 "address": address_all,
    #             })
    #
    # return JsonResponse({"success": False, "error": "Компания или ИП не найдены"}, status=404)

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


DADATA_API_KEY = "475fea08958c183ae5a7c24d8cb50a7957ce98bc"


def find_bank_by_bik(request):
    bik = request.GET.get("bik")
    if not bik:
        return JsonResponse({"success": False, "error": "БИК не указан"}, status=400)

    url = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/findById/bank"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Token {DADATA_API_KEY}"
    }
    data = {"query": bik}

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
        suggestions = [{"value": item["value"], "inn": item["data"]["bic"]} for item in results]
        return JsonResponse({"suggestions": suggestions})

    return JsonResponse({"suggestions": []})