from django.urls import path
from django.shortcuts import redirect
from . import views

def redirect_to_landing(request):
    return redirect('/landing')

urlpatterns = [
    path('', redirect_to_landing, name='home'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('privacy-policy', views.privacy_policy, name='privacy_policy'),
    path('cookie-policy', views.cookie_policy, name='cookie_policy'),
    path('terms-of-service', views.terms_of_service, name='terms_of_service'),
    path('success', views.success, name='success'),
    path('cancel', views.cancel, name='cancel'),
    path('account-settings/', views.account_settings, name='account_settings'),
    path('landing/', views.landing, name='landing'),
    path('landing/contact/', views.landing_contact, name='landing_contact'),
]
