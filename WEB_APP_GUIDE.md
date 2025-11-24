# Web Application Quick Start Guide

## Starting the Web App

### Development Mode (Default)
```bash
python web_app.py
```
- Accessible at: http://localhost:5000
- Debug mode enabled
- Auto-reloads on code changes

### Custom Configuration
```bash
# Allow external access (use with caution)
export FLASK_HOST=0.0.0.0
export FLASK_PORT=8080
python web_app.py
```

### Production Deployment
```bash
# Install Gunicorn
pip install gunicorn

# Set required environment variables
export FLASK_ENV=production
export FLASK_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex())')"

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 web_app:app
```

## Using the Web Interface

1. **Select States**: Click on one or more state boxes (they'll turn blue when selected)
2. **Optional: Set Page Limit**: For testing, enter a number like `5` to limit pages scraped
3. **Start Scraping**: Click the "🚀 Start Scraping" button
4. **Download Results**: Once complete, download Excel files from the "Available Downloads" section

## API Access

### Check Available Files
```bash
curl http://localhost:5000/api/status
```

Response:
```json
{
  "files": [
    {
      "filename": "vrm_listings_2024-11-24.xlsx",
      "size": 12345,
      "modified": "2024-11-24T12:34:56.789012"
    }
  ]
}
```

### Download a File Programmatically
```bash
curl -O http://localhost:5000/download/vrm_listings_2024-11-24.xlsx
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `FLASK_HOST` | `127.0.0.1` | Host to bind to |
| `FLASK_PORT` | `5000` | Port to run on |
| `FLASK_DEBUG` | `1` | Debug mode (1=on, 0=off) |
| `FLASK_SECRET_KEY` | dev key | Secret key for sessions (required in production) |
| `FLASK_ENV` | development | Environment (production enforces secret key) |

## Security Notes

- **Development**: Uses localhost by default for security
- **Production**: Requires `FLASK_SECRET_KEY` to be set
- **File Access**: Only Excel files matching pattern `vrm_listings_*.xlsx` can be downloaded
- **State Validation**: Only pre-defined states can be selected
- **Subprocess Safety**: Command injection protection via validated input lists
