from django import forms

class OrganizationWidget(forms.Select):
    template_name = 'widgets/organization_widget.html'
    
    def __init__(self, attrs=None):
        
        if attrs is None:
            attrs = {}

        super().__init__(attrs)