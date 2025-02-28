"""
Django Signals
-------------
Connects Django model events to the pipeline processing system.
Automatically triggers events when models are created, updated, or deleted.
"""
import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models import BusinessLead, AdditionalUserInfo
from .tasks import process_event_task

logger = logging.getLogger(__name__)

@receiver(post_save, sender=BusinessLead)
def business_lead_saved(sender, instance, created, **kwargs):
    """
    Trigger event processing when a business lead is saved.
    
    Args:
        sender: The model class
        instance: The actual instance being saved
        created: A boolean; True if a new record was created
    """
    event_type = 'business_lead_created' if created else 'business_lead_updated'
    logger.info(f"Business lead {instance.id} {'created' if created else 'updated'}, triggering '{event_type}' event")
    
    # Prepare data to be sent to event processor
    data = {
        'lead_id': instance.id,
        'name': instance.name,
        'email': instance.email,
        'company_name': instance.company_name,
        'company_size': instance.company_size,
        'annual_revenue': instance.annual_revenue,
        'project_budget': instance.project_budget,
        'services': instance.services,
        'help_text': instance.help_text,
        'preferred_language': instance.preferred_language,
        'status': instance.status,
        'created': created,
    }
    
    # Process async
    process_event_task.delay(event_type, data)

@receiver(post_save, sender=User)
def user_saved(sender, instance, created, **kwargs):
    """
    Trigger event processing when a user is saved.
    
    Args:
        sender: The model class
        instance: The actual instance being saved
        created: A boolean; True if a new record was created
    """
    # Only trigger for newly created users
    if created:
        event_type = 'user_created'
        logger.info(f"User {instance.id} created, triggering '{event_type}' event")
        
        # Prepare data to be sent to event processor
        data = {
            'user_id': instance.id,
            'username': instance.username,
            'email': instance.email,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
        }
        
        # Process async
        process_event_task.delay(event_type, data)
