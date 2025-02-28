"""
Celery Tasks
-----------
Defines asynchronous tasks to be processed by Celery workers.
Includes tasks for event processing, data pipeline execution, etc.
"""
import logging
from celery import shared_task
from typing import Dict, Any, Optional

from .dispatcher import EventDispatcher
from .errors import APIException

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def process_event_task(self, event_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process an event asynchronously.
    
    Args:
        event_type: The type of event to process
        data: The event data to process
        
    Returns:
        The result of event processing
        
    Raises:
        Exception: If an error occurs during processing
    """
    logger.info(f"Processing event '{event_type}' asynchronously (task ID: {self.request.id})")
    
    try:
        # Dispatch the event directly to the appropriate pipeline
        result = EventDispatcher.dispatch(event_type, data)
        logger.info(f"Successfully processed event '{event_type}' (task ID: {self.request.id})")
        return result
    
    except APIException as e:
        logger.error(f"API exception processing event '{event_type}': {str(e)}")
        # Propagate API exceptions without retry
        raise
    
    except Exception as e:
        logger.exception(f"Error processing event '{event_type}': {str(e)}")
        # Retry the task in case of unexpected errors
        try:
            # Retry with exponential backoff: 5s, 25s, 125s
            self.retry(countdown=5 ** (self.request.retries + 1))
        except self.MaxRetriesExceededError:
            logger.error(f"Max retries exceeded for event '{event_type}' (task ID: {self.request.id})")
            # Propagate the original exception
            raise

@shared_task
def cleanup_old_events():
    """
    Periodically clean up old events from the database.
    This task can be scheduled to run at regular intervals.
    """
    logger.info("Starting cleanup of old events")
    
    # Add your cleanup logic here
    # For example, delete events older than X days
    
    logger.info("Completed cleanup of old events")
