"""
Event Dispatcher
----------------
Routes incoming events directly to their appropriate pipelines based on event type.
"""
import logging
from typing import Dict, Any, Optional, Type

from .errors import APIException

logger = logging.getLogger(__name__)

class EventDispatcher:
    """
    Dispatches events directly to the appropriate pipeline based on event type.
    
    This class is responsible for:
    1. Registering pipelines for different event types
    2. Routing incoming events to the correct pipeline
    3. Providing a simple interface for event processing
    """
    
    _event_pipeline_mapping = {}  # Maps event types to pipeline names
    
    @classmethod
    def register_pipeline(cls, event_type: str, pipeline_name: str) -> None:
        """
        Register a pipeline for a specific event type.
        
        Args:
            event_type: The type of event this pipeline processes
            pipeline_name: The name of the pipeline to process this event type
        """
        cls._event_pipeline_mapping[event_type] = pipeline_name
        logger.info(f"Registered pipeline '{pipeline_name}' for event type '{event_type}'")
    
    @classmethod
    def get_pipeline_name(cls, event_type: str) -> Optional[str]:
        """
        Get the pipeline name for a specific event type.
        
        Args:
            event_type: The type of event
            
        Returns:
            The pipeline name for the specified event type, or None if no pipeline is registered
        """
        return cls._event_pipeline_mapping.get(event_type)
    
    @classmethod
    def dispatch(cls, event_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Dispatch an event directly to its appropriate pipeline.
        
        Args:
            event_type: The type of event to dispatch
            data: The event data to process
            
        Returns:
            The result from the pipeline
            
        Raises:
            APIException: If no pipeline is registered for the event type or pipeline processing fails
        """
        pipeline_name = cls.get_pipeline_name(event_type)
        
        if not pipeline_name:
            logger.error(f"No pipeline registered for event type: {event_type}")
            raise APIException(f"Unsupported event type: {event_type}")
        
        try:
            # Import here to avoid circular imports
            from backend.pipeline.core import get_pipeline
            
            # Get the pipeline
            pipeline = get_pipeline(pipeline_name)
            if not pipeline:
                raise APIException(f"Pipeline '{pipeline_name}' not found")
                
            # Process the data through the pipeline
            logger.info(f"Dispatching event '{event_type}' to pipeline '{pipeline_name}'")
            
            # Add event metadata to the data
            enriched_data = {
                **data,
                "event_metadata": {
                    "event_type": event_type,
                }
            }
            
            result = pipeline.process(enriched_data)
            logger.info(f"Successfully processed event '{event_type}' with pipeline '{pipeline_name}'")
            return result
            
        except Exception as e:
            logger.exception(f"Error processing event '{event_type}': {str(e)}")
            raise APIException(f"Error processing event: {str(e)}")

def load_pipeline_mappings():
    """
    Load pipeline mappings from the pipeline registry.
    This function is called when the app is ready.
    """
    try:
        # Import the pipeline registry
        from backend.pipeline.core import PIPELINE_REGISTRY
        from backend.pipeline.mappings import EVENT_PIPELINE_MAPPINGS
        
        # Register all pipeline mappings
        for event_type, pipeline_name in EVENT_PIPELINE_MAPPINGS.items():
            if pipeline_name in PIPELINE_REGISTRY:
                EventDispatcher.register_pipeline(event_type, pipeline_name)
            else:
                logger.warning(f"Cannot register mapping for event '{event_type}': Pipeline '{pipeline_name}' not found")
                
        logger.info("Successfully loaded pipeline mappings")
    except ImportError as e:
        logger.warning(f"Could not load pipeline mappings: {str(e)}")
    except Exception as e:
        logger.exception(f"Error loading pipeline mappings: {str(e)}")
