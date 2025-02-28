from django.contrib import admin
from django.urls import path, include, re_path
from django.shortcuts import redirect
from django.conf.urls.static import static
from django.conf import settings
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.http import HttpResponse

from . import debug_views

schema_view = get_schema_view(
    openapi.Info(
        title="Yekar Coaches API",
        default_version='v1',
        description="API documentation for Yekar Coaches platform",
        terms_of_service="https://www.yekar.es/terms/",
        contact=openapi.Contact(email="contact@yekar.es"),
        license=openapi.License(name="Proprietary"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

def debug_view(request):
    return HttpResponse("Template project backend is working!")

def detailed_debug_view(request):
    """A more detailed debug view that shows environment information."""
    import sys
    import os
    import socket
    
    try:
        # Test database connection
        from django.db import connections
        db_conn_status = {}
        for name, conn in connections.all():
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                db_conn_status[name] = "Working" if result else "Connected but query failed"
            except Exception as e:
                db_conn_status[name] = f"Error: {str(e)}"
        
        # Gather system information
        debug_info = {
            "Python version": sys.version,
            "Environment": dict(os.environ),
            "Hostname": socket.gethostname(),
            "IP addresses": socket.gethostbyname_ex(socket.gethostname()),
            "Database connections": db_conn_status,
            "Request headers": dict(request.headers),
        }
        
        # Format output
        output = "<h1>Debug Information</h1>"
        for key, value in debug_info.items():
            output += f"<h2>{key}</h2>"
            if isinstance(value, dict):
                output += "<ul>"
                for k, v in value.items():
                    output += f"<li><strong>{k}:</strong> {v}</li>"
                output += "</ul>"
            else:
                output += f"<p>{value}</p>"
        
        return HttpResponse(output)
    except Exception as e:
        return HttpResponse(f"Error in debug view: {str(e)}", status=500)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', include('front.urls')),
    path('debug/media/<path:path>', debug_views.serve_media_file, name='serve_media_file'),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('debug/', debug_view, name='debug'),
    path('detailed-debug/', detailed_debug_view, name='detailed_debug'),
]

if settings.DEBUG:
     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
