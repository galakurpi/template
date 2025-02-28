# Backend API Documentation

## Architecture Overview

The backend is built on Django with a modern event-driven architecture. It processes business events through configurable pipelines that can handle both synchronous and asynchronous operations.


## Event Processing System

The system processes events through these steps:

1. **Event Generation**: Events are triggered by API endpoints or model signals
2. **Dispatching**: The `EventDispatcher` routes events to the appropriate pipeline
3. **Processing**: The pipeline processes the event through a series of nodes
4. **Result**: The processing result is returned or stored

## Pipeline System

The pipeline system is a flexible, declarative way to process events through a series of steps.

### Key Components

- **Pipeline**: A sequence of processing nodes with defined flow
- **Node**: A single processing step (function with `@node` decorator)
- **Router**: Special node that determines which path to take next
- **Dispatcher**: Routes events to the correct pipeline

### Event-to-Pipeline Mapping

Events are mapped to pipelines in `backend/pipeline/mappings.py`:

python
EVENT_PIPELINE_MAPPINGS = {
'business_lead_created': 'lead_pipeline',
'user_created': 'user_pipeline',
# ...
}


## Creating a New Pipeline

To create a new pipeline:

1. Create a file in `backend/pipeline/pipelines/` (e.g., `my_pipeline.py`)
2. Define node functions with the `@node` decorator
3. Create the pipeline with `create_pipeline()`
4. Add the event mapping in `mappings.py`

## Triggering Events

Events can be triggered in several ways:

1. **API Endpoints**: Direct calls to process events
   ```python
   # Process synchronously
   result = EventDispatcher.dispatch('my_event_type', data)
   
   # Process asynchronously
   process_event_task.delay('my_event_type', data)
   ```

2. **Django Signals**: Automatic triggers when models change
   ```python
   @receiver(post_save, sender=MyModel)
   def model_saved(sender, instance, created, **kwargs):
       event_type = 'model_created' if created else 'model_updated'
       data = {...}  # Prepare data
       process_event_task.delay(event_type, data)
   ```

## Testing Pipelines

You can test pipelines through:

1. **Direct API calls**: Use the `/api/events/process/` endpoint
2. **Test endpoints**: Create specific test endpoints for your pipelines
3. **Unit tests**: Test individual nodes or entire pipelines

## Best Practices

1. Keep nodes small and focused on a single task
2. Use descriptive names for pipelines and nodes
3. Add proper logging in each node
4. Handle errors gracefully
5. Document the expected input and output of each node

