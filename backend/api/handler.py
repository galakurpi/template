"""
Event Handler Base
-----------------
Defines the base handler interface that all event handlers must implement.
Provides core functionality and utilities for processing events.
"""
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any

logger = logging.getLogger(__name__)

class BaseHandler(ABC):
    """
    Base class for all event handlers.
    
    All event processing handlers should inherit from this class and
    implement the 'process' method to handle specific event types.
    """
    
    @abstractmethod
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process an event with the given data.
        
        Args:
            data: The event data to process
            
        Returns:
            A dictionary containing the processing result
            
        Raises:
            NotImplementedError: If the subclass does not implement this method
        """
        raise NotImplementedError("Handlers must implement process method")
    
    def validate(self, data: Dict[str, Any]) -> bool:
        """
        Validate the event data before processing.
        
        Args:
            data: The event data to validate
            
        Returns:
            True if the data is valid, False otherwise
        """
        # Default implementation returns True
        # Subclasses should override this method to implement specific validation
        return True
    
    def pre_process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform any necessary pre-processing on the event data.
        
        Args:
            data: The event data to pre-process
            
        Returns:
            The pre-processed data
        """
        # Default implementation just returns the input data
        # Subclasses can override to implement specific pre-processing
        return data
    
    def post_process(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform any necessary post-processing on the result.
        
        Args:
            result: The result of event processing
            
        Returns:
            The post-processed result
        """
        # Default implementation just returns the input result
        # Subclasses can override to implement specific post-processing
        return result
