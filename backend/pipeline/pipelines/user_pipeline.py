"""
User Processing Pipeline
---------------------
Pipeline for processing user-related events.
"""
import logging
from typing import Dict, Any
from datetime import datetime

from ..core import node, create_pipeline

logger = logging.getLogger(__name__)

@node
def process_new_user(data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """Process a newly created user."""
    user_id = data.get('user_id')
    username = data.get('username')
    email = data.get('email')
    
    logger.info(f"Processing new user: {username} (ID: {user_id})")
    
    # In a real implementation, you might:
    # - Initialize user profile
    # - Send welcome email
    # - Set up default preferences
    
    # For now, we'll just simulate these actions
    result = {
        **data,
        "welcome_email_sent": True,
        "profile_initialized": True,
        "processed_at": datetime.now().isoformat(),
        "status": "new_user_setup_complete"
    }
    
    logger.info(f"Completed processing new user: {username}")
    return result

# Create the pipeline
user_pipeline = create_pipeline(
    "user_pipeline",
    process_new_user
) 