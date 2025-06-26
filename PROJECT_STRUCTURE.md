# AaryaOnlineCompiler - Project Structure

**Created by Aarya Agarwal**

## 📁 Project Overview

A complete replication of the AlgoU-Online-Compiler project using Django + React, featuring the same functionality with modern architecture and clean code organization.

```
AaryaOnlineCompiler/
├── 📂 AaryaCompiler/           # Django Backend
│   ├── 📂 AaryaCompiler/       # Main Django Project
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py         # Django settings with CORS & DRF
│   │   ├── urls.py             # Main URL configuration
│   │   └── wsgi.py
│   ├── 📂 compiler/            # Main App
│   │   ├── __init__.py
│   │   ├── admin.py            # Django admin configuration
│   │   ├── apps.py
│   │   ├── models.py           # CodeExecution model
│   │   ├── serializers.py      # DRF serializers
│   │   ├── services.py         # Code execution logic
│   │   ├── urls.py             # App URL patterns
│   │   ├── views.py            # API views
│   │   ├── tests.py
│   │   └── 📂 migrations/      # Database migrations
│   └── manage.py               # Django management script
├── 📂 frontend/                # React Frontend
│   ├── 📂 src/
│   │   ├── App.jsx             # Main React component
│   │   ├── App.css
│   │   ├── index.css           # Tailwind CSS
│   │   └── main.jsx            # React entry point
│   ├── 📂 public/
│   ├── package.json            # NPM dependencies
│   ├── tailwind.config.js      # Tailwind configuration
│   ├── postcss.config.js       # PostCSS configuration
│   └── vite.config.js          # Vite configuration
├── 📂 venv/                    # Python virtual environment
├── .gitignore                  # Git ignore rules
├── README.md                   # Main documentation
├── PROJECT_STRUCTURE.md        # This file
├── requirements.txt            # Python dependencies
├── setup.sh                    # Initial setup script
└── start.sh                    # Development server startup
```

## 🔧 Core Components

### Backend (Django)

1. **Models** (`compiler/models.py`)
   - `CodeExecution`: Stores code execution records with language, source code, results, and metadata

2. **Services** (`compiler/services.py`)
   - `CodeExecutionService`: Handles code compilation and execution for multiple languages
   - Support for C++, Python, Java, and JavaScript
   - Timeout and security management

3. **API Views** (`compiler/views.py`)
   - `ExecuteCodeView`: Main API endpoint for code execution
   - `HealthCheckView`: API health monitoring

4. **Serializers** (`compiler/serializers.py`)
   - Request/response serialization
   - Input validation and security checks

### Frontend (React)

1. **Main Component** (`src/App.jsx`)
   - Code editor with syntax highlighting
   - Language selector
   - Input/output panels
   - Execution controls

2. **Styling** (`src/index.css`)
   - Tailwind CSS utilities
   - Custom styles for code editor
   - Responsive design

## 🚀 Features Implemented

✅ **Multi-language Support**
- C++ (g++ compilation)
- Python (python3 execution)
- Java (javac + java execution)
- JavaScript (node.js execution)

✅ **Security Features**
- Code input validation
- Execution timeouts (10 seconds)
- Output size limits (1MB)
- Basic dangerous code detection

✅ **User Interface**
- Clean, modern design with Tailwind CSS
- Syntax highlighting with Prism.js
- Real-time code editing
- Responsive layout

✅ **Backend API**
- RESTful API with Django REST Framework
- CORS configuration for frontend communication
- Comprehensive error handling
- Execution history tracking

✅ **Development Tools**
- Automated setup script
- Combined startup script
- Comprehensive documentation
- Git configuration

## 🔄 Data Flow

1. **User Input**: User writes code in the React editor
2. **API Request**: Frontend sends POST request to `/api/execute/`
3. **Validation**: Django validates input and creates execution record
4. **Processing**: Code execution service compiles/runs the code
5. **Response**: Results sent back to frontend
6. **Display**: Output shown in the results panel

## 🔐 Security Considerations

- **Input Sanitization**: Validate all user inputs
- **Execution Isolation**: Use temporary directories for compilation
- **Resource Limits**: Timeout and memory restrictions
- **Code Filtering**: Basic detection of dangerous operations
- **CORS Policy**: Restricted cross-origin access

## 📊 Performance Features

- **Concurrent Execution**: Multiple users can execute code simultaneously
- **Efficient Cleanup**: Automatic temporary file removal
- **Database Optimization**: Indexed queries for execution history
- **Caching**: Static file caching for frontend assets

## 🎯 Extension Points

The architecture supports easy extension for:

- **New Languages**: Add language support in `services.py`
- **Authentication**: User login and session management
- **Code Sharing**: Save and share code snippets
- **Collaboration**: Real-time collaborative editing
- **Advanced Security**: Docker containerization
- **Performance**: Code execution metrics and profiling

## 📈 Deployment Ready

The project includes production considerations:

- **Environment Variables**: Configurable settings
- **Static Files**: Proper static file handling
- **Database**: Easy migration to PostgreSQL
- **WSGI/ASGI**: Production server compatibility
- **Logging**: Comprehensive logging system

---

**Project created by Aarya Agarwal as a modern Django + React implementation of online code compilation functionality.**
