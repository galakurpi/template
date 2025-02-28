from django.shortcuts import render
from django.http import HttpRequest
from django.middleware.csrf import get_token
import hashlib
import os

import logging
logger = logging.getLogger(__name__)

def get_file_hash(filepath):
    """Get hash of a file's contents"""
    if not os.path.exists(filepath):
        return None
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        buf = f.read(65536)  # Read in 64kb chunks
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(65536)
    return hasher.hexdigest()[:8] 

def get_version():
    """Generate version based on bundle.css and bundle.js hashes"""
    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'frontend')
    css_hash = get_file_hash(os.path.join(static_dir, 'bundle.css')) or ''
    js_hash = get_file_hash(os.path.join(static_dir, 'bundle.js')) or ''
    return f"{css_hash}{js_hash}"

def register(request: HttpRequest):
    version = get_version()
    return render(request, 'front/register.html', {'version': version})

def login(request: HttpRequest):
    version = get_version()
    return render(request, 'front/login.html', {'version': version})

def privacy_policy(request: HttpRequest):
    version = get_version()
    return render(request, 'front/privacyPolicy.html', {'version': version})

def cookie_policy(request: HttpRequest):
    version = get_version()
    return render(request, 'front/cookiePolicy.html', {'version': version})

def terms_of_service(request: HttpRequest):
    version = get_version()
    return render(request, 'front/termsOfService.html', {'version': version})

def success(request: HttpRequest):
    version = get_version()
    return render(request, 'front/success.html', {'version': version})

def cancel(request: HttpRequest):
    version = get_version()
    return render(request, 'front/cancel.html', {'version': version})

def account_settings(request: HttpRequest):
    version = get_version()
    return render(request, 'front/accountSettings.html', {'version': version})

def landing(request: HttpRequest):
    """View for landing page"""
    version = get_version()
    return render(request, 'front/landing.html', {'version': version})

def landing_contact(request: HttpRequest):
    """View for landing contact page"""
    version = get_version()
    return render(request, 'front/landingContact.html', {'version': version})