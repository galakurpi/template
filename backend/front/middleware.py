from django.http import HttpRequest, HttpResponse
from typing import Callable
import logging
from django.middleware.csrf import CsrfViewMiddleware

logger = logging.getLogger(__name__)

class CsrfExemptMiddleware:
    """
    Middleware to exempt certain paths from CSRF checks.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # List of paths to exempt from CSRF
        csrf_exempt_paths = [
            '/api/login/',            # Initial login endpoint
            '/api/user/remove-token', # Token-based auth endpoint
            '/api/user/access-token', # Token-based auth endpoint
            '/api/webhook/',          # Stripe webhook (uses signature verification)
        ]
        
        # Check if the path starts with any of the exempt paths
        is_exempt = any(request.path.startswith(path) for path in csrf_exempt_paths)
        
        if is_exempt:
            logger.debug(f"Exempting CSRF check for path: {request.path}")
            setattr(request, '_dont_enforce_csrf_checks', True)
        return self.get_response(request)

class GlobalHeaders:
    """
    Middleware to set global headers for certain paths.
    """
    def __init__(self, get_response: Callable) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self.get_response(request)

        # List of paths that require SharedArrayBuffer (adjust as necessary)
        paths_requiring_cross_origin_isolation = [
        ]

        # Set headers for paths requiring cross-origin isolation
        if any(request.path.startswith(path) for path in paths_requiring_cross_origin_isolation):
            response['Cross-Origin-Opener-Policy'] = 'same-origin'
            response['Cross-Origin-Embedder-Policy'] = 'require-corp'
            
        if request.path == '/' or request.path == '':
            response['Cross-Origin-Opener-Policy'] = 'same-origin'
            response['Cross-Origin-Embedder-Policy'] = 'require-corp'

        return response

class DebugRequestMiddleware:
    """Middleware to log all requests and responses for debugging purposes."""
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Log the incoming request
        logger.info(f"DEBUG MIDDLEWARE: Request received: {request.method} {request.path}")
        logger.info(f"DEBUG MIDDLEWARE: Headers: {dict(request.headers)}")
        
        try:
            # Process the request
            response = self.get_response(request)
            
            # Log the response
            logger.info(f"DEBUG MIDDLEWARE: Response status: {response.status_code}")
            logger.info(f"DEBUG MIDDLEWARE: Response headers: {dict(response.headers)}")
            
            return response
        except Exception as e:
            # Log any exceptions
            logger.error(f"DEBUG MIDDLEWARE: Exception during request processing: {str(e)}", exc_info=True)
            # Return a simple response to avoid cascading errors
            return HttpResponse(f"Debug middleware caught an error: {str(e)}", status=500)
