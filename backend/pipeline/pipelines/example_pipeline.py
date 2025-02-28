"""
Example Pipeline
--------------
A simple example pipeline to demonstrate the system.
"""
import logging
from typing import Dict, Any

from ..core import node, create_pipeline

logger = logging.getLogger(__name__)

@node
def process_example(data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """Process an example event."""
    logger.info(f"Processing example event with data: {data}")
    
    # Example processing logic
    result = {
        **data,
        "status": "success",
        "message": "Example event processed successfully",
    }
    
    return result

# Create the pipeline
example_pipeline = create_pipeline(
    "example_pipeline",
    process_example
) 