from django.urls import path, include
from .api.create_document import DocumentUPDViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'upd', DocumentUPDViewSet)

urlpatterns = [
    path("", include(router.urls)),
]