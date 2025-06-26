/**
 * AaryaOnlineCompiler - Main React Application
 * Created by Aarya Agarwal
 * 
 * A modern online code compiler supporting multiple programming languages.
 * Features a clean, responsive interface with real-time code editing and execution.
 */

import { useState } from 'react'
import axios from 'axios'
import Editor from 'react-simple-code-editor'
import { highlight, languages } from 'prismjs/components/prism-core'
import 'prismjs/components/prism-clike'
import 'prismjs/components/prism-cpp'
import 'prismjs/components/prism-python'
import 'prismjs/components/prism-java'
import 'prismjs/components/prism-javascript'

// API Configuration
const API_BASE_URL = 'http://localhost:8000/api'

// Default code examples for different languages
const DEFAULT_CODE = {
  cpp: `#include <iostream>
using namespace std;

int main() {
    cout << "Hello, World from AaryaOnlineCompiler!" << endl;
    return 0;
}`,
  python: `# Welcome to AaryaOnlineCompiler
# Created by Aarya Agarwal

print("Hello, World from AaryaOnlineCompiler!")`,
  java: `public class Main {
    public static void main(String[] args) {
        System.out.println("Hello, World from AaryaOnlineCompiler!");
    }
}`,
  javascript: `// Welcome to AaryaOnlineCompiler
// Created by Aarya Agarwal

console.log("Hello, World from AaryaOnlineCompiler!");`
}

function App() {
  const [language, setLanguage] = useState('cpp')
  const [code, setCode] = useState(DEFAULT_CODE.cpp)
  const [input, setInput] = useState('')
  const [output, setOutput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [executionTime, setExecutionTime] = useState(null)
  const [status, setStatus] = useState('')

  // Handle language change
  const handleLanguageChange = (newLanguage) => {
    setLanguage(newLanguage)
    setCode(DEFAULT_CODE[newLanguage])
    setOutput('')
    setStatus('')
    setExecutionTime(null)
  }

  // Execute code
  const executeCode = async () => {
    if (!code.trim()) {
      setOutput('Error: Please enter some code to execute.')
      return
    }

    setIsLoading(true)
    setOutput('Executing your code...')
    setStatus('running')

    try {
      const response = await axios.post(`${API_BASE_URL}/execute/`, {
        language: language,
        source_code: code,
        input_data: input
      })

      const result = response.data
      setStatus(result.status)
      setExecutionTime(result.execution_time)
      
      if (result.status === 'completed') {
        setOutput(result.output || 'Program executed successfully (no output)')
      } else {
        setOutput(result.error_output || 'An error occurred during execution')
      }
    } catch (error) {
      console.error('Execution error:', error)
      setStatus('error')
      
      if (error.response?.data) {
        setOutput(`Error: ${error.response.data.message || error.response.data.error || 'Unknown error occurred'}`)
      } else {
        setOutput('Error: Unable to connect to the compiler service. Please check if the backend is running.')
      }
    } finally {
      setIsLoading(false)
    }
  }

  // Get syntax highlighting for the selected language
  const getLanguageForHighlight = () => {
    const langMap = {
      cpp: languages.cpp,
      python: languages.python,
      java: languages.java,
      javascript: languages.javascript
    }
    return langMap[language] || languages.cpp
  }

  // Get status color
  const getStatusColor = () => {
    switch (status) {
      case 'completed': return 'text-green-600'
      case 'error': return 'text-red-600'
      case 'timeout': return 'text-yellow-600'
      case 'running': return 'text-blue-600'
      default: return 'text-gray-600'
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">AaryaOnlineCompiler</h1>
              <p className="text-sm text-gray-600">Created by Aarya Agarwal</p>
            </div>
            <div className="flex items-center space-x-4">
              {/* Language Selector */}
              <select
                value={language}
                onChange={(e) => handleLanguageChange(e.target.value)}
                className="border border-gray-300 rounded-md px-3 py-2 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="cpp">C++</option>
                <option value="python">Python</option>
                <option value="java">Java</option>
                <option value="javascript">JavaScript</option>
              </select>
              
              {/* Run Button */}
              <button
                onClick={executeCode}
                disabled={isLoading}
                className="bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white px-6 py-2 rounded-md font-medium transition-colors duration-200 flex items-center space-x-2"
              >
                {isLoading ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                    <span>Running...</span>
                  </>
                ) : (
                  <>
                    <span>▶</span>
                    <span>Run</span>
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Code Editor Section */}
          <div className="space-y-4">
            <div className="bg-white rounded-lg shadow border">
              <div className="border-b px-4 py-3">
                <h2 className="text-lg font-semibold text-gray-900">Code Editor</h2>
              </div>
              <div className="p-4">
                <Editor
                  value={code}
                  onValueChange={setCode}
                  highlight={(code) => highlight(code, getLanguageForHighlight())}
                  padding={10}
                  style={{
                    fontFamily: '"Fira code", "Fira Mono", monospace',
                    fontSize: 14,
                    backgroundColor: '#f8f9fa',
                    minHeight: '300px',
                    border: '1px solid #e9ecef',
                    borderRadius: '6px'
                  }}
                  className="min-h-[300px]"
                />
              </div>
            </div>

            {/* Input Section */}
            <div className="bg-white rounded-lg shadow border">
              <div className="border-b px-4 py-3">
                <h2 className="text-lg font-semibold text-gray-900">Input (Optional)</h2>
              </div>
              <div className="p-4">
                <textarea
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Enter input for your program here..."
                  className="w-full h-24 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono text-sm"
                />
              </div>
            </div>
          </div>

          {/* Output Section */}
          <div className="space-y-4">
            <div className="bg-white rounded-lg shadow border">
              <div className="border-b px-4 py-3 flex items-center justify-between">
                <h2 className="text-lg font-semibold text-gray-900">Output</h2>
                {status && (
                  <div className="flex items-center space-x-2">
                    <span className={`text-sm font-medium ${getStatusColor()}`}>
                      {status.charAt(0).toUpperCase() + status.slice(1)}
                    </span>
                    {executionTime !== null && (
                      <span className="text-sm text-gray-500">
                        ({executionTime.toFixed(3)}s)
                      </span>
                    )}
                  </div>
                )}
              </div>
              <div className="p-4">
                <pre className="bg-gray-900 text-green-400 p-4 rounded-md overflow-x-auto min-h-[300px] font-mono text-sm whitespace-pre-wrap">
                  {output || 'Click "Run" to execute your code and see the output here.'}
                </pre>
              </div>
            </div>

            {/* Info Panel */}
            <div className="bg-white rounded-lg shadow border">
              <div className="border-b px-4 py-3">
                <h2 className="text-lg font-semibold text-gray-900">Information</h2>
              </div>
              <div className="p-4 space-y-3">
                <div className="text-sm text-gray-600">
                  <p><strong>Current Language:</strong> {language.toUpperCase()}</p>
                  <p><strong>Execution Timeout:</strong> 10 seconds</p>
                  <p><strong>Memory Limit:</strong> 512 MB</p>
                </div>
                <div className="text-xs text-gray-500">
                  <p>• Write your code in the editor above</p>
                  <p>• Add input data if your program requires it</p>
                  <p>• Click "Run" to compile and execute</p>
                  <p>• View results in the output panel</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="mt-12 border-t bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between text-sm text-gray-600">
            <p>© 2024 AaryaOnlineCompiler - Created by Aarya Agarwal</p>
            <p>Built with Django + React</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App
