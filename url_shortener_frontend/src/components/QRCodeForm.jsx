import { useState } from 'react'
import config from '../config'

function QRCodeForm({ onResult, onError }) {
  const [originalUrl, setOriginalUrl] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const API_BASE_URL = config.API_BASE_URL

  const validateUrl = (url) => {
    if (url.length === 0) {
      return false;
    }
    const regex = /.+\..+/;
    return regex.test(url);
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!originalUrl.trim()) {
      onError('Please enter a URL')
      return
    }

    if (!validateUrl(originalUrl)) {
      onError('Please enter a valid URL')
      return
    }

    setIsLoading(true)
    onError('')

    try {
      const response = await fetch(`${API_BASE_URL}/generate_qr`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: originalUrl }),
      })

      const data = await response.json()
      console.log('QR Code response:', data)
      if (!response.ok) {
        throw new Error(data.error || 'Failed to generate QR code')
      }

      onResult({
        type: 'qrcode',
        originalUrl,
        shortUrl: data.short_url,
        qrCodeBase64: data.qr_code_base64
      })
      
    } catch (err) {
      onError(err.message || 'An error occurred while generating QR code')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="form-container">
      <h2 className="form-title">Generate QR Code</h2>
      <p className="form-subtitle">Create a QR code for your URL.</p>
      
      <form onSubmit={handleSubmit} className="url-form">
        <div className="input-container">
          <label htmlFor="qr-url-input" className="input-label">
            Paste your long link here
          </label>
          <input
            id="qr-url-input"
            type="url"
            value={originalUrl}
            onChange={(e) => setOriginalUrl(e.target.value)}
            placeholder="https://example.com/my-long-url"
            className="url-input"
            disabled={isLoading}
          />
        </div>
        <button 
          type="submit" 
          className="submit-btn"
          disabled={isLoading || !originalUrl.trim()}
        >
          {isLoading ? 'Generating...' : 'Generate QR Code'}
          <span className="btn-arrow">→</span>
        </button>
      </form>
    </div>
  )
}

export default QRCodeForm