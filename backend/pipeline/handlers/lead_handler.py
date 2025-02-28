"""
Business Lead Processing Handler
-------------------------------
Implements a handler for the lead pipeline.
"""
import logging
from typing import Dict, Any
from datetime import datetime

from .base import Handler
from ..core import get_pipeline

logger = logging.getLogger(__name__)

class LeadProcessingHandler(Handler):
    """
    Handles business lead processing using the simplified pipeline system.
    
    This handler connects the API dispatcher to the pipeline system.
    """
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a business lead through the pipeline.
        
        Args:
            data: The lead data to process
            
        Returns:
            A dictionary containing the processing result
        """
        logger.info(f"Processing business lead: {data.get('name', 'Unknown')}")
        
        # Add task context information if not present
        if "task_id" not in data:
            # Create a task ID for tracking
            task_id = f"lead_{datetime.now().strftime('%Y%m%d%H%M%S')}_{hash(str(data)) % 10000}"
            data["task_id"] = task_id
            data["created_at"] = datetime.now().isoformat()
        
        # Get the lead pipeline 
        pipeline = get_pipeline("lead_pipeline")
        if not pipeline:
            logger.error("Lead pipeline not found")
            return {"status": "error", "message": "Pipeline not found"}
        
        # Process the lead through the pipeline
        result = pipeline.process(data)
        
        # Log completion
        status = result.get("status", "unknown")
        logger.info(f"Completed processing lead: {data.get('name')} with status: {status}")
        
        return result 