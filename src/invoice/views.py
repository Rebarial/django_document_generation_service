from django.shortcuts import render

from django.db.models import Sum
from django.template.loader import render_to_string
from django.views.generic.edit import CreateView
from django.http import JsonResponse
from django.urls import reverse_lazy
from documents_сreating.models.documents.invoice_for_payment import DocumentInvoiceForPayment
from .forms import InvoiceDocumentForm, InvoiceItemFormSet
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.utils.dateparse import parse_date

def main(request):
    return render(request, 'main.html')


class InvoiceDocumentCreateView(LoginRequiredMixin, CreateView):
    model = DocumentInvoiceForPayment
    form_class = InvoiceDocumentForm
    template_name = 'inv_test.html'#'invoice_document_form_new.html'
    success_url = reverse_lazy('invoices_list')

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