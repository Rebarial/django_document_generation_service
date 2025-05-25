from django.shortcuts import render

from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from documents_сreating.models.documents.invoice_for_payment import DocumentInvoiceForPayment, InvoiceForPaymentItem
from .forms import InvoiceDocumentForm, InvoiceDocumentTableFormSet
from documents_сreating.forms import OrganizationForm, BankDetailsOrganizationForm
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.utils.dateparse import parse_date
from documents_сreating.models.organization import Organization, Status
from documents_сreating.models.reference import VatRate
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from documents_сreating.views import create_excel, create_pdf


class InvoiceDocumentCreateView(LoginRequiredMixin, CreateView):
    model = DocumentInvoiceForPayment
    form_class = InvoiceDocumentForm
    template_name = 'invoice_document_form_new.html'

    success_url = reverse_lazy('invoice_document')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request 
        return kwargs

    def get_object(self, queryset=None):
        obj = None
        id_doc = self.kwargs.get('id_doc')
        if not id_doc:
            id_doc = self.kwargs.get('id')
        if id_doc:
            obj = get_object_or_404(DocumentInvoiceForPayment, pk=id_doc)
        return obj

    def get_initial(self):
        initial = super().get_initial()
        object = self.get_object()
        if object:
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

        context['org_form'] = OrganizationForm(prefix='seller')
        context['counterparty_form'] = OrganizationForm(prefix='buyer')
        context['consignee_form'] = OrganizationForm(prefix='consignee')
        context['bank_coun'] = BankDetailsOrganizationForm(prefix='buyer_bank')
        context['bank_org'] = BankDetailsOrganizationForm(prefix='organization_bank')
        context['vat_rates'] = {v.id: float(v.rate) for v in VatRate.objects.filter(is_active=True)}
        
        object = self.get_object()
        if object:
           context['formset'] = InvoiceDocumentTableFormSet(queryset=object.items_docs.all())
        else:
            context['formset'] = InvoiceDocumentTableFormSet(queryset=InvoiceForPaymentItem.objects.none())
        context['vat_rate'] = self.vat_rate

        return context

    def form_valid(self, form):

        existing_obj = self.get_object()

        if existing_obj:
            form = InvoiceDocumentForm(self.request.POST, instance=existing_obj, request = self.request)
            if not form.is_valid():  
                return self.form_invalid(form)

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
 
        if not existing_obj:
            response = HttpResponseRedirect(self.success_url)
            return response

        if form.is_valid():
            if self.request.POST.get("download_excel") == "true":              
                return create_excel('invoice',self.object)

            if self.request.POST.get("download_pdf") == "true":
                return create_pdf('invoice', self.object)
    
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Form validation failed with errors:", form.errors.as_data())
        return super().form_invalid(form)

@login_required
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
        documents = documents.filter(buyer=coun_param)

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
            documents = documents.order_by('number')
        elif sort_param == 'name_document_old':
            documents = documents.order_by('-number')
    else:
        documents = documents.order_by('-date')

    paginator = Paginator(documents, cnt_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    page_range = list(paginator.page_range)

    if request.method == 'POST' and 'delete_document' in request.POST:
        print("im in")
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

