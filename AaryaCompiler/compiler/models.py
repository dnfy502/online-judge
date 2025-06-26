# AaryaOnlineCompiler - Compiler Models
# Created by Aarya Agarwal

from django.db import models
from django.utils import timezone
import uuid

class CodeExecution(models.Model):
    """
    Model to store code execution history and results.
    Tracks what code was executed, when, and what the output was.
    """
    LANGUAGE_CHOICES = [
        ('cpp', 'C++'),
        ('python', 'Python'),
        ('java', 'Java'),
        ('javascript', 'JavaScript'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('error', 'Error'),
        ('timeout', 'Timeout'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES, default='cpp')
    source_code = models.TextField(help_text="The source code to be executed")
    input_data = models.TextField(blank=True, help_text="Input data for the program")
    output = models.TextField(blank=True, help_text="Program output")
    error_output = models.TextField(blank=True, help_text="Error messages")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    execution_time = models.FloatField(null=True, blank=True, help_text="Execution time in seconds")
    memory_used = models.IntegerField(null=True, blank=True, help_text="Memory used in KB")
    created_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Code Execution"
        verbose_name_plural = "Code Executions"
    
    def __str__(self):
        return f"{self.language} execution at {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    
    @property
    def is_completed(self):
        return self.status in ['completed', 'error', 'timeout']
    
    def mark_completed(self):
        """Mark the execution as completed and set completion time"""
        if not self.completed_at:
            self.completed_at = timezone.now()
            if self.status == 'pending' or self.status == 'running':
                self.status = 'completed'
            self.save()
