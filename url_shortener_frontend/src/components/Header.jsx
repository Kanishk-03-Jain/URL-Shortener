import config from '../config'

function Header() {
  return (
    <header className="header">
      <div className="header-content">
        <div className="logo">
          <span className="logo-icon">🔗</span>
          <span className="logo-text">{config.APP_NAME}</span>
        </div>
        <nav className="nav">
          <button className="nav-btn">Platform</button>
          <button className="nav-btn">Solutions</button>
          <button className="nav-btn">Pricing</button>
          <button className="nav-btn">Resources</button>
          <div className="nav-actions">
            <button className="login-btn">Log in</button>
            <button className="signup-btn">Sign up Free</button>
          </div>
        </nav>
      </div>
    </header>
  )
}

export default Header