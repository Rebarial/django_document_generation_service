from django.urls import path
from .views import register_view, login_view, profile, logout_view, find_company_by_inn, find_bank_by_bik

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('profile/', profile, name='profile'),
    path('logout/', logout_view, name='logout'),
    path("find-company/", find_company_by_inn, name="find-company"),
    path("find-bank/", find_bank_by_bik, name="find-bank"),
]