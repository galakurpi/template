"""
Base Handler Module
------------------
Defines the base handler interface that all event handlers must implement.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any

class Handler(ABC):
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
        """
        pass 