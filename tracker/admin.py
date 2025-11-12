from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import *

admin.site.register(RequestLogs)

admin.site.site_header = "Expense Tracker Admin"
admin.site.site_title = "Expense Tracker Admin Portal"

class TrackingHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "current_balance",
        "amount",
        "expense_type",
        "description",  
        "created_at",
        "display_cashFlow",
    )
    search_fields = (
        'expense_type',
        'description'
    )
    ordering = (
        '-created_at',
        )
    # list_filter = (
    #     "expense_type",
    # )

    def display_cashFlow(self, obj):
        if obj.amount > 0:
            return "Positive"
        return "Negative"
    
    actions = ['make_credit', 'make_debit']

    @admin.action(description="Make Seleceted Expenses as Credited")
    def make_credit(modeladmin, request, queryset):
        for q in queryset:
            obj = TrackingHistory.objects.get(id = q.id)
            if obj.amount < 0:
                obj.amount = obj.amount * -1
                obj.save()
        queryset.update(expense_type='CREDIT')

    @admin.action(description="Make Seleceted Expenses as Debited")
    def make_debit(modeladmin, request, queryset):
        for q in queryset:
            obj = TrackingHistory.objects.get(id = q.id)
            if obj.amount > 0:
                obj.amount = obj.amount * -1
                obj.save()
        queryset.update(expense_type='DEBIT')

admin.site.register(TrackingHistory, TrackingHistoryAdmin)


class CurrentBalanceAdmin(admin.ModelAdmin):
    list_display =(
        "user",
        "current_balance",
    )
admin.site.register(CurrentBalance, CurrentBalanceAdmin)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone_number', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'phone_number')
    ordering = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
