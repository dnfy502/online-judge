# AaryaOnlineCompiler - Admin Configuration
# Created by Aarya Agarwal

from django.contrib import admin
from .models import CodeExecution

@admin.register(CodeExecution)
class CodeExecutionAdmin(admin.ModelAdmin):
    """
    Admin interface for CodeExecution model.
    Provides a comprehensive view of code executions for monitoring and debugging.
    """
    
    list_display = [
        'id', 'language', 'status', 'execution_time', 
        'created_at', 'completed_at', 'has_output', 'has_errors'
    ]
    
    list_filter = [
        'language', 'status', 'created_at', 'completed_at'
    ]
    
    search_fields = [
        'id', 'source_code', 'output', 'error_output'
    ]
    
    readonly_fields = [
        'id', 'created_at', 'completed_at', 'execution_time', 'memory_used'
    ]
    
    fieldsets = [
        ('Basic Information', {
            'fields': ('id', 'language', 'status', 'created_at', 'completed_at')
        }),
        ('Code', {
            'fields': ('source_code', 'input_data'),
            'classes': ('collapse',)
        }),
        ('Results', {
            'fields': ('output', 'error_output'),
            'classes': ('collapse',)
        }),
        ('Performance', {
            'fields': ('execution_time', 'memory_used'),
            'classes': ('collapse',)
        })
    ]
    
    date_hierarchy = 'created_at'
    
    def has_output(self, obj):
        """Check if execution has output"""
        return bool(obj.output)
    has_output.boolean = True
    has_output.short_description = 'Has Output'
    
    def has_errors(self, obj):
        """Check if execution has errors"""
        return bool(obj.error_output)
    has_errors.boolean = True
    has_errors.short_description = 'Has Errors'
    
    def get_queryset(self, request):
        """Optimize queryset for admin list view"""
        return super().get_queryset(request).select_related()
