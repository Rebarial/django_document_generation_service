from django.shortcuts import render

from django.db.models import Sum
from django.template.loader import render_to_string
from django.views.generic.edit import CreateView
from django.http import JsonResponse
from django.urls import reverse_lazy
from documents_сreating.models.documents.invoice_for_payment import DocumentInvoiceForPayment, InvoiceForPaymentItem
from .forms import InvoiceDocumentForm, InvoiceDocumentTableFormSet, OrganizationForm, BankDetailsOrganizationForm
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.utils.dateparse import parse_date
from documents_сreating.tools.work_with_excel.invoice_for_payment import invoice_for_payment_excel_document_create
from django.http import HttpResponse
from documents_сreating.models.organization import Organization, BankDetails, StatusOrganization, Status
from documents_сreating.models.reference import VatRate
from django.shortcuts import get_object_or_404
import json

def main(request):
    return render(request, 'main.html')


class InvoiceDocumentCreateView(LoginRequiredMixin, CreateView):
    model = DocumentInvoiceForPayment
    form_class = InvoiceDocumentForm
    template_name = 'invoice_document_form_new.html'
    #template_name = 'test.html'

    #success_url = reverse_lazy('invoices_list')
    success_url = reverse_lazy('main')

    def get_object(self, queryset=None):
        """Получение текущего объекта по переданному id_doc"""
        obj = None
        id_doc = self.kwargs.get('id_doc')
        if id_doc is not None:
            obj = get_object_or_404(DocumentInvoiceForPayment, pk=id_doc)
        return obj

    def get_initial(self):
        initial = super().get_initial()
        object = self.get_object()
        initial.update({
            'number': object.number,
            'date': object.date,
            'organization': object.organization.pk if object.organization else None,
            'organization_bank': object.organization_bank.pk if object.organization_bank else None,
            'buyer': object.buyer.pk if object.buyer else None,
            'buyer_bank': object.buyer_bank.pk if object.buyer_bank else None,
            'consignee': object.consignee.pk if object.consignee else None,
            'purpose_of_payment': object.purpose_of_payment,
            'payment_for': object.payment_for,
            'agreement': object.agreement,
            'vat_rate': object.vat_rate.pk if object.vat_rate else None,
            'printed_form': object.printed_form,
            'currency': object.currency.pk if object.currency else None,
            'discount': object.discount,
            'additional_info': object.additional_info,
            'is_stamp': object.is_stamp,
        })
        return initial

    vat_rate = VatRate.objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #seller_status = Status.objects.filter(name='Seller').first()
        context['org_form'] = OrganizationForm(prefix='seller')
        context['counterparty_form'] = OrganizationForm(prefix='buyer')
        context['consignee_form'] = OrganizationForm(prefix='consignee')
        context['bank_coun'] = BankDetailsOrganizationForm(prefix='buyer_bank')
        context['bank_org'] = BankDetailsOrganizationForm(prefix='organization_bank')
        object = self.get_object()
        if object:
           context['formset'] = InvoiceDocumentTableFormSet(queryset=object.items_docs.all())
        else:
            context['formset'] = InvoiceDocumentTableFormSet(queryset=InvoiceForPaymentItem.objects.none())
        context['vat_rate'] = self.vat_rate

        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()

        formset = InvoiceDocumentTableFormSet(self.request.POST)

        if formset.is_valid():
            invoice_tables = []
            formset_data = []

            for form_s in formset:
                invoice_table = form_s.save(commit=False)
                invoice_table.document_id = self.object.id
                invoice_table.save()
                invoice_tables.append(invoice_table)

                row_data = {
                    'name': form_s.cleaned_data.get('name'),
                    'unit': form_s.cleaned_data.get('unit_of_measurement'),
                    'quantity': form_s.cleaned_data.get('quantity'),
                    'price': form_s.cleaned_data.get('price'),
                    'sum': form_s.cleaned_data.get('sum')
                }

                formset_data.append(row_data)

        self.object.items_docs.set(invoice_tables)

        if form.is_valid():
            print(self.request.POST.get('download_pdf', default=None))
            if self.request.POST.get("download_excel") == "true":
                form_data = form.cleaned_data
                print("Excel::")
                
                excel_document = invoice_for_payment_excel_document_create.create_excel_document(self.object, None)
                response = HttpResponse(excel_document.read(), content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename=test UPD.pdf'
                print(response)
                return response

                return invoice_for_payment_excel_document_create.create_excel_document(self.object)

            if self.request.POST.get("download_pdf") == "true":
                form_data = form.cleaned_data
                print("PDF::")
                print(type(self.object))
                print(type(form_data))
                print(form_data)
                
                excel_document = invoice_for_payment_excel_document_create.create_excel_document(self.object, None)
                response = HttpResponse(excel_document.read(), content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename=test UPD.pdf'
                print(response)
                return response

        #return "300"
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Form validation failed with errors:", form.errors.as_data())
        return super().form_invalid(form)

def add_organization(request):
    if request.method == 'POST':

        prefix = request.POST.get('modal-prefix', None)
        print(request.POST)
        existing_org_id = request.POST.get(f'org_id', None)
        print(bool(existing_org_id))
        print(existing_org_id)
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

                return JsonResponse(
                    {
                        'name': organization.name,
                        'id': organization.id,
                    }
                )
            else:
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
                return JsonResponse(
                    {
                        'name': '2'
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
                #'stamp': organization.stamp,
                #'signature': organization.signature,
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
                'bik': bank.bik,
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
    


def invoice_document(request):
    query = request.GET.get('q', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    org_param = request.GET.get('filter_org', '')
    coun_param = request.GET.get('filter_coun', '')
    sort_param = request.GET.get('sort', '')

    documents = DocumentInvoiceForPayment.objects.select_related('organization', 'buyer').prefetch_related('items_docs').filter(user=request.user)

    if query:
        documents = documents.filter(number__icontains=query)

    if date_from:
        documents = documents.filter(date__gte=parse_date(date_from))
    if date_to:
        documents = documents.filter(date__lte=parse_date(date_to))
    if org_param:
        documents = documents.filter(organization=org_param)
    if coun_param:
        documents = documents.filter(counterparty=coun_param)

    if request.GET.get('cnt_page_paginator', ''):
        cnt_page = int(request.GET.get('cnt_page_paginator'))
    else:
        cnt_page = 20

    if sort_param:
        if sort_param == 'date_document_new':
            documents = documents.order_by('-date')
        elif sort_param == 'date_document_old':
            documents = documents.order_by('date')
        elif sort_param == 'name_document_new':
            documents = documents.order_by('name')
        elif sort_param == 'name_document_old':
            documents = documents.order_by('-name')
    else:
        documents = documents.order_by('-date')

    paginator = Paginator(documents, cnt_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    page_range = list(paginator.page_range)

    if request.method == 'POST' and 'delete_document' in request.POST:
        document_id = request.POST.get('document_id')
        document = DocumentInvoiceForPayment.objects.get(id=document_id, user=request.user)
        document.delete()
        return redirect('invoice_document')

    seller_status = Status.objects.filter(name="Seller").first()
    organizations = Organization.objects.filter(user=request.user, status_org__status=seller_status).distinct()

    buyer_status = Status.objects.filter(name="Buyer").first()
    counterparty = Organization.objects.filter(user=request.user, status_org__status=buyer_status).distinct()

    return render(request, 'invoice_document_new.html',
                  {'page_obj': page_obj, 'query': query, 'date_from': date_from, 'date_to': date_to, 'current_page': page_obj.number, 'total_pages': paginator.num_pages, 'organizations': organizations, 'counterparty':  counterparty, 'page_range': page_range})

