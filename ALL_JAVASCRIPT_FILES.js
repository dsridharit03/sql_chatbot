# ========================================
# COMPLETE REACT FRONTEND - ALL JAVASCRIPT FILES
# ========================================

# ========================================
# FILE: frontend/src/index.js
# ========================================
import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);


# ========================================
# FILE: frontend/src/App.js
# ========================================
import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const [question, setQuestion] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [showSQL, setShowSQL] = useState(true);

  // Example questions
  const exampleQuestions = [
    'Top 10 employees from employee table',
    'Show all employees with salary greater than 50000',
    'Count total number of employees by department',
    'Find employees hired in the last year',
    'Show average salary by department',
    'List all employees in Engineering department'
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!question.trim()) {
      setError('Please enter a question');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await axios.post(`${API_URL}/api/query/`, {
        question: question
      });

      setResult(response.data);
      setShowSQL(true);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to process query. Please try again.');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleExampleClick = (example) => {
    setQuestion(example);
    setError(null);
  };

  const renderTable = (data) => {
    if (!data || data.length === 0) {
      return <div className="no-data">No results found</div>;
    }

    const columns = Object.keys(data[0]);

    return (
      <div className="table-container">
        <div className="result-header">
          <h3>Results ({data.length} rows)</h3>
        </div>
        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                {columns.map((col, idx) => (
                  <th key={idx}>{col}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {data.map((row, rowIdx) => (
                <tr key={rowIdx}>
                  {columns.map((col, colIdx) => (
                    <td key={colIdx}>
                      {row[col] !== null && row[col] !== undefined 
                        ? String(row[col]) 
                        : <span className="null-value">NULL</span>
                      }
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    );
  };

  return (
    <div className="App">
      <div className="container">
        <header className="header">
          <h1>🔍 NL2SQL Query Interface</h1>
          <p>Ask questions in plain English and get results from your SQL Server database</p>
        </header>

        <div className="main-content">
          <form onSubmit={handleSubmit} className="query-form">
            <div className="input-group">
              <textarea
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="Ask a question about your database... (e.g., 'Top 10 employees from employee table')"
                rows="3"
                disabled={loading}
              />
              <button 
                type="submit" 
                disabled={loading}
                className="submit-btn"
              >
                {loading ? (
                  <>
                    <span className="spinner"></span>
                    Processing...
                  </>
                ) : (
                  <>
                    <span className="icon">🚀</span>
                    Ask Question
                  </>
                )}
              </button>
            </div>
          </form>

          <div className="examples-section">
            <h3>Example Questions:</h3>
            <div className="examples-grid">
              {exampleQuestions.map((example, idx) => (
                <button
                  key={idx}
                  onClick={() => handleExampleClick(example)}
                  className="example-btn"
                  disabled={loading}
                >
                  {example}
                </button>
              ))}
            </div>
          </div>

          {error && (
            <div className="error-box">
              <strong>⚠️ Error:</strong> {error}
            </div>
          )}

          {result && (
            <div className="results-section">
              {showSQL && result.sql && (
                <div className="sql-box">
                  <div className="sql-header">
                    <h3>Generated SQL Query</h3>
                    <button 
                      className="toggle-btn"
                      onClick={() => setShowSQL(!showSQL)}
                    >
                      {showSQL ? 'Hide' : 'Show'}
                    </button>
                  </div>
                  <pre className="sql-query">{result.sql}</pre>
                </div>
              )}

              {renderTable(result.data)}
            </div>
          )}
        </div>

        <footer className="footer">
          <p>Powered by Django + AI (OpenAI/Claude) + SQL Server</p>
        </footer>
      </div>
    </div>
  );
}

export default App;


# ========================================
# END OF ALL JAVASCRIPT FILES
# ========================================

# ========================================
# ADDITIONAL FILES (HTML, JSON, ENV)
# ========================================

# ========================================
# FILE: frontend/public/index.html
# ========================================
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta name="description" content="Natural Language to SQL Query Interface" />
    <title>NL2SQL - Ask Questions to Your Database</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>


# ========================================
# FILE: frontend/package.json
# ========================================
{
  "name": "nl2sql-frontend",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1",
    "axios": "^1.6.0"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "eslintConfig": {
    "extends": [
      "react-app"
    ]
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }
}


# ========================================
# FILE: frontend/.env.example
# ========================================
# Backend API URL
REACT_APP_API_URL=http://localhost:8000


# ========================================
# FILE: backend/requirements.txt
# ========================================
Django==5.0
djangorestframework==3.14.0
django-cors-headers==4.3.1
pyodbc==5.0.1
python-dotenv==1.0.0
anthropic==0.18.1
openai==1.12.0


# ========================================
# FILE: backend/.env.example
# ========================================
# Django Configuration
DJANGO_SECRET_KEY=your-secret-key-change-in-production
DEBUG=True

# SQL Server Configuration
DB_SERVER=localhost
DB_NAME=NL2SQLDemo
DB_USER=sa
DB_PASSWORD=YourPassword123

# AI API Configuration (Choose one)
# Option 1: OpenAI
OPENAI_API_KEY=sk-your-openai-api-key

# Option 2: Anthropic Claude
ANTHROPIC_API_KEY=sk-ant-your-anthropic-api-key

# Choose AI Provider: 'openai' or 'anthropic'
AI_PROVIDER=openai


# ========================================
# END OF ALL CONFIGURATION FILES
# ========================================
