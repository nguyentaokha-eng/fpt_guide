# FPT Guide Campus DN

A Django web application for FPT University Đà Nẵng students.

## Tech Stack

- **Backend:** Django 6.0.1
- **Database:** SQLite3 (db.sqlite3)
- **Frontend:** HTML, CSS, JavaScript (Jinja2 templates)
- **Deployment:** Railway (Gunicorn + WhiteNoise)

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| Django | 6.0.1 | Web framework |
| gunicorn | 25.0.3 | WSGI server for production |
| whitenoise | 6.8.2 | Static file serving for production |
| django-cors-headers | 4.9.0 | CORS support for API |
| asgiref | 3.11.0 | ASGI interface |
| sqlparse | 0.5.5 | SQL parsing |
| packaging | 26.0 | Package version parsing |
| tzdata | 2025.3 | Timezone data |

## Project Structure

```
fpt_guide/
├── fpt_guide/          # Django project settings
│   ├── settings.py     # Django settings
│   ├── urls.py        # Root URL configuration
│   └── wsgi.py        # WSGI application
├── home/              # Main app
│   ├── models.py       # Database models
│   ├── views.py        # View functions
│   ├── urls.py         # App URLs
│   └── admin.py        # Admin panel
├── templates/          # HTML templates
│   ├── base.html       # Base template
│   ├── home.html       # Home page
│   ├── families.html   # Club listings (slider)
│   ├── Afford_food.html    # Restaurant listings
│   ├── Afford_living.html  # Accommodation listings
│   ├── Afford_job.html     # Job listings
│   ├── rate_lecture.html   # Lecturer reviews
│   ├── lecturer_detail.html # Individual lecturer page
│   └── ...
├── static/            # Static files (development)
│   ├── css/           # Stylesheets
│   └── image/         # Images
│       ├── clubs/     # Club images
│       ├── food/      # Restaurant images
│       ├── living/    # Accommodation images
│       └── comments/  # Comment/user images
├── staticfiles/       # Collected static files (production)
└── db.sqlite3         # SQLite database

## Features

- **Home Page** - Overview of campus life
- **Families (Clubs)** - Interactive club slider with filtering
- **Afford Food** - Restaurant listings with reviews & ratings
- **Afford Living** - Accommodation listings with reviews
- **Afford Job** - Part-time job listings
- **Rate Lecture** - Lecturer review system
- **Curriculum** - Course information
- **Student Life** - Campus activities

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/comment/<place_id>/` | POST | Submit a comment/rating |
| `/comment/list/<place_id>/` | GET | Get comments for a place |

## Static Files Configuration

**Development:** Files served from `static/`
**Production:** Files served from `staticfiles/` via WhiteNoise

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files (production)
python manage.py collectstatic --noinput

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

## Deployment (Railway)

1. Connect GitHub repository to Railway
2. Set environment variables if needed
3. Railway automatically runs:
   - `pip install -r requirements.txt`
   - `python manage.py collectstatic --noinput` (from Procfile)
   - Start Gunicorn server

## Environment Variables (Railway)

- `SECRET_KEY` - Django secret key (auto-generated)
- `DEBUG` - Set to `True` for development
- `ALLOWED_HOSTS` - Include Railway URL

## Database Models

- **Member** - Team members
- **Experience** - Past experiences
- **Lecturer** - Lecturer information
- **Review** - Lecturer reviews
- **Place** - Restaurants/Accommodations
- **Comment** - User comments with ratings

## Image Directories

| Directory | Purpose |
|-----------|---------|
| `static/image/clubs/` | Club/organization photos |
| `static/image/food/` | Restaurant photos |
| `static/image/living/` | Accommodation photos |
| `static/image/comments/` | User avatar placeholders |

## License

MIT
