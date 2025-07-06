# 🔗 URL Shortener

A full-stack URL shortener application that transforms long URLs into short, shareable links. Built with React frontend and Flask backend.

## Architecture

```
URL Shortener/
├── url_shortener_backend/     # Flask API backend
│   ├── main.py               # Main application entry point
│   ├── config.py             # Configuration settings
│   ├── requirements.txt      # Python dependencies
│   ├── routes/              # API route handlers
│   ├── services/            # Business logic and database services
│   └── utilities/           # Helper functions and utilities
└── url_shortener_frontend/   # React frontend
    ├── src/
    │   ├── App.jsx          # Main React component
    │   ├── config.js        # Frontend configuration
    │   └── assets/          # Static assets
    ├── package.json         # Node.js dependencies
    └── vite.config.js       # Vite build configuration
```

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+**
- **Node.js 16+**
- **PostgreSQL 12+**

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd url_shortener_backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Create .env file
   ```
   
   Configure your `.env` file:
   ```env
   DEBUG=true
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=url_shortener
   DB_USER=postgres
   DB_PASSWORD=your-password
   ```

5. **Set up database**
   ```bash
   # Create PostgreSQL database
   createdb url_shortener
   ```

6. **Run the backend**
   ```bash
   python main.py
   ```

The backend will be available at `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd url_shortener_frontend
   ```

2. **Install dependencies**
   ```bash
   bun install
   ```

3. **Configure environment** (optional)
   ```bash
   # Create .env file for custom API URL
   echo "VITE_API_BASE_URL=http://localhost:5000" > .env
   ```

4. **Start development server**
   ```bash
   bun run dev
   ```

The frontend will be available at `http://localhost:5173`

## 📚 API Documentation

### Endpoints

#### `POST /shorten`
Shortens a given URL.

**Request Body:**
```json
{
  "url": "https://example.com/very-long-url-here"
}
```

**Response:**
```json
{
  "short_url": "http://localhost:5000/abc12345"
}
```

#### `GET /{hash}`
Redirects to the original URL.

**Response:** 302 redirect to original URL

#### `GET /`
Returns API welcome message.

**Response:**
```json
{
  "message": "Welcome to the URL Shortener API"
}
```

### Error Handling

All endpoints return appropriate HTTP status codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `404` - Not Found
- `500` - Internal Server Error

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and commit: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔮 Future Enhancements

- [ ] User authentication and personal URL management
- [ ] Analytics dashboard with click tracking
- [ ] Custom alias support
- [ ] QR code generation
- [ ] URL expiration dates
- [ ] Bulk URL shortening
- [ ] API rate limiting
- [ ] URL preview functionality

## 💡 Support

For questions or issues, please:
1. Check the [Issues](../../issues) section
2. Create a new issue if your problem isn't already listed
3. Provide detailed information about your environment and the problem

------