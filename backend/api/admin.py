from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.http import HttpResponse
import csv
from .models import AdditionalUserInfo, Payment, BusinessLead

# Unregister the default User admin
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

def export_as_csv(modeladmin, request, queryset):
    meta = modeladmin.model._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={meta.verbose_name_plural}.csv'
    writer = csv.writer(response)

    writer.writerow(field_names)
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])

    return response

export_as_csv.short_description = "Export selected entries as CSV"

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets
    
    

@admin.register(AdditionalUserInfo)
class AdditionalUserInfoAdmin(admin.ModelAdmin):
    list_display = ['user', 'customer_id', 'subscription']
    search_fields = ['user__username', 'user__email', 'customer_id']
    readonly_fields = ('joined_at',)
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'phone_number', 'instagram_handle', 'joined_at')
        }),
        ('Subscription', {
            'fields': ('subscription', 'last_payment', 'validity', 'customer_id')
        }),
    )

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment_date', 'product_id', 'payment_method', 'status', 'checkout_id')
    search_fields = ('user__username', 'product_id', 'status', 'customer_id')
    readonly_fields = ('payment_date',)  

@admin.register(BusinessLead)
class BusinessLeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'company_name', 'status', 'services', 'created_at')
    list_filter = ('status', 'company_size', 'annual_revenue', 'project_budget', 'services', 'preferred_language', 'created_at')
    search_fields = ('name', 'email', 'company_name', 'company_website', 'role')
    readonly_fields = ('created_at',)
    actions = [export_as_csv]
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'role', 'preferred_language')
        }),
        ('Company Information', {
            'fields': ('company_name', 'company_website', 'company_size', 'annual_revenue')
        }),
        ('Project Information', {
            'fields': ('project_budget', 'services', 'help_text')
        }),
        ('Status Tracking', {
            'fields': ('status', 'notes', 'created_at')
        })
    )  
