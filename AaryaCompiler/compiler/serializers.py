# AaryaOnlineCompiler - API Serializers
# Created by Aarya Agarwal

from rest_framework import serializers
from .models import CodeExecution

class CodeExecutionSerializer(serializers.ModelSerializer):
    """
    Serializer for CodeExecution model.
    Handles serialization/deserialization of code execution data for API responses.
    """
    
    class Meta:
        model = CodeExecution
        fields = [
            'id', 'language', 'source_code', 'input_data', 
            'output', 'error_output', 'status', 'execution_time', 
            'memory_used', 'created_at', 'completed_at'
        ]
        read_only_fields = [
            'id', 'output', 'error_output', 'status', 'execution_time',
            'memory_used', 'created_at', 'completed_at'
        ]

class ExecuteCodeRequestSerializer(serializers.Serializer):
    """
    Serializer for code execution requests.
    Validates incoming code execution requests from the frontend.
    """
    language = serializers.ChoiceField(
        choices=CodeExecution.LANGUAGE_CHOICES,
        default='cpp',
        help_text="Programming language for code execution"
    )
    source_code = serializers.CharField(
        min_length=1,
        help_text="Source code to be compiled and executed"
    )
    input_data = serializers.CharField(
        required=False,
        allow_blank=True,
        default="",
        help_text="Input data to be passed to the program during execution"
    )
    
    def validate_source_code(self, value):
        """
        Custom validation for source code.
        Ensures the source code is not empty and doesn't contain suspicious content.
        """
        if not value.strip():
            raise serializers.ValidationError("Source code cannot be empty")
        
        # Basic security check - prevent some dangerous operations
        dangerous_keywords = ['system(', 'exec(', 'eval(', '__import__', 'subprocess']
        for keyword in dangerous_keywords:
            if keyword in value:
                raise serializers.ValidationError(
                    f"Code contains potentially dangerous operation: {keyword}"
                )
        
        return value

class ExecuteCodeResponseSerializer(serializers.Serializer):
    """
    Serializer for code execution responses.
    Standardizes the format of execution results sent to the frontend.
    """
    id = serializers.UUIDField(read_only=True)
    status = serializers.CharField(read_only=True)
    output = serializers.CharField(read_only=True)
    error_output = serializers.CharField(read_only=True)
    execution_time = serializers.FloatField(read_only=True)
    memory_used = serializers.IntegerField(read_only=True)
    message = serializers.CharField(read_only=True)
