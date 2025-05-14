from django.contrib import admin
from django.urls import path, include
from utd.views import UtdDocumentCreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('documents_сreating.urls')),
    path('users/', include('users.urls')),
    path('', include('invoice.urls')),
    path('utd/', UtdDocumentCreateView.as_view(), name='utd')
]
