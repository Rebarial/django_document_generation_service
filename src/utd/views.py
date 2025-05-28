from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from documents_сreating.models import DocumentUTD, UTDItem, Organization, Status, VatRate
from .forms import UtdDocumentForm, UtdDocumentTableFormSet
from django.core.paginator import Paginator
from django.utils.dateparse import parse_date
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from documents_сreating.views import create_excel, create_pdf
from django.shortcuts import get_object_or_404
from documents_сreating.forms import OrganizationForm
from django.contrib.auth.decorators import login_required

class UtdDocumentCreateView(LoginRequiredMixin, CreateView):
    model = DocumentUTD
    form_class = UtdDocumentForm
    template_name = 'utd_document_form_new.html'
    success_url = reverse_lazy('utd_document')

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
            obj = get_object_or_404(DocumentUTD, pk=id_doc)
        return obj

    def get_initial(self):
        initial = super().get_initial()
        object = self.get_object()
        if object:
            initial.update({
                'number': object.number,
                'date': object.date,
                'corr_number': object.corr_number,
                'corr_date': object.corr_date,
                'payment_document': object.payment_document,
                'shipping_document': object.shipping_document,
                'is_advance': object.is_advance,
                'seller': object.seller.pk if object.seller else None,
                'consignor': object.consignor.pk if object.consignor else None,
                'buyer': object.buyer.pk if object.buyer else None,
                'consignee': object.consignee.pk if object.consignee else None,
                'contract_id': object.contract_id,
                'document_type': object.document_type.pk if object.document_type else None,
                'vat_rate': object.vat_rate.pk if object.vat_rate else None,
                'currency': object.currency.pk if object.currency else None,
                'print_form': object.print_form,
                'transfer_basis': object.transfer_basis,
                'transport_info': object.transport_info,
                'transfer_position': object.transfer_position,
                'transfer_name': object.transfer_name,
                'transfer_date': object.transfer_date,
                'transfer_additional_info': object.transfer_additional_info,
                'transfer_responsible_position': object.transfer_responsible_position,
                'transfer_responsible_name': object.transfer_responsible_name,
                'receiver_position': object.receiver_position,
                'receiver_name': object.receiver_name,
                'receipt_date': object.receipt_date,
                'receipt_additional_info': object.receipt_additional_info,
                'receipt_responsible_position': object.receipt_responsible_position,
                'receipt_responsible_name': object.receipt_responsible_name,
                'document_seller': object.document_seller.pk if object.document_seller else None,
                'document_buyer': object.document_buyer.pk if object.document_buyer else None,
                'is_stamp': object.is_stamp,
            })
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['org_form'] = OrganizationForm(prefix='seller')
        context['buyer_form'] = OrganizationForm(prefix='buyer')
        context['consignor_form'] = OrganizationForm(prefix='consignor')
        context['consignee_form'] = OrganizationForm(prefix='consignee')
        context['document_seller_form'] = OrganizationForm(prefix='document_seller')
        context['document_buyer_form'] = OrganizationForm(prefix='document_buyer')

        context['vat_rates'] = {v.id: float(v.rate) for v in VatRate.objects.filter(is_active=True)}

        object = self.get_object()
        if object:
            context['formset'] = UtdDocumentTableFormSet(queryset=object.items_docs.all())
        else:
            context['formset'] = UtdDocumentTableFormSet(queryset=UTDItem.objects.none())

        context['column_settings'] = {
            'code': {'label': 'Код товара', 'width': '90px'},
            'name': {'label': 'Наименование', 'width': '190px'},
            'type_code': {'label': 'Код вида товара', 'width': '90px'},
            'unit': {'label': 'Единица измерения', 'width': '120px'},
            'excise': {'label': 'Акциз', 'width': '90px'},
            'quantity': {'label': 'Количество', 'width': '130px'},
            'price': {'label': 'Цена', 'width': '140px'},
            'sum': {'label': 'Сумма', 'width': '140px'},
            'country': {'label': 'Страна', 'width': '140px'},
            'gtd_number': {'label': 'ГТД', 'width': '130px'},
        }

        return context

    def form_valid(self, form):
        existing_obj = self.get_object()
        if existing_obj:
            form = UtdDocumentForm(self.request.POST, instance=existing_obj, request = self.request)
            if not form.is_valid():
                print("FORM NOT VALID")
                return self.form_invalid(form)

        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()

        formset = UtdDocumentTableFormSet(self.request.POST)

        print(formset)

        if formset.is_valid():
            invoice_tables = []
            formset_data = []

            for form_s in formset:
                invoice_table = form_s.save(commit=False)
                invoice_table.utd_id = self.object.id
                invoice_table.save()
                invoice_tables.append(invoice_table)

                row_data = {
                    'code': form_s.cleaned_data.get('code'),
                    'name': form_s.cleaned_data.get('name'),      
                    'type_code': form_s.cleaned_data.get('type_code'),
                    'unit': form_s.cleaned_data.get('unit'),
                    'excise': form_s.cleaned_data.get('excise'),
                    'quantity': form_s.cleaned_data.get('quantity'),
                    'price': form_s.cleaned_data.get('price'),
                    'sum': form_s.cleaned_data.get('amount'),
                    'country': form_s.cleaned_data.get('country'),
                    'gtd_number': form_s.cleaned_data.get('gtd_number'),                    
                }

                print(row_data)

                formset_data.append(row_data)

            self.object.items_docs.set(invoice_tables)

            if not existing_obj:
                response = HttpResponseRedirect(self.success_url)
                return response

            if form.is_valid():
                if self.request.POST.get("download_excel") == "true":
                    return create_excel('utd', self.object)

                if self.request.POST.get("download_pdf") == "true":
                    return create_pdf('utd', self.object)

        return super().form_valid(form)

    def form_invalid(self, form):
        print("Form validation failed with errors:", form.errors.as_data())
        return super().form_invalid(form)

@login_required
def utd_document(request):
    query = request.GET.get('q', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    org_param = request.GET.get('filter_org', '')
    coun_param = request.GET.get('filter_coun', '')
    sort_param = request.GET.get('sort', '')

    documents = DocumentUTD.objects.select_related('seller', 'buyer').prefetch_related('items_docs').filter(user=request.user)

    if query:
        documents = documents.filter(number__icontains=query)

    if date_from:
        documents = documents.filter(date__gte=parse_date(date_from))
    if date_to:
        documents = documents.filter(date__lte=parse_date(date_to))
    if org_param:
        documents = documents.filter(seller=org_param)
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
        document_id = request.POST.get('document_id')
        document = DocumentUTD.objects.get(id=document_id, user=request.user)
        document.delete()
        return redirect('utd_document')

    seller_status = Status.objects.filter(name="Seller").first()
    organizations = Organization.objects.filter(user=request.user, status_org__status=seller_status).distinct()

    buyer_status = Status.objects.filter(name="Buyer").first()
    counterparty = Organization.objects.filter(user=request.user, status_org__status=buyer_status).distinct()

    return render(request, 'utd_document_new.html', {
        'page_obj': page_obj,
        'query': query,
        'date_from': date_from,
        'date_to': date_to,
        'current_page': page_obj.number,
        'total_pages': paginator.num_pages,
        'organizations': organizations,
        'counterparty': counterparty,
        'page_range': page_range
    })