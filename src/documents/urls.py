from django.contrib import admin
from django.urls import path, include
from utd.views import UtdDocumentCreateView
from django.conf import settings
from django.conf.urls.static import static
from documents_сreating.views  import add_organization, fetch_organization_data, fetch_organization_bank_data, fetch_bank_from_organization

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('documents_сreating.urls')),
    path('users/', include('users.urls')),
    path('invoice/', include('invoice.urls')),
    path('utd/', include('utd.urls')),
    path('utd/', UtdDocumentCreateView.as_view(), name='utd'),
    path('add-organization/', add_organization, name='add_organization'),
    path('fetch_organization_data/', fetch_organization_data, name='fetch_organization_data'),
    path('fetch_organization_bank_data/', fetch_organization_bank_data, name='fetch_organization_bank_data'),
    path('fetch_bank_from_organization/', fetch_bank_from_organization, name='fetch_bank_from_organization'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]