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
from django.shortcuts import get_object_or_404

def main(request):
    return render(request, 'main.html')


class InvoiceDocumentCreateView(LoginRequiredMixin, CreateView):
    model = DocumentInvoiceForPayment
    form_class = InvoiceDocumentForm
    template_name = 'invoice_document_form_new.html'
    #template_name = 'test.html'

    success_url = reverse_lazy('invoices_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        seller_status = Status.objects.filter(name='Seller').first()
        print(Status.objects.all())
        print(Organization.objects.filter(status_org__status=seller_status).distinct())
        context['org_form'] = OrganizationForm(prefix='organization')
        #context['bank_form'] = BankDetailsOrganizationForm(prefix='bank')
        context['counterparty_form'] = OrganizationForm(prefix='counterparty')
        context['consignee_form'] = OrganizationForm(prefix='consignee')
        context['bank_coun'] = BankDetailsOrganizationForm(prefix='bank_coun')
        context['bank_org'] = BankDetailsOrganizationForm(prefix='bank')#BankOrganizationForm(prefix='bank_org')
        #context['bank_coun'] = BankCounForm(prefix='bank_coun')
        context['formset'] = InvoiceDocumentTableFormSet(queryset=InvoiceForPaymentItem.objects.none())

        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()

        if form.is_valid():
            print(self.request.POST.get('download_pdf', default=None))
            if self.request.POST.get("download_excel") == "true":
                form_data = form.cleaned_data
                print("Excel::")
                print(type(self.object))
                print(type(form_data))
                print(form_data)
                
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

        return "300"
        #return super().form_valid(form)

    def form_invalid(self, form):
        print("Form validation failed with errors:", form.errors.as_data())
        return super().form_invalid(form)
    '''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = InvoiceItemFormSet(self.request.POST)
        else:
            context['formset'] = InvoiceItemFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        print("im here")
        # Привязываем документ к текущему пользователю
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
            
            # Обработка экспорта
            if 'save_pdf' in self.request.POST:
                return self.generate_pdf()
            elif 'save_excel' in self.request.POST:
                return self.generate_excel()
                
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def generate_pdf(self):
        # Реализация генерации PDF
        pass
        
    def generate_excel(self):
        # Реализация генерации Excel
        pass
    '''

def add_organization(request):
    if request.method == 'POST':

        prefix = request.POST.get('modal-prefix', None)
        print(prefix)
        existing_org_id = request.POST.get(f'modal-{prefix}-id', None)
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
        print(prefix)
        existing_org_id = request.POST.get(f'modal-{prefix}-id', None)
        print(existing_org_id)
        if prefix:
            if existing_org_id:
                organization = Organization.objects.get(id=existing_org_id)
                bank_form = BankDetailsOrganizationForm(request.POST, request.FILES, instance=organization, prefix=prefix)
            else:
                bank_form = BankDetailsOrganizationForm(request.POST, request.FILES, prefix=prefix)

            if bank_form.is_valid():

                organization = bank_form.save(commit=False)
                organization.user = request.user
                organization.save()

                StatusOrganization.objects.filter(organization=organization).delete()
                selected_statuses = bank_form.cleaned_data['statuses']
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


def fetch_organization_banks_data(request):
    """ Возвращает данные организации по переданному ID. """
    if request.method == 'GET':
        org_id = request.GET.get('org_id')
        try:
            # Ищем организацию по переданному ID
            organization = get_object_or_404(Organization, pk=org_id)
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


