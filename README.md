# University Finder API

## Authentication & Geocoding Setup

### Google OAuth Setup

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

10. **Optional - For Advanced Markers (removes deprecation warning):**

    - In Google Cloud Console, go to "Maps Management" > "Map IDs"
    - Create a new Map ID
    - Copy the Map ID and add it to your `.env`:
      ```
      GOOGLE_MAP_ID=your-map-id-here
      ```

11. Update your `.env` file with the credentials:

    ```
    GOOGLE_CLIENT_ID=your-actual-client-id
    GOOGLE_CLIENT_SECRET=your-actual-client-secret
    ```

12. Run the Django server and visit `/accounts/google/login/` to test Google authentication

### Geocoding (University Locations)

**This app uses OpenStreetMap Nominatim API (FREE - No API keys required!)**

- ✅ **No billing setup needed**
- ✅ **No API keys required**
- ✅ **Completely free**
- ✅ **Good coverage for universities worldwide**

The app automatically fetches university coordinates using OpenStreetMap's free geocoding service.

## Interactive Maps with Google Maps

**✅ Google Maps is now integrated with the latest AdvancedMarkerElement API!**

- ✅ **No more deprecation warnings** - Uses the latest Google Maps API
- ✅ **Beautiful interactive maps** - Click universities to see locations
- ✅ **Advanced markers** - Modern pin elements with custom styling
- ✅ **Responsive design** - Works perfectly on all devices
- ✅ **Graceful fallbacks** - App works even if maps fail to load

### Maps Features:

- **University markers** with custom pins and info windows
- **Click-to-locate** - Click any university card to center the map
- **Auto-fitting** - Map automatically adjusts to show all universities
- **Search integration** - Individual university search when needed

### Free Geocoding:

- **OpenStreetMap Nominatim** provides accurate coordinates
- **No API keys required** for geocoding
- **Worldwide coverage** for university locations

**The app combines the best of both worlds: Free geocoding + Premium interactive maps!**

## Features

- **Google Authentication**: Sign in with Google OAuth
- **University Search**: Search universities by country and name
- **Country Selection**: Browse universities from 9 countries
- **Interactive Maps**: Click universities to see locations on Google Maps
- **Advanced Markers**: Modern pin elements with info windows
- **Favorites System**: Save universities for later
- **Responsive Design**: Works on all devices
- **Free Geocoding**: OpenStreetMap Nominatim (no API keys needed)

## Running the Application

1. Install dependencies: `pip install -r requirements.txt`
2. Set up your `.env` file with required environment variables
3. Run migrations: `python manage.py migrate`
4. Start the server: `python manage.py runserver`
