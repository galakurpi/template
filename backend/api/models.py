from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth import get_user_model
    
class AdditionalUserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_hash = models.CharField(max_length=255)
    joined_at = models.DateTimeField(auto_now=True)
    last_payment = models.DateTimeField(null=True)
    validity = models.DateTimeField(null=True)  
    customer_id = models.CharField(max_length=255, null=True) 
    subscription = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    instagram_handle = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Additional Info for {self.user.username}"


### New: Payment model for tracking payments ###
class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    checkout_id = models.CharField(max_length=255, null=True)  
    payment_date = models.DateTimeField(auto_now=True)
    product_id = models.CharField(max_length=255) 
    payment_method = models.CharField(max_length=255) 
    status = models.CharField(max_length=255)  
    customer_id = models.CharField(max_length=255, null=True) 

    def __str__(self):
        return f"Payment {self.id} by {self.user.username} - Status: {self.status}"


class BusinessLead(models.Model):
    """Stores business leads from the AI business contact form"""
    name = models.CharField(max_length=255)
    email = models.EmailField()
    role = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    company_website = models.URLField(blank=True, null=True)
    company_size = models.CharField(max_length=100)
    annual_revenue = models.CharField(max_length=100)
    project_budget = models.CharField(max_length=100)
    services = models.CharField(max_length=255)
    help_text = models.TextField(blank=True, null=True)
    preferred_language = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default="New", 
                              choices=[("New", "New"), 
                                      ("Contacted", "Contacted"), 
                                      ("In Progress", "In Progress"), 
                                      ("Converted", "Converted"), 
                                      ("Closed", "Closed")])
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['status']),
        ]
        
    def __str__(self):
        return f"{self.name} - {self.company_name or 'No Company'} - {self.created_at.strftime('%Y-%m-%d')}"