import datetime
import hashlib
import json
import os
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie, csrf_protect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils import timezone as django_timezone
from pytz import timezone
from .models import AdditionalUserInfo, Payment,BusinessLead
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication

from django.conf import settings
from django.shortcuts import render
from django.db import transaction
from django.urls import reverse

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe_publishable_key = settings.STRIPE_PUBLISHABLE_KEY

import logging
logger = logging.getLogger(__name__)

User = get_user_model()

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['email', 'password', 'first_name', 'last_name', 'product_type'],
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='User email'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='User password'),
            'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='User first name'),
            'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='User last name'),
            'product_type': openapi.Schema(type=openapi.TYPE_STRING, description='Product type (monthly, annual)'),
            'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='Optional phone number'),
            'instagram_handle': openapi.Schema(type=openapi.TYPE_STRING, description='Optional Instagram handle'),
        }
    ),
    responses={
        200: openapi.Response(
            description="Success",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'token': openapi.Schema(type=openapi.TYPE_STRING),
                    'userId': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'groups': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
                    'sessionId': openapi.Schema(type=openapi.TYPE_STRING),
                    'roles': openapi.Schema(type=openapi.TYPE_OBJECT),
                }
            )
        ),
        400: "Bad Request",
        500: "Internal Server Error"
    },
    operation_description="Register a new user "
)
@api_view(['POST', 'GET'])
@permission_classes([AllowAny])
@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = request.data
            
            # Validate required fields
            required_fields = ['email', 'password', 'first_name', 'last_name', 'product_type']
            for field in required_fields:
                if field not in data:
                    raise KeyError(f"Missing required field: {field}")

            product_type = data['product_type']
            affiliate_code = data.get('affiliate_code')

            # Perform user registration inside a transaction to ensure atomicity
            with transaction.atomic():
                # Create User
                user = create_user(data)
                # Create or get token
                token, _ = Token.objects.get_or_create(user=user)
                # Get user groups
                groups = list(user.groups.values_list('name', flat=True))
                
                # Create Stripe Checkout Session based on product_type
                checkout_session = create_stripe_checkout_session(user, product_type)
                print(f"Created checkout session with ID: {checkout_session.id}")
                print(f"Customer ID from session: {checkout_session.customer}")

                # Create or update AdditionalUserInfo for the user
                user_info, created = AdditionalUserInfo.objects.get_or_create(user=user)
                user_info.customer_id = checkout_session.customer
                user_info.validity = datetime.datetime.now(django_timezone.utc) - datetime.timedelta(days=1)  # 1 day ago
                
                # Save contact information if provided
                if 'phone_number' in data:
                    user_info.phone_number = data['phone_number']
                if 'instagram_handle' in data:
                    user_info.instagram_handle = data['instagram_handle']
                    
               
                user_info.save()
                print(f"Saved customer ID {checkout_session.customer} for user {user.email}")

            # Return response with token and session ID
            return Response({
                'token': token.key,
                'userId': user.id,
                'groups': groups,
                'sessionId': checkout_session.id,
                'email': user.email,
                'firstName': user.first_name,
                'lastName': user.last_name
            }, status=status.HTTP_200_OK)

        except KeyError as e:
            return Response({
                'error': str(e),
            }, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({
                'error': 'Validation error: ' + ', '.join(e.messages),
            }, status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.StripeError as e:
            return Response({
                'error': f'Stripe error: {str(e)}',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({
                'error': f'An error occurred: {str(e)}',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == 'GET':
        return render(request, 'front/register.html')

    return Response({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



@login_required
@csrf_protect
def get_checkout_session_for_registered(request):
    """Creates a Stripe Checkout Session based on the selected product type for a registered user."""
    
    if request.method == 'POST':
        try:    
            data = json.loads(request.body)
            product_type = data['product_type']

            user = request.user
            checkout_session = create_stripe_checkout_session(user, product_type)

            user_info = AdditionalUserInfo.objects.get(user=user)
            user_info.customer_id = checkout_session.customer
            user_info.save()
            
            return JsonResponse({
                'message': 'Checkout session created successfully',
                'sessionId': checkout_session.id
            })
        except Exception as e:
            print(f"Error creating checkout session: {str(e)}")
            return JsonResponse({'message': str(e)}, status=500)



def create_user(data):
    """Creates and returns a new User."""
    user = User.objects.create_user(
        username=data['email'],
        email=data['email'],
        password=data['password'],
        first_name=data['first_name'],
        last_name=data['last_name']
    )
    return user

def create_stripe_checkout_session(user, product_type):
    """Creates a Stripe Checkout Session based on the selected product type."""
    
    # Choose the correct price ID based on the product type
    if product_type == 'monthly':
        # price_id = 'price_1Q9tIeFKWa7GKDdS1Q7E0nNM'  # TEST
        price_id = 'price_template'  # REAL
    elif product_type == 'annual':
        price_id = 'price_template'  # Replace with the actual price ID for annual subscription
    
    print("Creating Stripe Checkout Session for user:", user.email, "with price_id:", price_id)
    
    # Determine the base URL based on DEBUG setting
    base_url = 'https://coaches.yekar.es'
    
    try:
        # First, create or get the Stripe customer
        try:
            additional_info = AdditionalUserInfo.objects.get(user=user)
            if additional_info.customer_id:
                customer = stripe.Customer.retrieve(additional_info.customer_id)
                print(f"Retrieved existing customer: {customer.id}")
            else:
                customer = stripe.Customer.create(
                    email=user.email,
                    name=f"{user.first_name} {user.last_name}"
                )
                print(f"Created new customer: {customer.id}")
                additional_info.customer_id = customer.id
                additional_info.save()
        except AdditionalUserInfo.DoesNotExist:
            customer = stripe.Customer.create(
                email=user.email,
                name=f"{user.first_name} {user.last_name}"
            )
            print(f"Created new customer: {customer.id}")
            additional_info = AdditionalUserInfo.objects.create(
                user=user,
                customer_id=customer.id
            )
    
        # Create the Stripe Checkout Session with the customer ID
        checkout_session = stripe.checkout.Session.create(
            customer=customer.id,  # Use the customer ID here
            payment_method_types=['card'],
            line_items=[
                {
                    'price': price_id,
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url=f'{base_url}{reverse("success")}?session_id={{CHECKOUT_SESSION_ID}}',
            cancel_url=f'{base_url}{reverse("cancel")}',
        )
        
        print(f"Created checkout session with ID: {checkout_session.id}")
        print(f"Customer ID from session: {checkout_session.customer}")
        
        return checkout_session
        
    except stripe.error.StripeError as e:
        print(f"Stripe error creating session: {str(e)}")
        raise e
    except Exception as e:
        print(f"Unexpected error creating session: {str(e)}")
        raise e




@swagger_auto_schema(
    method='post',
    operation_description="Web login to the system",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=['email', 'password']
    ),
    responses={
        200: 'Success - Redirects to dashboard',
        400: 'Bad Request',
        401: 'Unauthorized'
    }
)
@csrf_exempt
@api_view(['POST', 'GET'])
@permission_classes([AllowAny])
def login_view(request):
    """Handle web login submissions"""
    if request.method == 'POST':
        try:
            # Check if this is a JSON request
            is_json_request = request.content_type == 'application/json'
            
            if is_json_request:
                data = request.data
                username = data.get('email', data.get('username'))
                password = data.get('password')
            else:
                username = request.POST.get('email', request.POST.get('username'))
                password = request.POST.get('password')
            
            if not username or not password:
                if is_json_request:
                    return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
                return render(request, 'front/login.html', {'error': 'Email and password are required'})
            
            # For login, username might be email
            if '@' in username:
                try:
                    user = User.objects.get(email=username)
                    username = user.username
                except User.DoesNotExist:
                    pass
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if is_json_request:
                    return Response({
                        'redirect_url': '/dashboard',
                        'status': 'success'
                    })
                return redirect('prototype')
            else:
                if is_json_request:
                    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
                return render(request, 'front/login.html', {'error': 'Invalid credentials'})
                
        except Exception as e:
            logger.exception(f"Login error: {str(e)}")
            if is_json_request:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            return render(request, 'front/login.html', {'error': str(e)})
            
    elif request.method == 'GET':
        return render(request, 'front/login.html')
    
    return Response({'error': 'Invalid request method'}, 
                   status=status.HTTP_405_METHOD_NOT_ALLOWED)


@swagger_auto_schema(
    method='post',
    operation_description="Logout from the system",
    responses={
        200: 'Success',
    }
)
@api_view(['POST'])
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'Logout successful', 'redirect_url': '/login'})
    return JsonResponse({'message': 'Invalid request method'}, status=405)


@swagger_auto_schema(
    method='get',
    operation_description="Get Stripe publishable key",
    responses={
        200: openapi.Response('Success', schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'stripe_publishable_key': openapi.Schema(type=openapi.TYPE_STRING),
            }
        )),
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])  # Allow unauthenticated access
def get_stripe_key(request):
    return JsonResponse({
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
    })
    
@swagger_auto_schema(
    method='post',
    operation_description="Stripe webhook endpoint",
    responses={
        200: 'Success',
        400: 'Bad Request',
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])  # Allow unauthenticated access to webhook
@csrf_exempt
def stripe_webhook(request):
    # Get the webhook secret key from settings
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    logger.info("=== Stripe Webhook Called ===")
    logger.info(f"Endpoint secret: {endpoint_secret[:5]}...")  # Only log first 5 chars for security

    # Extract the payload and headers from the request
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    logger.info(f"Received signature header: {sig_header[:20]}...")  # Log part of signature

    try:
        # Verify the webhook signature
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
        logger.info("✓ Webhook signature verified successfully")
    except ValueError:
        logger.error("✗ Invalid payload")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        logger.error("✗ Invalid signature")
        return HttpResponse(status=400)

    # Log the event type and full event data
    event_type = event['type']
    logger.info(f"Event Type: {event_type}")
    logger.info(f"Full Event Data: {json.dumps(event, indent=2)}")

    if event_type == 'invoice.payment_succeeded':
        invoice = event['data']['object']
        logger.info("→ Processing payment success webhook")
        handle_invoice_payment_succeeded(invoice)

    elif event_type == 'invoice.payment_failed':
        invoice = event['data']['object']
        logger.info("→ Processing payment failed webhook")
        handle_payment_failed(invoice)
        
    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        logger.info(f"→ Processing subscription cancellation for customer: {subscription['customer']}")
        handle_subscription_cancel(subscription)

    else:
        logger.info(f"⚠ Unhandled event type: {event_type}")

    logger.info("=== Webhook Processing Complete ===\n")
    return HttpResponse(status=200)


def handle_invoice_payment_succeeded(invoice):
    logger.info("=== Processing Payment Success ===")
    
    # Extract customer info
    customer_id = invoice.get('customer')
    subscription_id = invoice.get('subscription')
    customer_email = invoice.get('customer_email')
    
    logger.info("Customer Information:")
    logger.info(f"- Customer ID: {customer_id}")
    logger.info(f"- Subscription ID: {subscription_id}")
    logger.info(f"- Customer Email: {customer_email}")

    # Fetch user
    try:
        user = User.objects.get(email=customer_email)
        logger.info(f"✓ Found user: {user.email} (ID: {user.id})")
    except User.DoesNotExist:
        logger.error(f"✗ No user found for email: {customer_email}")
        return

    # Get user info
    user_info, created = AdditionalUserInfo.objects.get_or_create(user=user)
    current_validity = user_info.validity
    logger.info("\nSubscription Status:")
    logger.info(f"- Current validity: {current_validity}")
    logger.info(f"- Is new user info: {created}")
    logger.info(f"- Current subscription status: {user_info.subscription}")
    
    # Update customer ID if needed
    if not user_info.customer_id:
        logger.info(f"→ Setting customer ID: {customer_id}")
        user_info.customer_id = customer_id
        user_info.save()

    # Get subscription details
    try:
        subscription = stripe.Subscription.retrieve(subscription_id, expand=['plan'])
        price_id = subscription['plan']['id']
        logger.info(f"\nSubscription Details:")
        logger.info(f"- Price ID: {price_id}")
        logger.info(f"- Plan: {subscription['plan']}")
    except Exception as e:
        logger.error(f"✗ Error fetching subscription: {str(e)}")
        return

    # Process subscription type
    subscription_type, validity_duration = process_price_id(price_id)
    logger.info(f"\nValidity Calculation:")
    logger.info(f"- Subscription type: {subscription_type}")
    logger.info(f"- Validity duration: {validity_duration}")

    # Update subscription
    logger.info("\nUpdating Subscription:")
    if current_validity and current_validity > django_timezone.now():
        new_validity = current_validity + datetime.timedelta(days=31)
        logger.info(f"→ Extending existing validity:")
        logger.info(f"  - Current validity: {current_validity}")
        logger.info(f"  - New validity: {new_validity}")
    else:
        new_validity = django_timezone.now() + validity_duration
        logger.info(f"→ Setting new validity period:")
        logger.info(f"  - Starting from: {django_timezone.now()}")
        logger.info(f"  - Valid until: {new_validity}")

    update_user_subscription(user, subscription_type, validity_duration, price_id, customer_id, current_validity)
    
    # Handle affiliate earnings if this is the user's first payment
    if not user_info.last_payment and user_info.referred_by:
        logger.info("\nProcessing Affiliate Earnings:")
        logger.info(f"- First payment from referred user: {user.email}")
        logger.info(f"- Referred by affiliate: {user_info.referred_by.user.email}")
        
        affiliate = user_info.referred_by
        commission = affiliate.get_current_commission()
        logger.info(f"- Current commission rate: {commission}€")
        
        # Update affiliate's total earned
        affiliate.total_earned += commission
        affiliate.save()
        logger.info(f"✓ Updated affiliate earnings: +{commission}€")
        logger.info(f"- New total earned: {affiliate.total_earned}€")
    
    logger.info("\n✓ Payment processing completed successfully")
    logger.info(f"Final user status: {user_info.subscription}")
    logger.info("=== End Payment Processing ===\n")


def process_price_id(price_id):
    # Determine subscription type based on price_id
    # if price_id == 'price_1Q9tIeFKWa7GKDdS1Q7E0nNM':  # TEST
    if price_id == 'price_1QBigmFKWa7GKDdSbB0RKYWZ':  # REAL
        subscription_type = 'monthly'
        validity_duration = datetime.timedelta(days=30)
    elif price_id == 'annual_price_id':  # Replace with actual price ID for annual
        subscription_type = 'annual'
        validity_duration = datetime.timedelta(days=365)
    else:
        logger.error(f"Unknown price ID: {price_id}")
        return None, None

    return subscription_type, validity_duration


def update_user_subscription(user, subscription_type, validity_duration, price_id, customer_id, validity=None):
    try:
        user_info = AdditionalUserInfo.objects.get(user=user)
    except AdditionalUserInfo.DoesNotExist:
        logger.error(f"No AdditionalUserInfo found for user: {user.email}")
        return

    # Create the Payment record
    Payment.objects.create(
        user=user,
        product_id=price_id,
        payment_method='stripe',
        status='completed',
        customer_id=customer_id,
    )

    # Update the user's subscription validity and other details
    user_info.last_payment = django_timezone.now()
    user_info.customer_id = customer_id  # Ensure customer ID is set

    # Set validity period
    if validity and validity > django_timezone.now():
        user_info.validity = validity + datetime.timedelta(days=30)
    else:
        user_info.validity = django_timezone.now() + validity_duration

    # Always set subscription to ACTIVE on successful payment
    user_info.subscription = 'ACTIVE'
    user_info.save()

    logger.info(f"Payment for user {user.email} was successful")
    logger.info(f"Updated subscription status to: {user_info.subscription}")
    logger.info(f"Validity period set to: {user_info.validity}")


def handle_payment_failed(invoice):
    customer_id = invoice.get('customer')
    attempt_count = invoice.get('attempt_count', 0)
    is_3d_secure = invoice.get('payment_settings', {}).get('payment_method_options', {}).get('card', {}).get('request_three_d_secure') == 'automatic'

    logger.info(f"Processing payment failure for customer {customer_id}")
    logger.info(f"Attempt count: {attempt_count}")
    logger.info(f"Is 3D Secure: {is_3d_secure}")

    try:
        user_info = AdditionalUserInfo.objects.get(customer_id=customer_id)
        
        # Only set to INACTIVE if it's not the initial 3D Secure verification
        if not is_3d_secure or attempt_count > 0:
            user_info.subscription = 'INACTIVE'  
            user_info.save()
            logger.info(f"Payment for customer {customer_id} failed. Subscription set to inactive.")
        else:
            logger.info(f"Initial 3D Secure verification for customer {customer_id}. Keeping current subscription status.")
            
    except AdditionalUserInfo.DoesNotExist:
        logger.error(f"No user found for customer ID: {customer_id}. Payment failed handling could not be completed.")
        
   
   

def handle_subscription_cancel(subscription: stripe.Subscription):
    customer_id = subscription.customer

    additional_info = AdditionalUserInfo.objects.filter(
        customer_id=customer_id).first()

    if not additional_info:
        return HttpResponse(status=400)

    additional_info.subscription = 'CANCELLED'
    additional_info.save()
        
        
        
@swagger_auto_schema(
    method='get',
    operation_description="Check payment status",
    manual_parameters=[
        openapi.Parameter('session_id', openapi.IN_QUERY, description="Stripe session ID", type=openapi.TYPE_STRING),
    ],
    responses={
        200: openapi.Response('Success', schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(type=openapi.TYPE_STRING),
                'message': openapi.Schema(type=openapi.TYPE_STRING),
            }
        )),
        400: 'Bad Request',
        404: 'Not Found',
        500: 'Server Error',
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
@csrf_protect
def check_payment_status(request):
    session_id = request.GET.get('session_id')
    print(f"Checking payment status for session: {session_id}")

    if not session_id:
        return JsonResponse({'message': 'No session ID provided.', 'status': 'error'}, status=400)

    try:
        # Retrieve the session from Stripe
        checkout_session = stripe.checkout.Session.retrieve(session_id)
        customer_id = checkout_session.customer
        payment_status = checkout_session.payment_status
        status = checkout_session.status

        print(f"Session status: {status}")
        print(f"Payment status: {payment_status}")
        print(f"Customer ID: {customer_id}")

        # Get customer email from AdditionalUserInfo using customer_id
        try:
            user_info = AdditionalUserInfo.objects.get(customer_id=customer_id)
            user = user_info.user
            print(f"Found user through customer ID: {user.email}")
        except AdditionalUserInfo.DoesNotExist:
            print(f"User info not found for customer ID: {customer_id}")
            # Don't return error here, continue with status check

        # Check various states
        if status == 'complete' and payment_status == 'paid':
            print("Payment completed successfully")
            return JsonResponse({'status': 'completed'})
        elif status == 'expired':
            print("Session expired")
            return JsonResponse({'status': 'error', 'message': 'Payment session expired'})
        elif payment_status == 'unpaid':
            print("Payment still pending")
            return JsonResponse({'status': 'pending', 'message': 'Payment processing'})
        else:
            print(f"Other status - status: {status}, payment_status: {payment_status}")
            return JsonResponse({'status': 'pending', 'message': 'Payment being processed'})

    except stripe.error.StripeError as e:
        print(f"Stripe error: {str(e)}")
        return JsonResponse({'message': str(e), 'status': 'error'}, status=500)
    except Exception as e:
        print(f"Unexpected error in check_payment_status: {str(e)}")
        return JsonResponse({'message': 'An error occurred.', 'status': 'error'}, status=500)
    
    
@swagger_auto_schema(
    method='post',
    operation_description="Cancel subscription",
    responses={
        200: openapi.Response('Success', schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'success': openapi.Schema(type=openapi.TYPE_BOOLEAN),
            }
        )),
        400: 'Bad Request',
        404: 'Not Found',
        405: 'Method Not Allowed',
    }
)
@api_view(['POST'])
@login_required
@csrf_protect
def cancel_subscription(request):
    print("="*50)
    print("CANCEL SUBSCRIPTION DEBUG")
    print(f"Request method: {request.method}")
    print(f"Request user: {request.user}")
    print(f"Request user is authenticated: {request.user.is_authenticated}")
    if hasattr(request.user, 'email'):
        print(f"User email: {request.user.email}")
    print("="*50)

    if request.method == 'POST':
        user = request.user
        # Fetch user's Stripe customer ID
        try:
            print("Attempting to fetch AdditionalUserInfo...")
            additional_info = AdditionalUserInfo.objects.get(user=user)
            print(f"Found AdditionalUserInfo:")
            print(f"- Customer ID: {additional_info.customer_id}")
            print(f"- User ID: {additional_info.user.id}")
            stripe_customer_id = additional_info.customer_id
        except AdditionalUserInfo.DoesNotExist:
            print(f"ERROR: No AdditionalUserInfo found for user: {user.email}")
            return JsonResponse({'success': False, 'message': 'No subscription found'}, status=404)
        except Exception as e:
            print(f"ERROR: Unexpected error fetching AdditionalUserInfo: {str(e)}")
            return JsonResponse({'success': False, 'message': 'Error fetching user information'}, status=500)

        try:
            print(f"Fetching Stripe subscriptions for customer: {stripe_customer_id}")
            subscriptions = stripe.Subscription.list(customer=stripe_customer_id)
            print(f"Found {len(subscriptions.data)} subscriptions")
            
            if len(subscriptions.data) == 0:
                print(f"ERROR: No active subscriptions found for user: {user.email}")
                return JsonResponse({'success': False, 'message': 'No active subscription found'}, status=404)
            
            subscription = subscriptions.data[0]
            print(f"Found subscription:")
            print(f"- Subscription ID: {subscription.id}")
            print(f"- Status: {subscription.status}")
            print(f"- Current period end: {subscription.current_period_end}")
            
            print("Attempting to cancel subscription...")
            cancelled_subscription = stripe.Subscription.delete(subscription.id)
            print(f"Subscription cancelled successfully. New status: {cancelled_subscription.status}")

            return JsonResponse({'success': True})
        except stripe.error.StripeError as e:
            print(f"STRIPE ERROR: {str(e)}")
            return JsonResponse({'success': False, 'message': f'Stripe error: {str(e)}'}, status=400)
        except Exception as e:
            print(f"UNEXPECTED ERROR: {str(e)}")
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

    print("ERROR: Invalid request method")
    return JsonResponse({'message': 'Invalid request method'}, status=405)


@swagger_auto_schema(
    method='get',
    operation_description="Check authentication status",
    responses={
        200: openapi.Response('Success', schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'is_authenticated': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'subscription_status': openapi.Schema(type=openapi.TYPE_STRING),
                'message': openapi.Schema(type=openapi.TYPE_STRING),
            }
        )),
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])  # Allow unauthenticated access
@csrf_exempt
def check_auth_status(request):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'is_authenticated': False, 'message': 'No user logged in'})

    try:
        additional_info = AdditionalUserInfo.objects.get(user=user)
        if additional_info.validity and additional_info.validity <= django_timezone.now():
            return JsonResponse({'is_authenticated': True, 'subscription_status': 'EXPIRED'})

        if additional_info.subscription == 'CANCELLED':
            response_data = {
                'is_authenticated': True,
                'email': user.email,
                'subscription_status': additional_info.subscription,
                'message': 'Subscription cancelled'
            }
        elif additional_info.subscription == 'ACTIVE':
            response_data = {
                'is_authenticated': True,
                'email': user.email,
                'subscription_status': additional_info.subscription,
                'message': 'Subscription active'
            }
        else:
            response_data = {
                'is_authenticated': True,
                'email': user.email,
                'subscription_status': additional_info.subscription,
                'message': 'Unknown subscription status'
            }

        return JsonResponse(response_data)
    except AdditionalUserInfo.DoesNotExist:
        return JsonResponse({
            'is_authenticated': True,
            'email': user.email,
            'message': 'User info not found',
            'subscription_status': None
        })

