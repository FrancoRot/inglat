# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Context
**INGLAT** - Renewable energy installations and monitoring company (photovoltaic)

### Technology Stack:
- **Backend**: Django 5.2.4 + Python 3.11+
- **Database**: PostgreSQL  
- **Frontend**: HTML + CSS + JavaScript (Vanilla)
- **Version Control**: Git

### Current Project Phase:
Corporate website with project portfolio, blog, and contact systems. Future dashboard functionality for client monitoring.

---

## Development Commands

### Django Management:
```bash
# Run development server
python manage.py runserver

# Create and apply migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser for admin
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Shell access
python manage.py shell
```

### Database Operations:
```bash
# Reset database (development only)
python manage.py flush

# Load fixtures
python manage.py loaddata <fixture_name>

# Database shell
python manage.py dbshell
```

### Virtual Environment:
```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

---

## Architecture Overview

### Django Apps Structure:
- **apps/core**: Main application - homepage, about, services
- **apps/projects**: Project portfolio management (models in core app)
- **apps/blog**: News and articles system
- **apps/contact**: Contact forms and WhatsApp integration
- **apps/dashboard**: Future client dashboard functionality

### Key Models:
- **Project** (apps.core.models): Solar installation projects with images, descriptions, and technical specs
- **Blog models** (apps.blog): Articles and news content
- **Contact models** (apps.contact): Contact form submissions

### URL Structure:
- `/` - Homepage (core app)
- `/proyectos/` - Projects portfolio
- `/blog/` - Blog/news section  
- `/contacto/` - Contact page
- `/admin/` - Django admin panel

### Static Files Organization:
- **CSS**: `static/css/` - Separated by functionality (base.css, header.css, footer.css, home.css)
- **JavaScript**: `static/js/` - Modular structure (base.js, home.js, contact.js, whatsapp.js)
- **Images**: `static/images/` - Organized by type
- **Media**: `media/` - User uploaded files (projects, blog)

---

## Code Conventions

### Python/Django:
- Follow PEP 8 standards
- Spanish comments for team collaboration
- Use Django's MVT pattern consistently
- Environment variables for sensitive settings via `get_env_variable()`

### Templates:
- Extend from `templates/base/base.html`
- Use `{% load static %}` for all static file references
- Organize templates by app in `templates/<app_name>/`
- Reusable components in `templates/base/`

### CSS/JavaScript:
- **NO inline styles or scripts in templates**
- Use separate CSS/JS files per page/functionality
- Global styles in `base.css`, specific styles in dedicated files
- Reference in templates with proper static tags:
```django
{% load static %}
<link rel="stylesheet" href="{% static 'css/base.css' %}">
<link rel="stylesheet" href="{% static 'css/home.css' %}">
<script src="{% static 'js/base.js' %}"></script>
<script src="{% static 'js/home.js' %}"></script>
```

### Database:
- PostgreSQL configuration via environment variables
- Models with Spanish verbose names for admin interface
- Use slugs for SEO-friendly URLs
- Automatic timestamping with created_at/updated_at

---

## Important File Locations

### Configuration:
- `INGLAT/settings.py` - Main Django settings
- `requirements.txt` - Main dependencies file
- `requirements/` - Environment-specific requirements

### Documentation:
- `docs/PRD.md` - Product requirements and business rules
- `docs/Project_structure.md` - Detailed architecture documentation
- `docs/UI_UX_doc.md` - Design guidelines and UI specifications
- `docs/Bug_tracking.md` - Known issues and bug reports
- `docs/Implementation.md` - Implementation guidelines

### Key Apps:
- `apps/core/models.py` - Project model definition (main business logic)
- `apps/core/views.py` - Homepage and core functionality
- `INGLAT/urls.py` - Main URL routing configuration

---

## Development Workflow

### Before Making Changes:
1. Read relevant documentation from `docs/` directory
2. Check `docs/Bug_tracking.md` for known issues
3. Review `docs/UI_UX_doc.md` for design guidelines
4. Understand business rules in `docs/PRD.md`

### CSS/JS Development:
- Always use separate files, never inline
- Update `base.css` for global styles and CSS variables
- Create page-specific files for unique functionality
- Test responsive design across devices
- Follow INGLAT color scheme and branding

### Django Development:
- Use Django admin for content management
- Follow MVT pattern strictly
- Spanish field names and help text for admin users
- Proper URL naming and reverse lookups
- Optimize for SEO and performance

### Testing:
- Test all forms and user interactions
- Verify responsive design on mobile/tablet
- Check Django admin functionality for content management
- Validate SEO meta tags and schema markup