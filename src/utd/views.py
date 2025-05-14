from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from documents_сreating.models.documents.upd import DocumentUPD
from .forms import UtdDocumentForm #, UtdDocumentTableFormSet
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.utils.dateparse import parse_date
from django.template.loader import render_to_string

class UtdDocumentCreateView(LoginRequiredMixin, CreateView):
    model = DocumentUPD
    form_class = UtdDocumentForm
    template_name = 'utd_document_form_new.html'
    success_url = reverse_lazy('utd_document')

    #def get_form_kwargs(self):
    #    kwargs = super().get_form_kwargs()
    #    kwargs['request'] = self.request
    #    return kwargs
    
    
    