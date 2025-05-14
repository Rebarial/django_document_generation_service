from django.urls import path
from .views import UtdDocumentCreateView

urlpatterns = [
    path('', UtdDocumentCreateView.as_view(), name='utd'),
]