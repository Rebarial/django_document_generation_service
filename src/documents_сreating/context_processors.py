from django.urls import resolve

def global_nav_context(request):
    """ Добавления глобальной навигационной информации. """
    nav_dict = {
        'documents': {
            'Счет': {
                'list': 'invoice_document',
                'new': 'invoice',
                'all': ['invoice_document', 'invoice']
            },
            'УПД': {
                'list': 'utd_document',
                'new': 'utd',
                'all' : ['utd', 'utd_document']
            },
        },
        'services' :{
            'Организации':{
                'list': 'profile',
                'all': ['edit_organization', 'add-counterparty-profile', 'add-organization-profile']
            }
        },
        'account':{
            'Профиль': {
                'list': 'profile',
                'all': ['profile']
            }
        }
    }

    current_url = resolve(request.path).url_name

    return {
        'nav_dict': nav_dict,
        'current_url': current_url
    }