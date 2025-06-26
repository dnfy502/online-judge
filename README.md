# Online Compiler

**Created by Aarya Agarwal**

A modern, full-stack online code compiler that supports multiple programming languages. Built with Django REST Framework for the backend and React with Vite for the frontend.

## ✨ Features

- **Multi-language Support**: C++ and Python
- **Real-time Code Editing**: Syntax highlighting with Prism.js
- **Live Code Execution**: One-click compilation and execution
- **Responsive Design**: Clean, modern interface built with Tailwind CSS
- **Error Handling**: Comprehensive error reporting and timeout management
- **Execution History**: Track and monitor code executions
- **RESTful API**: Well-documented API endpoints for code execution

## 🛠 Tech Stack

### Backend (Django)
- **Django 5.2**: Python web framework
- **Django REST Framework**: API development
- **SQLite**: Database (easily replaceable with PostgreSQL/MySQL)
- **CORS Headers**: Cross-origin resource sharing

### Frontend (React)
- **React 18**: Modern UI library
- **Vite**: Fast build tool and development server
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: HTTP client for API calls
- **Prism.js**: Syntax highlighting
- **react-simple-code-editor**: Code editing component

## 📦 Installation

### Prerequisites
- Python 3.8+ and pip
- Node.js 16+ and npm
- GCC/G++ compiler (for C++ support)
- Java JDK (for Java support)
- Node.js (for JavaScript support)

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd AaryaOnlineCompiler
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install django djangorestframework django-cors-headers
   ```

4. **Navigate to Django project and run migrations**
   ```bash
   cd AaryaCompiler
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the Django development server**
   ```bash
   python manage.py runserver
   ```
   The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd ../frontend
   ```

2. **Install Node.js dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm run dev
   ```
   The frontend will be available at `http://localhost:5173`

## 🚀 Usage

1. **Open your browser** and navigate to `http://localhost:5173`
2. **Select a programming language** from the dropdown menu
3. **Write your code** in the editor (sample code is provided)
4. **Add input data** if your program requires it
5. **Click "Run"** to compile and execute your code
6. **View the output** in the results panel

## 📡 API Endpoints

### Base URL: `http://localhost:8000/api/`

#### Execute Code
- **POST** `/execute/`
- **Request Body**:
  ```json
  {
    "language": "cpp",
    "source_code": "#include<iostream>\nint main(){...}",
    "input_data": "optional input"
  }
  ```
- **Response**:
  ```json
  {
    "id": "uuid",
    "status": "completed",
    "output": "program output",
    "error_output": "",
    "execution_time": 0.123,
    "message": "Code executed successfully!"
  }
  ```

#### Health Check
- **GET** `/health/`
- **Response**:
  ```json
  {
    "status": "healthy",
    "message": "AaryaOnlineCompiler API is running",
    "version": "1.0.0",
    "author": "Aarya Agarwal"
  }
  ```

#### Execution History
- **GET** `/execute/`
- **Response**: List of recent code executions

## 🔧 Configuration

### Backend Configuration
- **CORS Settings**: Configure allowed origins in `settings.py`
- **Timeout Settings**: Modify execution timeout in `services.py`
- **Database**: Switch from SQLite to PostgreSQL in `settings.py`

### Frontend Configuration
- **API URL**: Update `API_BASE_URL` in `App.jsx`
- **Styling**: Customize Tailwind config in `tailwind.config.js`

## 🛡 Security Features

- **Input Validation**: Comprehensive validation of source code
- **Execution Timeout**: Prevents infinite loops (10-second limit)
- **Output Limiting**: Prevents memory exhaustion
- **Dangerous Code Detection**: Basic filtering of system calls
- **CORS Protection**: Configured cross-origin policies

## 📊 Performance

- **Execution Timeout**: 10 seconds per execution
- **Memory Limit**: 1MB output limit
- **Concurrent Support**: Handles multiple simultaneous executions
- **Database Optimization**: Indexed queries for execution history

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Aarya Agarwal**
- GitHub: [@dnfy502]
- Email: aarya.agarwal6@gmail.com

## 🙏 Acknowledgments

- Inspired by AlgoU-Online-Compiler

## 📸 Screenshots

![Code Editor Interface](screenshots/editor.png)
*Clean, modern code editing interface*

![Execution Results](screenshots/output.png)
*Real-time execution results with syntax highlighting*

## 🔮 Future Enhancements

- [ ] More programming languages (Go, Rust, C#)
- [ ] Code sharing and collaboration features
- [ ] User authentication and saved projects
- [ ] Docker-based execution for better security
- [ ] Real-time collaborative editing
- [ ] Code templates and snippets
- [ ] Performance metrics and profiling
- [ ] Integration with GitHub/GitLab

---

**Built with ❤️ by Aarya Agarwal**
