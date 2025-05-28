from django import forms

class OrganizationWidget(forms.Select):
    template_name = 'widgets/organization_widget.html'
    
    def __init__(self, attrs=None):
        
        if attrs is None:
            attrs = {}

        super().__init__(attrs)



class PaymentDocumentWidget(forms.TextInput):
    template_name = 'widgets/payment_document_widget.html'
    
    def render(self, name, value, attrs=None, renderer=None):
        return super().render(name, value, attrs)