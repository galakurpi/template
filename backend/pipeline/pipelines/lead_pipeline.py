"""
Lead Processing Pipeline
---------------------
A pipeline for processing and routing business leads.
"""
import logging
import random
from datetime import datetime, timedelta
from typing import Dict, Any

from ..core import Pipeline, node, create_pipeline

logger = logging.getLogger(__name__)

# --------- Define nodes as simple functions ---------

@node
def analyze_lead(data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze a lead using simulated LLM."""
    logger.info(f"Analyzing lead: {data.get('name', 'Unknown')}")
    
    # Extract data for analysis
    name = data.get('name', 'Unknown')
    company = data.get('company_name', 'Unknown Company')
    budget = data.get('project_budget', 'Unknown')
    services = data.get('services', 'Unknown')
    
    # Helper functions for analysis
    def determine_priority(budget, services):
        high_value_keywords = ["enterprise", "ai", "machine learning", "automation"]
        has_high_value = any(keyword in services.lower() for keyword in high_value_keywords) if services else False
        high_budget = any(value in budget.lower() for value in ["$100,000+", "100k+", "high"]) if budget else False
        
        if high_budget and has_high_value:
            return "high"
        elif high_budget or has_high_value:
            return "medium"
        else:
            return "low"
    
    def calculate_lead_value(budget):
        if not budget:
            return round(random.uniform(1000, 10000), 2)
        if "$100,000+" in budget or "100k+" in budget:
            return round(random.uniform(100000, 500000), 2)
        elif "$50,000+" in budget or "50k+" in budget:
            return round(random.uniform(50000, 100000), 2)
        elif "$10,000+" in budget or "10k+" in budget:
            return round(random.uniform(10000, 50000), 2)
        else:
            return round(random.uniform(1000, 10000), 2)
    
    # Simulate LLM analysis
    analysis = {
        "sentiment": random.choice(["positive", "neutral", "negative"]),
        "priority": determine_priority(budget, services),
        "expected_value": calculate_lead_value(budget),
        "response_needed": True,
        "estimated_close_days": random.randint(7, 90),
    }
    
    logger.info(f"Lead analysis complete - Priority: {analysis['priority']}, Value: {analysis['expected_value']}")
    return {**data, "analysis": analysis}

@node
def route_lead(data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """Route the lead based on analysis."""
    logger.info(f"Routing lead: {data.get('name', 'Unknown')}")
    
    if "analysis" not in data:
        logger.warning("No analysis data found, defaulting to route 0")
        return {**data, "route": 0}
        
    analysis = data["analysis"]
    priority = analysis.get('priority', 'low')
    expected_value = analysis.get('expected_value', 0)
    
    # Routing logic
    if priority == "high":
        # High priority leads go to sales team
        logger.info("Lead routed to: escalation")
        return {**data, "route": "escalation"}
    elif expected_value > 50000:
        # High value leads get invoice processing
        logger.info("Lead routed to: invoice")
        return {**data, "route": "invoice"}
    else:
        # Standard leads get automated response
        logger.info("Lead routed to: response")
        return {**data, "route": "response"}

@node
def generate_response(data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """Generate a response using simulated LLM."""
    logger.info(f"Generating response for lead: {data.get('name', 'Unknown')}")
    
    name = data.get('name', 'there')
    company = data.get('company_name', 'your company')
    services = data.get('services', 'our services')
    
    # Templates for response generation
    templates = [
        f"Hi {name}, thanks for your interest in our services! We've received your inquiry about {services} and will be in touch shortly to discuss how we can help {company}.",
        f"Hello {name}, we appreciate you reaching out about {services}. Our team is reviewing your requirements and will contact you within 2 business days with a personalized proposal for {company}.",
        f"Thank you {name} for considering our services for {company}. We're excited about the possibility of working on {services} with you and will reach out soon to schedule an initial consultation."
    ]
    
    # Simulate response generation
    response = {
        "text": random.choice(templates),
        "generated_at": datetime.now().isoformat(),
        "suggested_follow_up": (datetime.now() + timedelta(days=2)).isoformat()
    }
    
    logger.info(f"Generated response for lead")
    return {**data, "response": response}

@node
def send_reply(data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """Send the generated response."""
    logger.info(f"Sending reply to lead: {data.get('name', 'Unknown')}")
    
    if "response" not in data:
        return {**data, "status": "error", "message": "No response to send"}
    
    # In a real implementation, this would send an email
    email_sent = {
        "to": data.get('email', 'unknown@example.com'),
        "subject": "Thank you for your inquiry",
        "body": data["response"]["text"],
        "sent_at": datetime.now().isoformat(),
        "status": "sent"
    }
    
    logger.info(f"Reply sent to {data.get('email', 'unknown@example.com')}")
    return {**data, "email_sent": email_sent, "status": "completed"}

@node
def escalate_ticket(data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """Escalate the lead to sales team."""
    logger.info(f"Escalating lead: {data.get('name', 'Unknown')}")
    
    analysis = data.get("analysis", {})
    
    # In a real implementation, this might create a task in a CRM
    escalation = {
        "assigned_to": "sales_team",
        "priority": analysis.get('priority', 'medium'),
        "due_date": (datetime.now() + timedelta(days=1)).isoformat(),
        "notes": f"High-priority lead from {data.get('company_name', 'Unknown')} - Expected value: ${analysis.get('expected_value', 'Unknown')}"
    }
    
    logger.info(f"Lead escalated to sales team")
    return {**data, "escalation": escalation, "status": "escalated"}

@node
def process_invoice(data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """Process invoice for high-value lead."""
    logger.info(f"Processing invoice for lead: {data.get('name', 'Unknown')}")
    
    analysis = data.get("analysis", {})
    expected_value = analysis.get('expected_value', 10000)
    
    # In a real implementation, this might prepare a custom proposal
    invoice = {
        "proposal_id": f"PROP-{random.randint(10000, 99999)}",
        "amount": expected_value,
        "services": data.get('services', 'Consulting Services'),
        "valid_until": (datetime.now() + timedelta(days=30)).isoformat(),
        "status": "draft"
    }
    
    logger.info(f"Invoice processed for lead - Amount: ${expected_value}")
    return {**data, "invoice": invoice, "status": "invoice_ready"}


# --------- Create the pipeline ---------

# Define the routing paths
route_paths = {
    "response": [generate_response, send_reply],
    "escalation": [escalate_ticket],
    "invoice": [process_invoice]
}

# Create the pipeline with the main flow and routing
lead_pipeline = create_pipeline(
    "lead_pipeline",
    analyze_lead,
    route_lead,
    routers={route_lead: route_paths}
) 