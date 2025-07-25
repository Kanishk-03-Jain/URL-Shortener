function ErrorMessage({ error }) {
  if (!error) return null

  return (
    <div className="error-message">
      <span className="error-icon">⚠️</span>
      {error}
    </div>
  )
}

export default ErrorMessage