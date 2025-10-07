# University Finder API

A comprehensive Django-based university finder application with Google OAuth authentication, interactive mapping, and multi-country university data.

## 🚀 Features

- **Google OAuth Authentication** - Secure login with Google accounts
- **Multi-Country University Data** - 1,715+ universities across 9 countries
- **Interactive Google Maps** - Visual university locations with markers
- **Country-Based Filtering** - Universities from Philippines, Japan, India, Australia, Canada, Singapore, Thailand, Saudi Arabia, United Kingdom
- **Real-time Search** - Search universities within selected countries
- **Responsive Design** - Mobile-friendly interface with Bootstrap
- **REST API** - Backend API for university data and locations

## 📋 APIs Used

### External APIs

#### 1. **Google OAuth 2.0 API**

- **Purpose**: User authentication and authorization
- **Endpoints Used**:
  - `https://accounts.google.com/o/oauth2/v2/auth` - OAuth authorization
  - `https://oauth2.googleapis.com/token` - Token exchange
  - `https://www.googleapis.com/oauth2/v2/userinfo` - User profile data
- **Authentication**: Client ID/Secret from Google Cloud Console
- **Data Retrieved**: User email, name, profile picture

#### 2. **Google Maps JavaScript API**

- **Purpose**: Interactive map display and university location visualization
- **Features Used**:
  - Map rendering and markers
  - Info windows for university details
  - Geocoding (coordinates to addresses)
- **Authentication**: API key from Google Cloud Console

#### 3. **OpenStreetMap Nominatim API**

- **Purpose**: Geocoding service for university coordinates
- **Endpoint**: `https://nominatim.openstreetmap.org/search`
- **Features**:
  - University address to latitude/longitude conversion
  - Reverse geocoding capabilities
- **Authentication**: User-Agent header required
- **Rate Limiting**: 1 request/second

#### 4. **Hipolabs Universities API**

- **Purpose**: Source of university data
- **Endpoint**: `http://universities.hipolabs.com/search`
- **Parameters**: `country={country_name}`
- **Data Retrieved**: University names, countries, domains, websites
- **Authentication**: None required

## 🔄 System Flow Architecture

### Frontend Flow (User Journey)

```
1. User visits website
   ↓
2. Redirected to login (if not authenticated)
   ↓
3. Google OAuth authentication
   ↓
4. User lands on home page
   ↓
5. Clicks "Universities" → universities page
   ↓
6. Selects country from dropdown
   ↓
7. Universities load from database
   ↓
8. Interactive map shows university locations
   ↓
9. User can search within selected country
   ↓
10. Click "Locate" to see university on map
```

### Backend Flow (Data Processing)

#### Initial Data Loading

```
Management Command: load_universities
↓
For each country in [Philippines, Japan, India, Australia, Canada, Singapore, Thailand, Saudi Arabia, United Kingdom]:
    ↓
    Call Hipolabs API: /search?country={country}
    ↓
    For each university returned:
        ↓
        Call Nominatim API to get coordinates
        ↓
        Store in database: University(name, country, lat, lng)
```

#### Runtime University Display

```
User selects country on frontend
↓
Frontend calls: GET /api/universities/?country={selected_country}
↓
Django view filters universities from database
↓
Returns JSON with university list
↓
Frontend renders university cards
↓
Frontend calls: GET /api/university-locations/?country={selected_country}
↓
Returns coordinates for map markers
↓
Google Maps renders with university markers
```

#### Authentication Flow

```
User clicks "Login with Google"
↓
Django redirects to: accounts/google/login/
↓
Google OAuth consent screen
↓
User grants permission
↓
Google redirects to: accounts/google/login/callback/
↓
Django exchanges code for access token
↓
Fetches user profile from Google
↓
Creates/updates user in database
↓
Logs user in and redirects to home
```

### Database Flow

#### Models Structure

```
User (Django auth)
    ↓
SocialAccount (allauth) → Google OAuth data
    ↓
University (name, country, lat, lng)
```

#### API Endpoints

```
GET  /api/universities/           → List universities by country
GET  /api/university-locations/   → Get coordinates for map
GET  /api/search-university/      → Search university by name
GET  /api/user/                   → Current user info
```

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.8+
- Django 5.2+
- PostgreSQL (recommended) or SQLite

### 1. Clone and Install

```bash
git clone <repository-url>
cd university-finder-api
pip install -r requirements.txt
```

### 2. Environment Setup

Create a `.env` file in the project root:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
DATABASE_URL=postgresql://user:password@localhost:5432/university_finder
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_API_KEY=your-google-maps-api-key
```

### 3. Google OAuth Setup

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

### 4. Google Maps Setup

1. In Google Cloud Console, enable "Maps JavaScript API"
2. Create an API key with restrictions for your domain
3. Add the API key to your `.env` file

### 5. Database Setup

```bash
python manage.py migrate
python manage.py load_universities  # Load university data
```

### 6. Run the Application

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to access the application.

## 📊 Data Management

### Loading University Data

The system includes a management command to load universities for all supported countries:

```bash
python manage.py load_universities
```

This command:

- Fetches data from Hipolabs Universities API
- Geocodes university locations using OpenStreetMap Nominatim
- Stores data in the local database for fast retrieval

### Supported Countries

- Philippines (default)
- Japan
- India
- Australia
- Canada
- Singapore
- Thailand
- Saudi Arabia
- United Kingdom

## 🔒 Security & Performance

### Security Measures

- CSRF protection on forms
- HTTPS enforcement in production
- OAuth 2.0 secure token handling
- Content Security Policy (CSP) headers

### Performance Optimizations

- Database indexing on country field
- Coordinate caching in database
- Lazy loading of map components
- CDN for static assets (Bootstrap, Font Awesome)

## 🏗️ Project Structure

```
university-finder-api/
├── api/                    # Main application
│   ├── models.py          # Database models
│   ├── views.py           # API views
│   ├── views_frontend.py  # Frontend views
│   ├── serializers.py     # API serializers
│   └── urls.py           # API URL patterns
├── config/                # Django settings
│   ├── settings.py       # Main settings
│   ├── urls.py           # URL configuration
│   └── adapters.py       # Social auth adapters
├── templates/            # HTML templates
│   ├── navbar.html       # Navigation component
│   ├── home.html         # Home page
│   ├── universities.html # Universities page
│   ├── account/          # Authentication templates
│   └── socialaccount/    # Social auth templates
├── static/               # Static files
├── manage.py            # Django management script
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Hipolabs Universities API](http://universities.hipolabs.com/) for university data
- [OpenStreetMap Nominatim](https://nominatim.openstreetmap.org/) for geocoding
- [Google Maps Platform](https://developers.google.com/maps) for mapping
- [Django Allauth](https://django-allauth.readthedocs.io/) for authentication
