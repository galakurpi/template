from django.conf import settings
from django.http import HttpResponse, Http404
import os

def serve_media_file(request, path):
    media_file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(media_file_path):
        with open(media_file_path, 'rb') as f:
            return HttpResponse(f.read(), content_type="video/mp4")
    else:
        raise Http404("Media file not found")
