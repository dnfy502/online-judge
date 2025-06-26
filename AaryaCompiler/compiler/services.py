# AaryaOnlineCompiler - Code Execution Services
# Created by Aarya Agarwal

import os
import subprocess
import tempfile
import time
import signal
from typing import Dict, Tuple, Optional
from django.conf import settings
from .models import CodeExecution

class TimeoutException(Exception):
    """Custom exception for execution timeout"""
    pass

class CodeExecutionService:
    """
    Service class for executing code in different programming languages.
    Handles compilation, execution, and cleanup of temporary files.
    """
    
    # Execution timeout in seconds
    EXECUTION_TIMEOUT = 10
    
    # Maximum output size in bytes (1 MB)
    MAX_OUTPUT_SIZE = 1024 * 1024
    
    @staticmethod
    def timeout_handler(signum, frame):
        """Signal handler for execution timeout"""
        raise TimeoutException("Code execution timed out")
    
    @classmethod
    def execute_code(cls, execution: CodeExecution) -> Dict:
        """
        Main method to execute code based on the programming language.
        
        Args:
            execution: CodeExecution instance containing the code to execute
            
        Returns:
            Dict containing execution results
        """
        execution.status = 'running'
        execution.save()
        
        start_time = time.time()
        
        try:
            if execution.language == 'cpp':
                result = cls._execute_cpp(execution.source_code, execution.input_data)
            elif execution.language == 'python':
                result = cls._execute_python(execution.source_code, execution.input_data)
            elif execution.language == 'java':
                result = cls._execute_java(execution.source_code, execution.input_data)
            elif execution.language == 'javascript':
                result = cls._execute_javascript(execution.source_code, execution.input_data)
            else:
                result = {
                    'success': False,
                    'output': '',
                    'error': f'Unsupported language: {execution.language}',
                    'execution_time': 0
                }
            
            execution_time = time.time() - start_time
            execution.execution_time = execution_time
            execution.output = result['output']
            execution.error_output = result['error']
            execution.status = 'completed' if result['success'] else 'error'
            
        except TimeoutException:
            execution.status = 'timeout'
            execution.error_output = f'Code execution timed out after {cls.EXECUTION_TIMEOUT} seconds'
            result = {
                'success': False,
                'output': '',
                'error': execution.error_output,
                'execution_time': cls.EXECUTION_TIMEOUT
            }
        except Exception as e:
            execution.status = 'error'
            execution.error_output = f'Unexpected error: {str(e)}'
            result = {
                'success': False,
                'output': '',
                'error': execution.error_output,
                'execution_time': time.time() - start_time
            }
        
        execution.mark_completed()
        return result
    
    @classmethod
    def _execute_cpp(cls, source_code: str, input_data: str = "") -> Dict:
        """Execute C++ code"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Write source code to file
            source_file = os.path.join(temp_dir, 'main.cpp')
            executable_file = os.path.join(temp_dir, 'main')
            
            with open(source_file, 'w') as f:
                f.write(source_code)
            
            # Compile
            try:
                compile_process = subprocess.run(
                    ['g++', '-o', executable_file, source_file, '-std=c++17'],
                    capture_output=True,
                    text=True,
                    timeout=cls.EXECUTION_TIMEOUT
                )
                
                if compile_process.returncode != 0:
                    return {
                        'success': False,
                        'output': '',
                        'error': f'Compilation Error:\\n{compile_process.stderr}',
                        'execution_time': 0
                    }
                
                # Execute
                return cls._run_executable(executable_file, input_data)
                
            except subprocess.TimeoutExpired:
                raise TimeoutException("Compilation timed out")
    
    @classmethod
    def _execute_python(cls, source_code: str, input_data: str = "") -> Dict:
        """Execute Python code"""
        with tempfile.TemporaryDirectory() as temp_dir:
            source_file = os.path.join(temp_dir, 'main.py')
            
            with open(source_file, 'w') as f:
                f.write(source_code)
            
            try:
                # Set up signal handler for timeout
                signal.signal(signal.SIGALRM, cls.timeout_handler)
                signal.alarm(cls.EXECUTION_TIMEOUT)
                
                process = subprocess.run(
                    ['python3', source_file],
                    input=input_data,
                    capture_output=True,
                    text=True,
                    timeout=cls.EXECUTION_TIMEOUT
                )
                
                signal.alarm(0)  # Cancel alarm
                
                return {
                    'success': process.returncode == 0,
                    'output': cls._truncate_output(process.stdout),
                    'error': cls._truncate_output(process.stderr) if process.returncode != 0 else '',
                    'execution_time': 0  # We could implement better timing here
                }
                
            except subprocess.TimeoutExpired:
                signal.alarm(0)
                raise TimeoutException("Python execution timed out")
    
    @classmethod
    def _execute_java(cls, source_code: str, input_data: str = "") -> Dict:
        """Execute Java code"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Extract class name from source code (basic implementation)
            import re
            class_match = re.search(r'public\\s+class\\s+(\\w+)', source_code)
            class_name = class_match.group(1) if class_match else 'Main'
            
            source_file = os.path.join(temp_dir, f'{class_name}.java')
            
            with open(source_file, 'w') as f:
                f.write(source_code)
            
            try:
                # Compile
                compile_process = subprocess.run(
                    ['javac', source_file],
                    capture_output=True,
                    text=True,
                    timeout=cls.EXECUTION_TIMEOUT,
                    cwd=temp_dir
                )
                
                if compile_process.returncode != 0:
                    return {
                        'success': False,
                        'output': '',
                        'error': f'Compilation Error:\\n{compile_process.stderr}',
                        'execution_time': 0
                    }
                
                # Execute
                process = subprocess.run(
                    ['java', class_name],
                    input=input_data,
                    capture_output=True,
                    text=True,
                    timeout=cls.EXECUTION_TIMEOUT,
                    cwd=temp_dir
                )
                
                return {
                    'success': process.returncode == 0,
                    'output': cls._truncate_output(process.stdout),
                    'error': cls._truncate_output(process.stderr) if process.returncode != 0 else '',
                    'execution_time': 0
                }
                
            except subprocess.TimeoutExpired:
                raise TimeoutException("Java execution timed out")
    
    @classmethod
    def _execute_javascript(cls, source_code: str, input_data: str = "") -> Dict:
        """Execute JavaScript code using Node.js"""
        with tempfile.TemporaryDirectory() as temp_dir:
            source_file = os.path.join(temp_dir, 'main.js')
            
            with open(source_file, 'w') as f:
                f.write(source_code)
            
            try:
                process = subprocess.run(
                    ['node', source_file],
                    input=input_data,
                    capture_output=True,
                    text=True,
                    timeout=cls.EXECUTION_TIMEOUT
                )
                
                return {
                    'success': process.returncode == 0,
                    'output': cls._truncate_output(process.stdout),
                    'error': cls._truncate_output(process.stderr) if process.returncode != 0 else '',
                    'execution_time': 0
                }
                
            except subprocess.TimeoutExpired:
                raise TimeoutException("JavaScript execution timed out")
    
    @classmethod
    def _run_executable(cls, executable_path: str, input_data: str = "") -> Dict:
        """Run a compiled executable"""
        try:
            process = subprocess.run(
                [executable_path],
                input=input_data,
                capture_output=True,
                text=True,
                timeout=cls.EXECUTION_TIMEOUT
            )
            
            return {
                'success': process.returncode == 0,
                'output': cls._truncate_output(process.stdout),
                'error': cls._truncate_output(process.stderr) if process.returncode != 0 else '',
                'execution_time': 0
            }
            
        except subprocess.TimeoutExpired:
            raise TimeoutException("Executable timed out")
    
    @classmethod
    def _truncate_output(cls, output: str) -> str:
        """Truncate output if it exceeds maximum size"""
        if len(output.encode('utf-8')) > cls.MAX_OUTPUT_SIZE:
            truncated = output.encode('utf-8')[:cls.MAX_OUTPUT_SIZE].decode('utf-8', errors='ignore')
            return truncated + "\\n\\n[Output truncated due to size limit]"
        return output
