import { useState } from 'react'
import './App.css'
import Header from './components/Header'
import HeroSection from './components/HeroSection'
import TabSelector from './components/TabSelector'
import ShortLinkForm from './components/ShortLinkForm'
import QRCodeForm from './components/QRCodeForm'
import ResultDisplay from './components/ResultDisplay'
import ErrorMessage from './components/ErrorMessage'

function App() {
  const [activeTab, setActiveTab] = useState('shortlink')
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')

  const handleTabChange = (tab) => {
    setActiveTab(tab)
    setResult(null)
    setError('')
  }

  const handleResult = (resultData) => {
    setResult(resultData)
    setError('')
  }

  const handleError = (errorMessage) => {
    setError(errorMessage)
    setResult(null)
  }

  const handleReset = () => {
    setResult(null)
    setError('')
  }

  return (
    <div className="app">
      <Header />
      
      <main className="main">
        <HeroSection />
        
        <div className="content-container">
          <TabSelector activeTab={activeTab} onTabChange={handleTabChange} />
          
          <div className="form-section">
            {activeTab === 'shortlink' ? (
              <ShortLinkForm onResult={handleResult} onError={handleError} />
            ) : (
              <QRCodeForm onResult={handleResult} onError={handleError} />
            )}
            
            <ErrorMessage error={error} />
            
            {result && (
              <ResultDisplay result={result} onReset={handleReset} />
            )}
          </div>
        </div>
      </main>

      <footer className="footer">
        <p>Built with React & Flask</p>
      </footer>
    </div>
  )
}

export default App
