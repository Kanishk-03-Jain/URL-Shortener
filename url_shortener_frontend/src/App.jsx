import { useState } from 'react'
import './App.css'
import config from './config'

function App() {
  const [originalUrl, setOriginalUrl] = useState('')
  const [shortenedUrl, setShortenedUrl] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [copied, setCopied] = useState(false)

  const API_BASE_URL = config.API_BASE_URL

  const validateUrl = (url) => {
    try {
      const urlObj = new URL(url)
      return ['http:', 'https:'].includes(urlObj.protocol)
    } catch {
      return false
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!originalUrl.trim()) {
      setError('Please enter a URL')
      return
    }

    if (!validateUrl(originalUrl)) {
      setError('Please enter a valid URL (must start with http:// or https://)')
      return
    }

    setIsLoading(true)
    setError('')
    setShortenedUrl('')

    try {
      const response = await fetch(`${API_BASE_URL}/shorten`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: originalUrl }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.error || 'Failed to shorten URL')
      }

      setShortenedUrl(data.short_url)
    } catch (err) {
      setError(err.message || 'An error occurred while shortening the URL')
    } finally {
      setIsLoading(false)
    }
  }

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(shortenedUrl)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (err) {
      console.error('Failed to copy: ', err)
    }
  }

  const reset = () => {
    setOriginalUrl('')
    setShortenedUrl('')
    setError('')
    setCopied(false)
  }

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <h1>🔗 {config.APP_NAME}</h1>
          <p>{config.APP_DESCRIPTION}</p>
        </header>

        <main className="main">
          <form onSubmit={handleSubmit} className="form">
            <div className="input-group">
              <input
                type="url"
                value={originalUrl}
                onChange={(e) => setOriginalUrl(e.target.value)}
                placeholder="Enter your long URL here..."
                className="url-input"
                disabled={isLoading}
              />
              <button 
                type="submit" 
                className="shorten-btn"
                disabled={isLoading || !originalUrl.trim()}
              >
                {isLoading ? 'Shortening...' : 'Shorten'}
              </button>
            </div>
          </form>

          {error && (
            <div className="error-message">
              <span className="error-icon">⚠️</span>
              {error}
            </div>
          )}

          {shortenedUrl && (
            <div className="result-section">
              <h3>Your shortened URL:</h3>
              <div className="result-container">
                <input
                  type="text"
                  value={shortenedUrl}
                  readOnly
                  className="result-input"
                />
                <button 
                  onClick={copyToClipboard}
                  className="copy-btn"
                  title="Copy to clipboard"
                >
                  {copied ? '✓' : '📋'}
                </button>
              </div>
              <div className="result-actions">
                <a 
                  href={shortenedUrl} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="test-link"
                >
                  Test Link
                </a>
                <button onClick={reset} className="reset-btn">
                  Shorten Another
                </button>
              </div>
            </div>
          )}
        </main>

        <footer className="footer">
          <p>Built with React & Flask</p>
        </footer>
      </div>
    </div>
  )
}

export default App
