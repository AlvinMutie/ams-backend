import os

class Config:
    # Flask secret key for sessions
    SECRET_KEY = 'your-super-secret-key-change-this-in-production'
    
    # Google OAuth 2.0 Configuration
    # Get these from: https://console.cloud.google.com/apis/credentials
    GOOGLE_CLIENT_ID = 'your-google-client-id-here'
    GOOGLE_CLIENT_SECRET = 'your-google-client-secret-here'
    
    # Redirect URI - this should match what you set in Google Cloud Console
    GOOGLE_REDIRECT_URI = 'http://localhost:5000/auth/google/callback'
    
    # OAuth scopes - what information we want from Google
    GOOGLE_SCOPES = [
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile'
    ]
    
    # Database path
    DATABASE_PATH = 'database.db'

# Instructions to get Google OAuth credentials:
# 1. Go to https://console.cloud.google.com/
# 2. Create a new project or select existing one
# 3. Enable Google+ API and Google OAuth2 API
# 4. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client IDs"
# 5. Choose "Web application"
# 6. Add authorized redirect URIs:
#    - http://localhost:5000/auth/google/callback (for development)
#    - https://your-domain.com/auth/google/callback (for production)
# 7. Copy the Client ID and Client Secret
# 8. Replace the placeholder values above with your actual credentials
