# AaryaOnlineCompiler - API Views
# Created by Aarya Agarwal

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.utils import timezone
import logging

from .models import CodeExecution
from .serializers import (
    ExecuteCodeRequestSerializer,
    ExecuteCodeResponseSerializer,
    CodeExecutionSerializer
)
from .services import CodeExecutionService

# Configure logging
logger = logging.getLogger(__name__)

class HealthCheckView(APIView):
    """
    Simple health check endpoint to verify the API is running.
    Useful for frontend connectivity testing and monitoring.
    """
    
    def get(self, request):
        """Return API health status"""
        return Response({
            'status': 'healthy',
            'message': 'AaryaOnlineCompiler API is running',
            'timestamp': timezone.now(),
            'version': '1.0.0',
            'author': 'Aarya Agarwal'
        })

class ExecuteCodeView(APIView):
    """
    Main API endpoint for code execution.
    Handles POST requests with source code and returns execution results.
    """
    
    def post(self, request):
        """
        Execute code submitted by the frontend.
        
        Expected request body:
        {
            "language": "cpp",
            "source_code": "#include<iostream>\nint main(){...}",
            "input_data": "optional input for the program"
        }
        
        Returns:
        {
            "id": "uuid",
            "status": "completed|error|timeout",
            "output": "program output",
            "error_output": "error messages if any",
            "execution_time": 1.23,
            "message": "Success message"
        }
        """
        try:
            # Validate request data
            request_serializer = ExecuteCodeRequestSerializer(data=request.data)
            if not request_serializer.is_valid():
                return Response({
                    'error': 'Invalid request data',
                    'details': request_serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            
            validated_data = request_serializer.validated_data
            
            # Create code execution record
            execution = CodeExecution.objects.create(
                language=validated_data['language'],
                source_code=validated_data['source_code'],
                input_data=validated_data.get('input_data', '')
            )
            
            logger.info(f"Starting code execution {execution.id} for language {execution.language}")
            
            # Execute the code
            execution_result = CodeExecutionService.execute_code(execution)
            
            # Prepare response
            response_data = {
                'id': str(execution.id),
                'status': execution.status,
                'output': execution.output,
                'error_output': execution.error_output,
                'execution_time': execution.execution_time,
                'memory_used': execution.memory_used,
                'message': self._get_status_message(execution.status)
            }
            
            logger.info(f"Code execution {execution.id} completed with status: {execution.status}")
            
            # Return appropriate HTTP status based on execution result
            if execution.status == 'completed':
                return Response(response_data, status=status.HTTP_200_OK)
            elif execution.status == 'timeout':
                return Response(response_data, status=status.HTTP_408_REQUEST_TIMEOUT)
            else:  # error
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            logger.error(f"Unexpected error in code execution: {str(e)}")
            return Response({
                'error': 'Internal server error',
                'message': 'An unexpected error occurred while executing your code',
                'details': str(e) if request.user.is_staff else 'Contact support if this persists'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get(self, request):
        """
        Get execution history (optional feature).
        Returns recent code executions for monitoring/debugging.
        """
        try:
            # Get recent executions (limit to last 10)
            executions = CodeExecution.objects.all()[:10]
            serializer = CodeExecutionSerializer(executions, many=True)
            
            return Response({
                'executions': serializer.data,
                'count': executions.count(),
                'message': 'Recent execution history retrieved successfully'
            })
            
        except Exception as e:
            logger.error(f"Error retrieving execution history: {str(e)}")
            return Response({
                'error': 'Failed to retrieve execution history',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _get_status_message(self, status: str) -> str:
        """
        Get user-friendly status message based on execution status.
        """
        messages = {
            'completed': 'Code executed successfully!',
            'error': 'Code execution failed. Check the error output for details.',
            'timeout': 'Code execution timed out. Your program may have an infinite loop or is taking too long.',
            'pending': 'Code execution is pending...',
            'running': 'Code is currently executing...'
        }
        return messages.get(status, 'Unknown status')
