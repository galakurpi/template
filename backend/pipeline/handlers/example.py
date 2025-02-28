"""
Example Event Handler
-------------------
Implements handlers for example events. Use this as a template for creating
new event handlers.
"""
import logging
from typing import Dict, Any

from .base import Handler

logger = logging.getLogger(__name__)

class ExampleEventHandler(Handler):
    """
    Handles example events.
    
    This is a template that can be used as a reference when creating
    new event handlers.
    """
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process an example event.
        
        Args:
            data: The event data to process
            
        Returns:
            A dictionary containing the processing result
        """
        logger.info(f"Processing example event with data: {data}")
        
        # Example processing logic
        result = {
            "status": "success",
            "message": "Example event processed successfully",
            "processed_data": data,
        }
        
        return result 