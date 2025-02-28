from django.shortcuts import redirect
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse
from functools import wraps
from api.models import AdditionalUserInfo
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

def redirect_to_login_page():
    return redirect(reverse('login'))

def subscription_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Please log in to access this page.')
            response = redirect_to_login_page()
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            return response

        try:
            user_info = AdditionalUserInfo.objects.get(user=request.user)
            if user_info.validity and user_info.validity >= timezone.now():
                # User has a valid subscription
                response = view_func(request, *args, **kwargs)
                response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
                response['Pragma'] = 'no-cache'
                response['Expires'] = '0'
                return response
            else:
                # Subscription expired or not set
                messages.error(request, 'Your subscription has expired. Please renew to access this page.')
                return redirect(reverse('account_settings') + '?status=expired')
        except ObjectDoesNotExist:
            # User does not have AdditionalUserInfo
            messages.error(request, 'Subscription information not found. Please contact support.')
            return redirect(reverse('account_settings') + '?status=not_found')
        except Exception as e:
            messages.error(request, f'An unexpected error occurred: {str(e)}. Please try again later.')
            return redirect(reverse('account_settings') + '?status=error')

    return _wrapped_view