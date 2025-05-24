from django.forms import Widget
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

class OrganizationWidget(Widget):
    def __init__(self, attrs=None):
        super().__init__(attrs)

    def render(self, name, value, attrs=None, renderer=None):
        context = {
            'organization_field': {
                'id_for_label': attrs.get('id', '') if attrs else '',
                'label': 'Организация',
                'value': value,
                'name': name,
                'required': self.is_required,
                'help_text': self.attrs.get('help_text', ''),
            },
            'bank_field': {
                'id_for_label': f"{attrs.get('id', '')}_bank" if attrs else '',
                'label': 'Банк организации',
                'name': f"{name}_bank",
                'required': self.attrs.get('bank_required', False),
                'help_text': self.attrs.get('bank_help_text', ''),
            }
        }
        
        return mark_safe(render_to_string('widgets/organization_widget.html', context))