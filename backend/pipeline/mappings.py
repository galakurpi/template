"""
Event to Pipeline Mappings
-------------------------
Maps event types to the pipelines that should process them.
"""

# A simple dictionary mapping event types to pipeline names
EVENT_PIPELINE_MAPPINGS = {
    # Business lead events
    'business_lead_created': 'lead_pipeline',
    'business_lead_updated': 'lead_pipeline',
    'process_lead': 'lead_pipeline',
    
    # User events 
    'user_created': 'user_pipeline',
    
    # Example event
    'example_event': 'example_pipeline'
} 