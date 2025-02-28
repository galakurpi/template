# apps.py
from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend.api'

    def ready(self):
        """
        Initialize app when Django starts.
        """
        # Load and register all pipeline mappings
        from .dispatcher import load_pipeline_mappings
        load_pipeline_mappings()
