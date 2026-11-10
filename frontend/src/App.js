import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const [question, setQuestion] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [showSQL, setShowSQL] = useState(true);
  const [isTyping, setIsTyping] = useState(false);

  // Example questions with categories
  const exampleCategories = {
    'Basic Queries': [
      'Show all customers',
      'Top 10 records from any table',
      'Count total records in employee table',
    ],
    'Analytics': [
      'Show average salary by department',
      'Count employees by department',
      'Find highest paid employee',
    ],
    'Filters': [
      'Show employees with salary greater than 50000',
      'Find employees hired in last year',
      'List employees in Engineering department',
    ],
  };

  const allExamples = Object.values(exampleCategories).flat();

  // Typing animation effect
  useEffect(() => {
    if (question.length > 0) {
      setIsTyping(true);
      const timer = setTimeout(() => setIsTyping(false), 500);
      return () => clearTimeout(timer);
    }
  }, [question]);

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
      setError(err.response?.data?.error || 'Failed to process query. Please check your connection.');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleExampleClick = (example) => {
    setQuestion(example);
    setError(null);
  };

  const clearAll = () => {
    setQuestion('');
    setResult(null);
    setError(null);
  };

  const renderTable = (data) => {
    if (!data || data.length === 0) {
      return (
        <div className="no-data">
          <div className="no-data-icon">📭</div>
          <p>No results found</p>
          <small>Try a different query</small>
        </div>
      );
    }

    const columns = Object.keys(data[0]);

    return (
      <div className="table-container">
        <div className="result-header">
          <div className="result-info">
            <h3>Query Results</h3>
            <span className="result-count">{data.length} {data.length === 1 ? 'row' : 'rows'}</span>
          </div>
          <button className="export-btn" onClick={() => exportToCSV(data)}>
            📥 Export CSV
          </button>
        </div>
        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th className="row-number">#</th>
                {columns.map((col, idx) => (
                  <th key={idx}>
                    <div className="column-header">
                      {col}
                    </div>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {data.map((row, rowIdx) => (
                <tr key={rowIdx} className="fade-in-row" style={{animationDelay: `${rowIdx * 0.03}s`}}>
                  <td className="row-number">{rowIdx + 1}</td>
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

  const exportToCSV = (data) => {
    if (!data || data.length === 0) return;
    
    const headers = Object.keys(data[0]);
    const csvContent = [
      headers.join(','),
      ...data.map(row => headers.map(h => `"${row[h] || ''}"`).join(','))
    ].join('\n');
    
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `query-results-${Date.now()}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
  };

  return (
    <div className="App">
      {/* Animated Background */}
      <div className="background-animation">
        <div className="gradient-orb orb-1"></div>
        <div className="gradient-orb orb-2"></div>
        <div className="gradient-orb orb-3"></div>
      </div>

      <div className="container">
        {/* Header */}
        <header className="header">
          <div className="header-content">
            <div className="logo-section">
              <div className="logo-icon">🔮</div>
              <div>
                <h1 className="main-title">
                  NL<span className="highlight">2</span>SQL
                </h1>
                <p className="subtitle">Natural Language to SQL Query Interface</p>
              </div>
            </div>
            <p className="tagline">
              Ask questions in plain English, get instant SQL insights from your database
            </p>
          </div>
        </header>

        {/* Main Content */}
        <div className="main-content">
          {/* Query Input Section */}
          <div className="query-section">
            <form onSubmit={handleSubmit} className="query-form">
              <div className="input-wrapper">
                <div className="input-label">
                  <span className="label-icon">💬</span>
                  <span>Ask your question</span>
                  {isTyping && <span className="typing-indicator">...</span>}
                </div>
                <textarea
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  placeholder="e.g., Show all customers from New York, Top 10 highest paid employees, Count orders by month..."
                  rows="3"
                  disabled={loading}
                  className={isTyping ? 'typing' : ''}
                />
                <div className="input-actions">
                  <button 
                    type="button"
                    onClick={clearAll}
                    className="clear-btn"
                    disabled={loading || !question}
                  >
                    ✕ Clear
                  </button>
                  <button 
                    type="submit" 
                    disabled={loading || !question.trim()}
                    className="submit-btn"
                  >
                    {loading ? (
                      <>
                        <span className="spinner"></span>
                        <span>Processing...</span>
                      </>
                    ) : (
                      <>
                        <span className="btn-icon">✨</span>
                        <span>Generate Query</span>
                      </>
                    )}
                  </button>
                </div>
              </div>
            </form>
          </div>

          {/* Example Questions */}
          <div className="examples-section">
            <div className="examples-header">
              <h3>💡 Example Questions</h3>
              <p>Click any question to try it out</p>
            </div>
            
            <div className="examples-categories">
              {Object.entries(exampleCategories).map(([category, examples]) => (
                <div key={category} className="category-group">
                  <h4 className="category-title">{category}</h4>
                  <div className="examples-grid">
                    {examples.map((example, idx) => (
                      <button
                        key={idx}
                        onClick={() => handleExampleClick(example)}
                        className="example-btn"
                        disabled={loading}
                      >
                        <span className="example-icon">→</span>
                        {example}
                      </button>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Error Display */}
          {error && (
            <div className="error-box animate-in">
              <div className="error-icon">⚠️</div>
              <div className="error-content">
                <strong>Error</strong>
                <p>{error}</p>
              </div>
              <button className="error-close" onClick={() => setError(null)}>✕</button>
            </div>
          )}

          {/* Results Section */}
          {result && (
            <div className="results-section animate-in">
              {/* SQL Query Display */}
              <div className="sql-box">
                <div className="sql-header">
                  <div className="sql-title">
                    <span className="sql-icon">⚡</span>
                    <h3>Generated SQL Query</h3>
                  </div>
                  <div className="sql-actions">
                    <button 
                      className="copy-btn"
                      onClick={() => {
                        navigator.clipboard.writeText(result.sql);
                        alert('SQL copied to clipboard!');
                      }}
                    >
                      📋 Copy
                    </button>
                    <button 
                      className="toggle-btn"
                      onClick={() => setShowSQL(!showSQL)}
                    >
                      {showSQL ? '🙈 Hide' : '👁️ Show'}
                    </button>
                  </div>
                </div>
                {showSQL && (
                  <div className="sql-content">
                    <pre className="sql-query">{result.sql}</pre>
                  </div>
                )}
              </div>

              {/* Data Table */}
              {renderTable(result.data)}
            </div>
          )}
        </div>

        {/* Footer */}
        <footer className="footer">
          <div className="footer-content">
            <div className="footer-info">
              <p>Powered by</p>
              <div className="tech-stack">
                <span className="tech-badge">Django</span>
                <span className="tech-badge">React</span>
                <span className="tech-badge">OpenAI</span>
                <span className="tech-badge">SQL Server</span>
              </div>
            </div>
            <div className="footer-stats">
              {result && (
                <div className="stat-item">
                  <span className="stat-value">{result.rowCount}</span>
                  <span className="stat-label">Results</span>
                </div>
              )}
            </div>
          </div>
        </footer>
      </div>
    </div>
  );
}

export default App;