"""
API Endpoints
------------
Defines the HTTP endpoints for receiving events and data from external sources.
Handles incoming requests, validates data, and forwards to the dispatcher.
"""
import json
import logging
from typing import Dict, Any

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from .dispatcher import EventDispatcher
from .errors import APIException

logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def process_event(request):
    """
    Process an incoming event.
    
    Request format:
    {
        "event_type": "example_event",
        "data": {
            // Event-specific data
        }
    }
    
    Returns:
        A JSON response with the processing result or error message
    """
    try:
        payload = request.data
        
        # Validate request payload
        if not isinstance(payload, dict):
            return Response(
                {"error": "Invalid request format"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Extract event type and data
        event_type = payload.get('event_type')
        event_data = payload.get('data', {})
        
        if not event_type:
            return Response(
                {"error": "Missing event_type in request"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Log the incoming event
        logger.info(f"Received event of type '{event_type}'")
        logger.debug(f"Event data: {event_data}")
        
        # Dispatch the event to the appropriate handler
        result = EventDispatcher.dispatch(event_type, event_data)
        
        # Return the result
        return Response(result, status=status.HTTP_200_OK)
    
    except APIException as e:
        logger.error(f"API exception processing event: {str(e)}")
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        logger.exception(f"Error processing event: {str(e)}")
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def queue_event(request):
    """
    Queue an event for asynchronous processing.
    
    Request format:
    {
        "event_type": "example_event",
        "data": {
            // Event-specific data
        }
    }
    
    Returns:
        A JSON response confirming the event has been queued
    """
    try:
        payload = request.data
        
        # Validate request payload
        if not isinstance(payload, dict):
            return Response(
                {"error": "Invalid request format"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Extract event type and data
        event_type = payload.get('event_type')
        event_data = payload.get('data', {})
        
        if not event_type:
            return Response(
                {"error": "Missing event_type in request"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Log the incoming event
        logger.info(f"Queueing event of type '{event_type}' for async processing")
        
        # Import and call the Celery task to process the event asynchronously
        from .tasks import process_event_task
        task = process_event_task.delay(event_type, event_data)
        
        # Return confirmation that the event has been queued
        return Response({
            "message": "Event queued for processing",
            "task_id": task.id
        }, status=status.HTTP_202_ACCEPTED)
    
    except Exception as e:
        logger.exception(f"Error queueing event: {str(e)}")
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([AllowAny])  # Allow unauthenticated for testing
def test_lead_pipeline(request):
    """
    Test endpoint for the lead processing pipeline.
    
    This endpoint allows testing the lead processing pipeline without creating
    a BusinessLead in the database. It directly processes a lead through the pipeline.
    
    Request format:
    {
        "name": "John Doe",
        "email": "john@example.com",
        "company_name": "Example Corp",
        "project_budget": "$50,000+",
        "services": "AI Development",
        ...
    }
    
    Returns:
        The complete pipeline processing result
    """
    try:
        # Get lead data from request
        lead_data = request.data
        
        # Log the test request
        logger.info(f"Testing lead pipeline with data: {lead_data}")
        
        # Process the lead through the pipeline
        result = EventDispatcher.dispatch('process_lead', lead_data)
        
        # Return the complete processing result with route history
        return Response(result, status=status.HTTP_200_OK)
    
    except APIException as e:
        logger.error(f"API exception in test pipeline: {str(e)}")
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        logger.exception(f"Error in test pipeline: {str(e)}")
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
