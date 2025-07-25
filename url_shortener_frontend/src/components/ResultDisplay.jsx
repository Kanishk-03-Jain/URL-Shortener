import { useState } from 'react'

function ResultDisplay({ result, onReset }) {
  const [copied, setCopied] = useState(false)

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(result.shortUrl)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (err) {
      console.error('Failed to copy: ', err)
    }
  }

  if (result.type === 'shortlink') {
    return (
      <div className="result-section">
        <h3>Your shortened URL:</h3>
        <div className="result-container">
          <input
            type="text"
            value={result.shortUrl}
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
            href={result.shortUrl} 
            target="_blank" 
            rel="noopener noreferrer"
            className="test-link"
          >
            Test Link
          </a>
          <button onClick={onReset} className="reset-btn">
            Shorten Another
          </button>
        </div>
      </div>
    )
  }

  if (result.type === 'qrcode') {
    return (
      <div className="qr-result-section">
        <div className="qr-content">
          <div className="qr-left">
            <h3>Your QR Code & Short URL:</h3>
            <div className="result-container">
              <input
                type="text"
                value={result.shortUrl}
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
                href={result.shortUrl} 
                target="_blank" 
                rel="noopener noreferrer"
                className="test-link"
              >
                Test Link
              </a>
              <button onClick={onReset} className="reset-btn">
                Generate Another
              </button>
            </div>
          </div>
          <div className="qr-right">
            <div className="qr-code-container">
              <img 
                src={`data:image/png;base64,${result.qrCodeBase64}`}
                alt="QR Code"
                className="qr-code-image"
              />
            </div>
          </div>
        </div>
      </div>
    )
  }

  return null
}

export default ResultDisplay