@api_view(['POST'])
@permission_classes([AllowAny])
def get_access_token(request):
    """
    Return the current user's access token.
    This endpoint exists for mobile app compatibility.
    """
    if not request.user.is_authenticated:
        return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
    
    token, _ = Token.objects.get_or_create(user=request.user)
    return Response({
        'token': token.key,
        'userId': request.user.id,
        'email': request.user.email,
        'firstName': request.user.first_name,
        'lastName': request.user.last_name,
    })

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def remove_token(request):
    """
    Remove the authentication token for the current user (logout).
    This endpoint exists for mobile app compatibility.
    """
    try:
        if request.user.is_authenticated:
            # Delete the user's auth token
            Token.objects.filter(user=request.user).delete()
            # Logout the user
            logout(request)
            return Response({'message': 'Successfully logged out'})
        return Response({'message': 'Not logged in'}, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error in remove_token: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_profile(request):
    """Get the current user's profile information."""
    if not request.user.is_authenticated:
        return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        additional_info = AdditionalUserInfo.objects.get(user=request.user)
        subscription_status = additional_info.subscription
    except AdditionalUserInfo.DoesNotExist:
        subscription_status = None

    return Response({
        'id': request.user.id,
        'email': request.user.email,
        'firstName': request.user.first_name,
        'lastName': request.user.last_name,
        'subscription_status': subscription_status
    })

@swagger_auto_schema(
    method='post',
    operation_description="Delete user account",
    responses={
        200: openapi.Response('Success', schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'success': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                'message': openapi.Schema(type=openapi.TYPE_STRING),
            }
        )),
        400: 'Bad Request',
        401: 'Unauthorized',
        500: 'Server Error',
    }
)
@api_view(['POST'])
@login_required
@csrf_protect
def delete_account(request):
    print("="*50)
    print("DELETE ACCOUNT")
    print(f"Request method: {request.method}")
    print(f"Request user: {request.user}")
    print(f"User email: {request.user.email}")
    print("="*50)

    if request.method == 'POST':
        user = request.user
        try:
            # Cancel Stripe subscription if exists
            try:
                additional_info = AdditionalUserInfo.objects.get(user=user)
                if additional_info.customer_id:
                    print(f"Found Stripe customer ID: {additional_info.customer_id}")
                    # Cancel all subscriptions for the customer
                    subscriptions = stripe.Subscription.list(customer=additional_info.customer_id)
                    for subscription in subscriptions.data:
                        print(f"Cancelling subscription: {subscription.id}")
                        stripe.Subscription.delete(subscription.id)
                    
                    # Delete the customer in Stripe
                    print(f"Deleting Stripe customer: {additional_info.customer_id}")
                    stripe.Customer.delete(additional_info.customer_id)
            except AdditionalUserInfo.DoesNotExist:
                print("No AdditionalUserInfo found - skipping Stripe cleanup")
            except stripe.error.StripeError as e:
                print(f"Stripe error during cleanup: {str(e)}")
                # Continue with account deletion even if Stripe cleanup fails

            # Delete auth token
            print("Deleting auth token...")
            Token.objects.filter(user=user).delete()

            # Delete the user
            print(f"Deleting user: {user.email}")
            user.delete()

            print("Account deletion completed successfully")
            return JsonResponse({
                'success': True,
                'message': 'Account deleted successfully'
            })

        except Exception as e:
            print(f"Error during account deletion: {str(e)}")
            return JsonResponse({
                'success': False,
                'message': f'Error deleting account: {str(e)}'
            }, status=500)

    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    }, status=405)

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['name', 'email', 'role', 'company_size', 'annual_revenue', 'project_budget', 'services', 'preferred_language'],
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Full name'),
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email address'),
            'role': openapi.Schema(type=openapi.TYPE_STRING, description='Role within organization'),
            'company_name': openapi.Schema(type=openapi.TYPE_STRING, description='Company name'),
            'company_website': openapi.Schema(type=openapi.TYPE_STRING, description='Company website'),
            'company_size': openapi.Schema(type=openapi.TYPE_STRING, description='Company size'),
            'annual_revenue': openapi.Schema(type=openapi.TYPE_STRING, description='Annual revenue'),
            'project_budget': openapi.Schema(type=openapi.TYPE_STRING, description='Project budget'),
            'services': openapi.Schema(type=openapi.TYPE_STRING, description='Services of interest'),
            'help_text': openapi.Schema(type=openapi.TYPE_STRING, description='Additional information'),
            'preferred_language': openapi.Schema(type=openapi.TYPE_STRING, description='Preferred language'),
        }
    ),
    responses={
        200: openapi.Response(
            description="Success",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'success': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    'message': openapi.Schema(type=openapi.TYPE_STRING),
                }
            )
        ),
        400: "Bad Request",
        500: "Internal Server Error"
    },
    operation_description="Submit business lead from AI business contact form"
)
@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def submit_business_lead(request):
    """Handle business lead form submissions"""
    logger.info("Business lead submission received")
    logger.info(f"Request method: {request.method}")
    logger.info(f"Content type: {request.content_type}")
    
    if request.method != 'POST':
        logger.warning(f"Invalid request method: {request.method}")
        return Response({
            'success': False,
            'message': 'Only POST requests are allowed'
        }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    try:
        # Log request body
        body = request.body.decode('utf-8')
        logger.info(f"Raw request body: {body}")
        
        # Parse data based on content type
        if request.content_type == 'application/json':
            try:
                data = json.loads(body)
                logger.info(f"Parsed JSON data: {data}")
            except json.JSONDecodeError as e:
                logger.error(f"JSON parse error: {str(e)}")
                return Response({
                    'success': False,
                    'message': 'Invalid JSON format'
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            data = request.data
            logger.info(f"Form data from request.data: {data}")
        
        # Validate required fields
        required_fields = ['name', 'email', 'role', 'company_size', 
                          'annual_revenue', 'project_budget', 'services', 'preferred_language']
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            logger.warning(f"Missing required fields: {missing_fields}")
            return Response({
                'success': False,
                'message': f'Missing required fields: {", ".join(missing_fields)}'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create new lead
        logger.info("Creating new business lead")
        lead = BusinessLead(
            name=data['name'],
            email=data['email'],
            role=data['role'],
            company_name=data.get('company_name', ''),
            company_website=data.get('company_website', ''),
            company_size=data['company_size'],
            annual_revenue=data['annual_revenue'],
            project_budget=data['project_budget'],
            services=data['services'],
            help_text=data.get('help_text', ''),
            preferred_language=data['preferred_language']
        )
        lead.save()
        
        logger.info(f"New business lead saved successfully: {lead.id} - {lead.name} ({lead.email})")
        
        # Send notification email to admins (optional, implement later)
        # This would notify staff about the new lead
        
        return Response({
            'success': True,
            'message': 'Thank you for your inquiry. We will contact you shortly.'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error submitting business lead: {str(e)}")
        logger.exception("Full traceback for business lead submission error")
        return Response({
            'success': False,
            'message': 'An error occurred while processing your request.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)