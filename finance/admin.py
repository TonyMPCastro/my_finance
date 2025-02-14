from django.contrib import admin
from . import models


@admin.register(models.Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = [ 'is_active', 'name', 'code', 'created_at', 'updated_at']
    search_fields = ['name']
    list_filter = ['is_active', 'name']


@admin.register(models.PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['is_active', 'name', 'created_at', 'updated_at']
    search_fields = ['name']
    list_filter = ['is_active', 'name']

@admin.register(models.TypeMovement)
class TypeMovementAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_filter = ['name']

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display =  ['name', 'is_active', 'type_category', 'description', 'created_at', 'updated_at']
    search_fields = ['name', 'type_category__name', 'description']
    list_filter = ['is_active', 'type_category', 'name', 'description']

@admin.register(models.StatusMovement)
class StatusMovementAdmin(admin.ModelAdmin):
    list_display = ['name', 'type']
    search_fields = ['name', 'type__name']
    list_filter = ['name', 'type']

@admin.register(models.MovementFinancial)
class MovementFinancialAdmin(admin.ModelAdmin):
    list_display =  ['description', 'bank', 'value', 'value_payment', 'file', 'is_installment', 'installment', 'related_id', 'category', 'status', 'payment_at', 'due_at', 'created_at', 'updated_at']
    search_fields = ['category__name', 'description', 'status__name', 'bank__name']
    list_filter = ['category', 'description', 'payment_at', 'due_at', 'bank', 'status'] 