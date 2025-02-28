"""
Pipeline Core
------------
A simplified pipeline system for processing data through a series of nodes.
"""
import logging
import inspect
from typing import Dict, Any, List, Callable, Optional, Type, Union
from functools import wraps
import os
import importlib.util
import sys

logger = logging.getLogger(__name__)

# Global registry of pipelines
PIPELINE_REGISTRY = {}

class Node:
    """Base class for all pipeline nodes."""
    
    def __init__(self, name: str = None):
        """Initialize a node with an optional name."""
        self.name = name or self.__class__.__name__
    
    def process(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process data through this node.
        
        Args:
            data: The data to process
            context: The pipeline context
            
        Returns:
            Processed data
        """
        logger.debug(f"Processing node: {self.name}")
        return data
        
    def __call__(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Make nodes callable for simpler usage."""
        return self.process(data, context)

class FunctionNode(Node):
    """A node that wraps a function."""
    
    def __init__(self, func: Callable, name: str = None):
        """
        Initialize with a function.
        
        Args:
            func: The function to call when processing
            name: Optional name for the node
        """
        super().__init__(name or func.__name__)
        self.func = func
    
    def process(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process by calling the wrapped function.
        
        Args:
            data: The data to process
            context: The pipeline context
            
        Returns:
            Result of the function call
        """
        logger.debug(f"Calling function node: {self.name}")
        result = self.func(data, context)
        # If the function returned nothing, return the original data
        return result if result is not None else data

def node(func=None, *, name=None):
    """
    Decorator to convert a function into a pipeline node.
    
    Usage:
        @node
        def my_node(data, context):
            # Process data
            return data
            
        @node(name="custom_name")
        def another_node(data, context):
            # Process data
            return data
    """
    def decorator(f):
        return FunctionNode(f, name)
        
    if func is None:
        return decorator
    return decorator(func)

class Pipeline:
    """
    A simple, flexible pipeline for processing data through a series of nodes.
    """
    
    def __init__(self, name: str):
        """
        Initialize a pipeline.
        
        Args:
            name: Name of the pipeline
        """
        self.name = name
        self.nodes = []
        self.router_nodes = {}
        self._register()
    
    def _register(self):
        """Register this pipeline in the global registry."""
        PIPELINE_REGISTRY[self.name] = self
        logger.info(f"Registered pipeline: {self.name}")
    
    def add(self, node: Union[Node, Callable]) -> 'Pipeline':
        """
        Add a node to the pipeline.
        
        Args:
            node: A Node instance or a callable function
            
        Returns:
            The pipeline instance for chaining
        """
        if not isinstance(node, Node):
            # If it's a function, wrap it in a FunctionNode
            node = FunctionNode(node)
            
        self.nodes.append(node)
        return self
    
    def add_router(self, router_node: Node, routes: Dict[Any, List[Node]]) -> 'Pipeline':
        """
        Add a router node with its possible routes.
        
        Args:
            router_node: The node that determines the route
            routes: Mapping from route values to lists of nodes to execute
            
        Returns:
            The pipeline instance for chaining
        """
        self.nodes.append(router_node)
        self.router_nodes[router_node.name] = routes
        return self
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process data through the pipeline.
        
        Args:
            data: The data to process
            
        Returns:
            The processed data
        """
        logger.info(f"Starting pipeline: {self.name}")
        
        context = {
            "pipeline": {
                "name": self.name,
                "current_node": None,
                "history": []
            }
        }
        
        current_data = data
        i = 0
        
        while i < len(self.nodes):
            node = self.nodes[i]
            context["pipeline"]["current_node"] = node.name
            context["pipeline"]["history"].append(node.name)
            
            try:
                logger.debug(f"Executing node: {node.name}")
                result = node.process(current_data, context)
                current_data = result
                
                # Check if this is a router node
                if node.name in self.router_nodes:
                    route_value = current_data.get("route")
                    if route_value is not None and route_value in self.router_nodes[node.name]:
                        # Process the route's nodes
                        route_nodes = self.router_nodes[node.name][route_value]
                        for route_node in route_nodes:
                            context["pipeline"]["current_node"] = route_node.name
                            context["pipeline"]["history"].append(route_node.name)
                            current_data = route_node.process(current_data, context)
            
            except Exception as e:
                logger.exception(f"Error in node {node.name}: {str(e)}")
                current_data["error"] = str(e)
                current_data["failed_node"] = node.name
                break
                
            i += 1
            
        logger.info(f"Completed pipeline: {self.name}, executed nodes: {context['pipeline']['history']}")
        return current_data

def create_pipeline(name: str, *nodes, routers=None) -> Pipeline:
    """
    Create a pipeline with the given nodes.
    
    Args:
        name: Name of the pipeline
        *nodes: Nodes to add to the pipeline
        routers: Dictionary of router nodes and their routes
        
    Returns:
        The created pipeline
    """
    pipeline = Pipeline(name)
    
    # Add regular nodes
    for node in nodes:
        pipeline.add(node)
    
    # Add router nodes
    if routers:
        for router_node, routes in routers.items():
            pipeline.add_router(router_node, routes)
    
    return pipeline

def get_pipeline(name: str) -> Optional[Pipeline]:
    """
    Get a pipeline by name.
    
    Args:
        name: Name of the pipeline
        
    Returns:
        The pipeline, or None if not found
    """
    return PIPELINE_REGISTRY.get(name)

def list_pipelines() -> Dict[str, Pipeline]:
    """
    List all registered pipelines.
    
    Returns:
        Dictionary of pipeline names to pipeline instances
    """
    return PIPELINE_REGISTRY.copy()

def load_pipelines(directory: str = "pipelines") -> None:
    """
    Load all pipeline modules from a directory.
    
    Args:
        directory: The directory to load from, relative to the pipeline package
    """
    pipeline_dir = os.path.join(os.path.dirname(__file__), directory)
    
    if not os.path.exists(pipeline_dir):
        logger.warning(f"Pipeline directory not found: {pipeline_dir}")
        return
        
    for filename in os.listdir(pipeline_dir):
        if filename.endswith('.py') and not filename.startswith('_'):
            module_path = os.path.join(pipeline_dir, filename)
            module_name = f"backend.pipeline.{directory}.{filename[:-3]}"
            
            try:
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)
                logger.info(f"Loaded pipeline module: {module_name}")
            except Exception as e:
                logger.exception(f"Error loading pipeline module {module_name}: {e}") 