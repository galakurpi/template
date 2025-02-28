"""
Pipeline Processor
----------------
Manages the flow of data through the processing pipeline.
Coordinates event handling and transformation through various stages.
"""
import logging
from typing import Dict, Any, List, Callable, Optional

logger = logging.getLogger(__name__)

class Pipeline:
    """
    Manages a sequence of processing steps for event data.
    
    This class implements the pipeline pattern, allowing data to flow
    through a series of processing steps, with each step potentially
    transforming the data before passing it to the next step.
    """
    
    def __init__(self, name: str):
        """
        Initialize a new pipeline.
        
        Args:
            name: A name for this pipeline, used in logging
        """
        self.name = name
        self.steps: List[Callable[[Dict[str, Any]], Dict[str, Any]]] = []
        self.error_handler: Optional[Callable[[Exception, Dict[str, Any]], None]] = None
        self.logger = logging.getLogger(f"{__name__}.{self.name}")
        
    def add_step(self, step: Callable[[Dict[str, Any]], Dict[str, Any]]) -> 'Pipeline':
        """
        Add a processing step to the pipeline.
        
        Args:
            step: A function that takes a data dictionary and returns a transformed data dictionary
            
        Returns:
            The pipeline instance, for method chaining
        """
        self.steps.append(step)
        return self
        
    def set_error_handler(self, handler: Callable[[Exception, Dict[str, Any]], None]) -> 'Pipeline':
        """
        Set a handler for errors that occur during pipeline processing.
        
        Args:
            handler: A function that takes an exception and the data being processed
            
        Returns:
            The pipeline instance, for method chaining
        """
        self.error_handler = handler
        return self
        
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process data through all pipeline steps.
        
        Args:
            data: The initial data to process
            
        Returns:
            The data after being processed by all pipeline steps
            
        Raises:
            Exception: If an error occurs during processing and no error handler is set
        """
        self.logger.info(f"Starting pipeline processing with {len(self.steps)} steps")
        
        current_data = data
        
        for i, step in enumerate(self.steps):
            try:
                self.logger.debug(f"Executing step {i+1}/{len(self.steps)}")
                current_data = step(current_data)
            except Exception as e:
                self.logger.error(f"Error in pipeline step {i+1}: {str(e)}")
                
                if self.error_handler:
                    self.error_handler(e, current_data)
                    return {"error": str(e), "step": i+1}
                else:
                    raise
        
        self.logger.info("Pipeline processing completed successfully")
        return current_data 