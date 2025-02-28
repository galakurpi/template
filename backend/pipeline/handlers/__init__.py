"""
Handler Registration Module
-------------------------
Contains functions to register all event handlers with the dispatcher.
"""
import logging
from backend.api.dispatcher import EventDispatcher
from .example import ExampleEventHandler
from .lead_handler import LeadProcessingHandler

logger = logging.getLogger(__name__)

def register_handlers():
    """
    Register all event handlers with the dispatcher.
    This function is called when the app is ready.
    """
    from backend.api.handler import BaseHandler
    
    # Example event handler adapter
    class AdaptedExampleHandler(BaseHandler):
        def process(self, data):
            handler = ExampleEventHandler()
            return handler.process(data)
    
    # Business lead handler adapter
    class AdaptedLeadHandler(BaseHandler):
        def process(self, data):
            handler = LeadProcessingHandler()
            return handler.process(data)
    
    # Register the adapters with the event dispatcher
    EventDispatcher.register_handler('example_event', AdaptedExampleHandler)
    EventDispatcher.register_handler('business_lead_created', AdaptedLeadHandler)
    EventDispatcher.register_handler('process_lead', AdaptedLeadHandler)
    
    logger.info("All event handlers registered successfully") 