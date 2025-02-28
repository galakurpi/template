# api/urls.py

from django.urls import path
from . import views, endpoints

urlpatterns = [
    # Web Auth
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Payments
    path('stripe-key/', views.get_stripe_key, name='get_stripe_key'),
    path('webhook/', views.stripe_webhook, name='stripe-webhook'),
    path('check_payment_status/', views.check_payment_status, name='check_payment_status'),
    path('cancel-subscription/', views.cancel_subscription, name='cancel_subscription'),
    path('auth-status/', views.check_auth_status, name='check_auth_status'),
    path('get_checkout_session_for_registered/', views.get_checkout_session_for_registered, name='get_checkout_session_for_registered'),
    path('delete-account/', views.delete_account, name='delete_account'),

    # Business Leads
    path('submit-business-lead/', views.submit_business_lead, name='submit_business_lead'),
    
    # Pipeline Endpoints
    path('events/process/', endpoints.process_event, name='process_event'),
    path('events/queue/', endpoints.queue_event, name='queue_event'),
    path('pipeline/test-lead/', endpoints.test_lead_pipeline, name='test_lead_pipeline'),
]