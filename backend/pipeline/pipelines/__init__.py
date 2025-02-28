"""
Pipeline Collection
----------------
Imports and registers all available pipelines.
"""
from ..core.registry import PipelineRegistry
from .lead_pipeline import LeadPipeline

# Register pipelines
PipelineRegistry.register("lead_pipeline", LeadPipeline) 