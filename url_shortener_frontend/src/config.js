// Configuration for the URL Shortener frontend
export const config = {
  // Backend API URL - change this to your deployed backend URL
  API_BASE_URL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000',
  
  // App settings
  APP_NAME: 'URL Shortener',
  APP_DESCRIPTION: 'Transform long URLs into short, shareable links',
}

export default config