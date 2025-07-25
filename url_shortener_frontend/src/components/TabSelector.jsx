function TabSelector({ activeTab, onTabChange }) {
  return (
    <div className="tab-selector">
      <button 
        className={`tab-btn ${activeTab === 'shortlink' ? 'active' : ''}`}
        onClick={() => onTabChange('shortlink')}
      >
        <span className="tab-icon">🔗</span>
        Short link
      </button>
      <button 
        className={`tab-btn ${activeTab === 'qrcode' ? 'active' : ''}`}
        onClick={() => onTabChange('qrcode')}
      >
        <span className="tab-icon">📱</span>
        QR Code
      </button>
    </div>
  )
}

export default TabSelector