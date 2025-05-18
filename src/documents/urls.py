from django.contrib import admin
from django.urls import path, include
from utd.views import UtdDocumentCreateView
from django.conf import settings
from invoice.views import add_organization, fetch_organization_data

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('documents_сreating.urls')),
    path('users/', include('users.urls')),
    path('', include('invoice.urls')),
    path('utd/', UtdDocumentCreateView.as_view(), name='utd'),
    path('add-organization/', add_organization, name='add_organization'),
    path('fetch_organization_data', fetch_organization_data, name='fetch_organization_data')
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]