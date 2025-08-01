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
Corporate website with project portfolio, blog, contact systems, and solar energy simulator. Future dashboard functionality for client monitoring.

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

### Testing Commands:
```bash
# No test framework currently configured
# Tests should be added using Django's built-in testing or pytest-django
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
- **apps/core**: Main application - homepage, about, services, and project models
- **apps/projects**: Project portfolio management (uses models from core app)
- **apps/blog**: News and articles system (models not yet implemented)
- **apps/contact**: Contact forms and WhatsApp integration (models not yet implemented)
- **apps/dashboard**: Future client dashboard functionality

### Key Models (apps/core/models.py):
- **Project**: Solar installation projects with images, descriptions, and technical specs
- **SimuladorConfig**: Global configuration for the solar energy simulator
- **CostoInstalacion**: Installation cost ranges by power capacity
- **FactorUbicacion**: Solar irradiation factors by Argentine provinces
- **FactorOrientacion**: Efficiency factors by roof orientation
- **TipoTejado**: Roof types with complexity factors
- **AnguloTejado**: Roof inclination angles with efficiency factors

### URL Structure:
- `/` - Homepage (core app)
- `/proyectos/` - Projects portfolio
- `/simulador/` - Solar energy simulator
- `/blog/` - Blog/news section  
- `/contacto/` - Contact page
- `/admin/` - Django admin panel

### Static Files Organization:
- **CSS**: `static/css/` - Separated by functionality (base.css, header.css, footer.css, home.css, simulador.css)
- **JavaScript**: `static/js/` - Modular structure (base.js, home.js, contact.js, whatsapp.js, simulador.js)
- **Images**: `static/images/` - Organized by type, includes simulator SVG icons
- **Media**: `media/` - User uploaded files (projects, blog)

---

## Code Conventions

### Python/Django:
- Follow PEP 8 standards
- Spanish comments and docstrings for team collaboration
- Use Django's MVT pattern consistently
- Environment variables for sensitive settings via `get_env_variable()`
- Models use Spanish verbose names for admin interface
- Proper field validation and help text in Spanish

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

## Solar Energy Simulator

The project includes a comprehensive solar energy calculator with the following components:

### Simulator Models:
- **SimuladorConfig**: Global settings for calculations (efficiency, prices, autoconsumo factors)
- **CostoInstalacion**: Installation costs by power range (0-3kW, 3-5kW, 5-10kW, 10+kW)
- **FactorUbicacion**: Solar irradiation by Argentine provinces
- **FactorOrientacion**: Efficiency by roof orientation (N, NE, E, SE, S, SO, O, NO)
- **TipoTejado**: Roof types with complexity factors
- **AnguloTejado**: Inclination angles with efficiency factors

### Simulator Features:
- Annual consumption calculation
- Optimal power sizing
- Installation cost estimation
- Battery system options
- Electric vehicle integration
- ROI and payback calculations
- Province-specific solar irradiation
- Roof type and orientation optimization

### Simulator URL:
- `/simulador/` - Interactive solar calculator
- AJAX endpoint: `/calcular-solar/` (POST)

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

### Security Considerations:
- Check `docs/Bug_tracking.md` for critical security issues
- Never commit sensitive data (passwords, keys) with default values
- Validate all user inputs in calculator endpoints
- Use environment variables for all sensitive settings

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
- Test solar calculator with various input combinations
- Verify AJAX endpoints return valid JSON responses

---

## Known Issues & Considerations

### Critical Issues (see docs/Bug_tracking.md):
- Blog and Contact apps have empty models but are in INSTALLED_APPS
- Some URL patterns may reference non-existent views
- MEDIA_URL/MEDIA_ROOT configuration required for ImageField
- Input validation missing in calculator endpoints

### Dependencies:
- `python-decouple` installed but not used (consider using for better environment variable handling)
- No testing framework configured (recommend adding pytest-django)

### Regional Settings:
- Project targets Argentine market (provinces, phone numbers)
- Solar irradiation data specific to Argentina
- Currency calculations in USD