# University Finder API

## Google OAuth Setup

To enable Google authentication, follow these steps:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google+ API
4. Go to "Credentials" in the left sidebar
5. Click "Create Credentials" > "OAuth 2.0 Client IDs"
6. Configure the OAuth consent screen if prompted
7. Set the application type to "Web application"
8. Add authorized redirect URIs:
   - For development: `http://127.0.0.1:8000/accounts/google/login/callback/`
   - For production: `https://yourdomain.com/accounts/google/login/callback/`
     (Remember to change ACCOUNT_DEFAULT_HTTP_PROTOCOL back to 'https' in production)
9. Copy the Client ID and Client Secret

10. Update your `.env` file with the credentials:

    ```
    GOOGLE_CLIENT_ID=your-actual-client-id
    GOOGLE_CLIENT_SECRET=your-actual-client-secret
    ```

11. Run the Django server and visit `/accounts/google/login/` to test Google authentication

## Google Maps Setup (Optional)

The application includes optional Google Maps integration for university locations. The university search and all other features work perfectly without maps.

### To Enable Maps (Optional):
1. **Enable Billing**: Google Maps requires billing to be enabled on your Google Cloud project
2. **Enable APIs**: Make sure both "Maps JavaScript API" and "Places API" are enabled
3. **API Key**: The same `GOOGLE_API_KEY` from your `.env` file is used for maps

### Without Maps:
- ✅ University search works perfectly
- ✅ Country selection works perfectly
- ✅ Favorites system works perfectly
- ✅ All core functionality is available
- Map area shows a helpful message explaining the search still works

**Note**: Maps are a bonus feature. The entire application functions perfectly without Google Maps billing.

## Features

- **Google Authentication**: Sign in with Google OAuth
- **University Search**: Search universities by country and name
- **Interactive Maps**: Click universities to see their locations
- **Favorites System**: Save universities for later
- **Responsive Design**: Works on all devices

## Running the Application

1. Install dependencies: `pip install -r requirements.txt`
2. Set up your `.env` file with required environment variables
3. Run migrations: `python manage.py migrate`
4. Start the server: `python manage.py runserver`
